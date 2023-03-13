from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class Token(BaseModel):
    access_token: str


class User(BaseModel):
    user_uuid: str
    user_name: str
    display_name: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


class PrivateUser(User):
    hashed_password: str
    deleted: bool


class Signup(BaseModel):
    user_name: str
    password: str


class Password(BaseModel):
    old_password: str
    new_password: str


class DisplayName(BaseModel):
    display_name: str


class Post(BaseModel):
    post_uuid: str
    user_uuid: str
    title: str
    summary: Optional[str]
    tags_uuid: Optional[List[str]]
    website: Optional[str]
    location_uuid: Optional[str]
    since: Optional[str]
    image_uuid: Optional[str]
    body: str
    created_at: datetime
    updated_at: Optional[datetime]


class NewPost(BaseModel):
    title: str
    tags: Optional[List[str]]
    website: Optional[str]
    location: Optional[str]
    since: Optional[str]
    image: Optional[str]
    body: str


class Tag(BaseModel):
    tag_uuid: str
    body: str
    created_at: datetime
    updated_at: Optional[datetime]


class Location(BaseModel):
    location_uuid: str
    body: str
    created_at: datetime
    updated_at: Optional[datetime]


class Image(BaseModel):
    image_uuid: str
    user_uuid: str
    body: str
    created_at: datetime
    updated_at: Optional[datetime]


class Reactions(BaseModel):
    like: int
    super_like: int


class Reaction(BaseModel):
    reaction_uuid: str
    user_uuid: str
    post_uuid: str
    like: bool
    super_like: bool
    created_at: datetime
    updated_at: Optional[datetime]


class NewReaction(BaseModel):
    like: bool
    super_like: bool


class ReactedPosts(BaseModel):
    liked_posts_uuid: List[str]
    super_liked_posts_uuid: List[str]
