from datetime import datetime
from pydantic import BaseModel
from typing import Optional 

class Post(BaseModel):
    post_uuid: str
    user_uuid: str
    title: str
    summary: Optional[str]
    tags_uuid: Optional[list[str]]
    website: Optional[str]
    location_uuid: Optional[str]
    since: Optional[str]
    image_uuid: Optional[str]
    body: str
    created_at: datetime
    updated_at: Optional[datetime]

class Reaction(BaseModel):
    post_uuid: str
    like: int
    super_like: int

class NewPost(BaseModel):
    title: str
    tags: Optional[list[str]]
    website: Optional[str]
    location: Optional[str]
    since: Optional[str]
    image: Optional[str]
    body:str

class Reactions(BaseModel):
    reactions: list[Reaction]

