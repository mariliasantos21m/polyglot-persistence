import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
API_URL = os.getenv("API_URL")

def get_countries():
    try:
        response = requests.get(f"{API_URL}/countries")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar países: {e}")
        return []
    
def get_states(countries:list[int]):
    try:
        params = {"countries": countries}
        response = requests.get(f"{API_URL}/states", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar estados: {e}")
        return []

def get_cities(states:list[int]):
    try:
        params = {"states": states}
        response = requests.get(f"{API_URL}/cities", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar cidades: {e}")
        return []

def get_locations(params):
    try:
        response = requests.get(f"{API_URL}/locations", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar locais: {e}")
        return []