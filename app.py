import streamlit as st
import api_client as API

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



# if st.button("testee"):
#     teste = requests.get(API_URL)
#     print(teste)

    


