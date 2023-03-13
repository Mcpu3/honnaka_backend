from datetime import datetime
import os 

from fastapi import APIRouter,HTTPException,status

import images.api.v1.crud as crud
import images.api.v1.schema as schema


api_router = APIRouter()

@api_router.get("/image/{image_uuid}")
def get_image(image_uuid: str) -> schema.Image:
    image = crud.read_image(image_uuid)
    if not image:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return image


