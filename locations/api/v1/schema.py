from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    location_uuid: str
    body: str
    created_at: str
    updated_at: Optional[str]

class Locations(BaseModel):
    locations_uuid: list[str]