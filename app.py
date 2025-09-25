import streamlit as st
import api_client as API
import pandas as pd
import pydeck as pdk
import json
from geopy.distance import geodesic

# dados api 
location_options =  API.get_locations({})


st.set_page_config(page_title="Geo Dashboard", layout="wide")
st.title("GeoJSON Dashboard com MongoDB")

if "expander_open" not in st.session_state:
    st.session_state.expander_open = False

with st.expander("Cadastrar Novo Ponto", expanded= st.session_state.expander_open):
    with st.form("insert_form"):
        name = st.text_input("Nome *")
        latv = st.number_input("Latitude *")
        long  = st.number_input("Longitude *")
        country = st.text_input("País *")
        state = st.text_input("Estado *")
        city = st.text_input("Cidade *")
        props = st.text_area("Propriedades (JSON)", value='')
        submitted = st.form_submit_button("Inserir")
        if submitted:
            if(not name or not latv or not long or not country or not state or not city):
                st.error("Preencha todos os campos obriatórios para cadastrar um novo ponto.")
            else:
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
                    "properties": props_dict,
                    "geometry": {"type":"Point", "coordinates":[long, latv]},
                    "city": city,
                    "state": state,
                    "country": country
                }
                API.create_location(body)

                st.session_state.expander_open = False

with st.expander("Consulta Integrada", expanded= st.session_state.expander_open):
    st.write("Filtre para visualizar os pontos no mapa.")

    country_data = API.get_countries()
    select_country = st.multiselect("País", options=country_data, format_func=lambda x:x['name'])

    country_ids = [country['id'] for country in select_country] if select_country else []
    state_options = API.get_states(country_ids) if country_ids else []
    select_state = st.multiselect("Estado", options=state_options, format_func=lambda x:x['name'])

    state_ids = [state['id'] for state in select_state] if select_state else []
    city_options = API.get_cities(state_ids) if state_ids else []
    select_city = st.multiselect("Cidade", options=city_options, format_func=lambda x:x['name'])

    if st.button(key ='button_locations_select', label="Buscar", disabled= not bool(select_country or select_state or select_city)):
        params= {
            "city": [city['name'] for city in select_city] if select_city else None,
            "state": [state['name'] for state in select_state] if select_state else None,
            "country": [country['name'] for country in select_country] if select_country else None
        }
        response= API.get_locations(params)
        if(len(response) > 0):
            points = [d for d in response if d.get("geometry",{}).get("type") == "Point"]
        
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

            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(latitude=center[0], longitude=center[1], zoom=11, pitch=0),
                layers=layers,
                tooltip={"text": "{name}\n{category}"}
            ))
    
with st.expander("Geoprocessamento", expanded= st.session_state.expander_open):
    select_location = st.selectbox(
        "Local", 
        options=location_options, 
        format_func=lambda x:x['name'], 
        index=None, 
        placeholder="Selecione um local"
    )
    search_radius = st.slider("Raio de distância(Km)", 0, 100, 10)


    if st.button(key ='button_locations_search_radius', label= "Buscar", disabled= not bool(select_location)):
        params= {
            "id": select_location['id'] if select_location else None,
            "search_radius": search_radius
        }
        response= API.get_locations_search_radius(params)
        if(len(response) > 0):
            points = [d for d in response if d.get("geometry",{}).get("type") == "Point"]
        
            center = [points[0]["geometry"]["coordinates"][1], points[0]["geometry"]["coordinates"][0]]
        
            layers = []

            if points:
                df_geo = pd.DataFrame(points)
                df_geo["lon"] = df_geo["geometry"].apply(lambda g: g["coordinates"][0])
                df_geo["lat"] = df_geo["geometry"].apply(lambda g: g["coordinates"][1])
                layers.append(pdk.Layer(
                    "ScatterplotLayer",
                    data=df_geo,
                    get_position=["lon","lat"],
                    get_radius=25,
                    pickable=True,
                    get_fill_color=[150, 0, 20, 200]  # vermelho com transparência
                ))

            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(latitude=center[0], longitude=center[1], zoom=15, pitch=0),
                layers=layers,
                tooltip={"text": "{name}"}
            ))

with st.expander("Distância entre pontos", expanded= st.session_state.expander_open):
    select_location1 = st.selectbox(
        "Local 1", 
        options=location_options, 
        format_func=lambda x:x['name'],
        index= None,
        placeholder= "Selecione o Local 1"
    )
    select_location2 = st.selectbox(
        "Local 2", 
        options=location_options, 
        format_func=lambda x:x['name'],
        index= None,
        placeholder= "Selecione o Local 1"
    )

    disabled_button_calculate_distance = True
    if(select_location1 and select_location2 and select_location1['id'] == select_location2["id"]):
        disabled_button_calculate_distance = True
        st.error("Os locais são iguais! Selecione locais diferentes para o cálculo.")
    else:
        disabled_button_calculate_distance = False

    if st.button(key ='button_calculate_distance', label= "Calcular", disabled= disabled_button_calculate_distance):
       distance = geodesic(select_location1["geometry"]["coordinates"], select_location2["geometry"]["coordinates"]).km

       st.write(f"A distância entre os pontos é de {distance:.2f}km.")