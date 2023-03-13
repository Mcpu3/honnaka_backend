from datetime import datetime
import os 

from fastapi import APIRouter,HTTPException,status

import tags.api.v1.crud as crud
import tags.api.v1.schema as schema


api_router = APIRouter()

@api_router.get("/tag/{tag_uuid}")
def get_tag(tag_uuid: str) -> schema.Tag:
    tag = crud.read_tag(tag_uuid)
    if not tag:
        raise HTTPException()
    
    return tag

@api_router.get("/tags/")
def get_tags(like: str) -> schema.Tags:
    tags = crud.read_tags(like)
    if len(tags) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return tags

