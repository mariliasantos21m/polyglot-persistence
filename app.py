import streamlit as st
import api_client as API
import pandas as pd
import pydeck as pdk
import json

st.set_page_config(page_title="Geo Dashboard", layout="wide")
st.title("GeoJSON Dashboard com MongoDB")
st.sidebar.header("Filtros")

country_data = API.get_countries()
select_country = st.sidebar.multiselect("País", options=country_data, format_func=lambda x:x['name'])

country_ids = [country['id'] for country in select_country] if select_country else []
state_options = API.get_states(country_ids) if country_ids else []
select_state = st.sidebar.multiselect("Estado", options=state_options, format_func=lambda x:x['name'])

state_ids = [state['id'] for state in select_state] if select_state else []
city_options = API.get_cities(state_ids) if state_ids else []
select_city = st.sidebar.multiselect("Cidade", options=city_options, format_func=lambda x:x['name'])

button_search_enable = bool(select_country or select_state or select_city) 

# STATES
st.session_state["select_country"] = select_country
st.session_state["select_state"] = select_state
st.session_state["select_city"] = select_city

if "expander_open" not in st.session_state:
    st.session_state.expander_open = False

with st.expander("Inserir novo ponto", expanded= st.session_state.expander_open):
    with st.form("insert_form"):
        name = st.text_input("Nome", value="")
        category  = st.text_input("Categoria", value="")
        long  = st.number_input("Longitude")
        latv = st.number_input("Latitude")
        country = st.text_input("País", value="")
        state = st.text_input("Estado", value="")
        city = st.text_input("Cidade", value="")
        props = st.text_area("Propriedades (JSON)", value='{"rating": 4.5}')
        submitted = st.form_submit_button("Inserir")
        if submitted:
            try:
                props_dict = json.loads(props) if props.strip() else {}
                props_dict['city'] = city
                props_dict['state'] = state
                props_dict['country'] = country
            except Exception as e:
                st.error(f"JSON inválido em Propriedades: {e}")
                st.stop()
                
            body = {
                "name": name,
                "category": category,
                "properties": props_dict,
                "geometry": {"type":"Point", "coordinates":[long, latv]},
                "city": city,
                "state": state,
                "country": country
            }
            API.create_location(body)

            st.session_state.expander_open = False
            st.session_state["select_country"] = []
            st.session_state["select_state"] = []
            st.session_state["select_city"] = []

st.write("Filtre para visualizar os pontos no mapa.")

if st.sidebar.button("Buscar", disabled= not button_search_enable):
    params= {
        "city": [city['name'] for city in select_city] if select_city else None,
        "state": [state['name'] for state in select_state] if select_state else None,
        "country": [country['name'] for country in select_country] if select_country else None
    }
    response= API.get_locations(params)
    if(len(response) > 0):
        points = [d for d in response if d.get("geometry",{}).get("type") == "Point"]
        lines = [d for d in response if d.get("geometry",{}).get("type") == "LineString"]
        polys  = [d for d in response if d.get("geometry",{}).get("type") == "Polygon"]
    
        # Map center
        if points:
            center = [points[0]["geometry"]["coordinates"][1], points[0]["geometry"]["coordinates"][0]]
        else:
            center = [0, 0]

        layers = []

        if points:
            df_geo = pd.DataFrame(points)
            df_geo["lon"] = df_geo["geometry"].apply(lambda g: g["coordinates"][0])
            df_geo["lat"] = df_geo["geometry"].apply(lambda g: g["coordinates"][1])
            layers.append(pdk.Layer(
                "ScatterplotLayer",
                data=df_geo,
                get_position=["lon","lat"],
                get_radius=50,
                pickable=True,
                get_fill_color=[150, 0, 20, 200]  # vermelho com transparência
            ))

        if lines or polys:
            layers.append(pdk.Layer(
                "GeoJsonLayer",
                data={"type": "FeatureCollection", "features": response},
                pickable=True,
                stroked=True,
                filled=True,
                line_width_min_pixels=2,
                get_fill_color=[0, 255, 0, 100],   # verde semitransparente para polígonos
                get_line_color=[0, 0, 255, 200]    # azul para linhas
            ))

        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=center[0], longitude=center[1], zoom=11, pitch=0),
            layers=layers,
            tooltip={"text": "{name}\n{category}"}
        ))

        st.session_state.expander_open = False
    
