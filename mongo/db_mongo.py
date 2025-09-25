import os
from dotenv import load_dotenv
from pymongo import MongoClient
import streamlit as st


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

@st.cache_resource
def getMongoConnection():
    """
    Estabelece e retorna uma conexão com o MongoDB.
    """
    try:
        client = MongoClient(MONGO_URI)
        # O comando server_info() irá gerar uma exceção se a conexão falhar
        client.server_info()

        #se esse banco de dados não existir ele será criado no momento de inserção do dado
        db = client['geo_app']
        locations = db["locations"]
        locations.create_index([("geometry", "2dsphere")])

        return db
    except Exception as e:
        return None