from datetime import datetime
import os

from fastapi import APIRouter,HTTPException,status

import locations.api.v1.crud as crud
import locations.api.v1.schema as schema


api_router = APIRouter()

@api_router.get("/location/{location_uuid}")
def get_location(location_uuid: str) -> schema.Location:
    location = crud.read_location(location_uuid)
    if not location:
        raise HTTPException()
    
    return location

@api_router.get("/locations/")
def get_locations(like: str) -> schema.Locations:
    locations = crud.read_locations(like)
    if len(locations) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return locations