from sqlalchemy import create_engine
from sqlite.tables import metadata
import streamlit as st
import os

DB_FILE = "locations.db"

@st.cache_resource
def get_sqlite_engine():
    """
    Cria e retorna uma engine de conexão com o banco de dados SQLite.
    """
    try:
        first_time = not os.path.exists(DB_FILE)

        engine = create_engine(f"sqlite:///{DB_FILE}")

        if first_time:
            metadata.create_all(engine)

        return engine
    except Exception as e:
        return None