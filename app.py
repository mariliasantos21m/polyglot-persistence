import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")

country_options = []
state_options = []
city_options = []


st.set_page_config(page_title="Geo Dashboard", layout="wide")
st.title("GeoJSON Dashboard com MongoDB")

st.sidebar.header("Filtros")
country = st.sidebar.multiselect("País", options=country_options, default=[])
state = st.sidebar.multiselect("Estado", options=state_options, default=[])
city = st.sidebar.multiselect("Cidade", options=city_options, default=[])

if st.button("testee"):
    teste = requests.get(API_URL)
    print(teste)


