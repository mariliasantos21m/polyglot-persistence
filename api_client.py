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

def create_location(body):
    try:
        response = requests.post(f"{API_URL}/location", json=body)
        response.raise_for_status()
        st.success("Registro inserido com sucesso! Clique em Recarregar dados.")
    except requests.RequestException as e:
        st.error(f"Erro ao salvar local: {e}")
        return 
    
def get_locations_search_radius(params):
    try:
        response = requests.get(f"{API_URL}/locations/search-radius", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar locais por raio de distância: {e}")
        return []