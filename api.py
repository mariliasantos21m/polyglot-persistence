from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlite.seed_data import run_seeders
from sqlite.query import get_countries as get_countries_query
from sqlite.query import get_states as get_states_query
from sqlite.query import get_cities as get_cities_query

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
run_seeders()

@app.get("/countries")
def get_countries():
    result= get_countries_query()
    return [{"id": row.id, "name": row.name} for row in result]

@app.get("/states")
def get_states():
    result= get_states_query()
    return [{"id": row.id, "name": row.name} for row in result]

@app.get("/cities")
def get_cities():
    result= get_cities_query()
    return [{"id": row.id, "name": row.name} for row in result]