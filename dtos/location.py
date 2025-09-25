from pydantic import BaseModel
from typing import Literal, Any
from dtos.geometry import Geometry

class Location(BaseModel):
    name: str
    properties: dict
    city: str
    state: str
    country: str
    geometry: Geometry