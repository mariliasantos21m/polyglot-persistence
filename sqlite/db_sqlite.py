from sqlalchemy import create_engine, MetaData
import streamlit as st

@st.cache_resource
def get_sqlite_engine():
    """
    Cria e retorna uma engine de conexão com o banco de dados SQLite.
    """
    try:
        engine = create_engine("sqlite:///locations.db")
        return engine
    except Exception as e:
        print(f"Erro ao conectar com o SQLite: {e}")
        return None
    
metadata = MetaData()