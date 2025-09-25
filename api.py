from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
import sqlite.query as sqlite_querys 
import mongo.query as mongo_querys 
from typing import Optional, List
from dtos.location import Location

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/countries")
def get_countries():
    result= sqlite_querys.get_countries()
    return [{"id": row.id, "name": row.name} for row in result]

@app.get("/states")
def get_states(countries: list[int] = Query(...)):
    result= sqlite_querys.get_states(countries)
    return [{"id": row.id, "name": row.name} for row in result]

@app.get("/cities")
def get_cities(states: list[int] = Query(...)):
    result= sqlite_querys.get_cities(states)
    return [{"id": row.id, "name": row.name} for row in result]

@app.get("/locations")
def get_locations(
    city: Optional[List[str]] = Query(None),
    state: Optional[List[str]] = Query(None),
    country: Optional[List[str]] = Query(None),
    id: Optional[str] = Query(None),
    limit: Optional[int] = 100
):
    params = {
        "city": city, 
        "state": state, 
        "country": country,
        "id": id, 
        "limit": limit
    }
    result= mongo_querys.get_locations(params)
    return result

@app.get("/locations/search-radius")
def get_locations(
    id: str,
    search_radius: int 
):
    response= mongo_querys.get_locations_by_search_radius(id, search_radius)
    return response

@app.post("/location")
def get_locations(location: Location):
    try:
        mongo_querys.create_location(location)
        sqlite_querys.create(location.city, location.state, location.country)
    except Exception as e:
        raise