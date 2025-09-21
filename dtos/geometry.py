from pydantic import BaseModel
from typing import Literal, Any

class Geometry(BaseModel):
    type: Literal["Point","LineString","Polygon"]
    coordinates: Any