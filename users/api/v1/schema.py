from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str


class PublicUser(BaseModel):
    user_name: str
    display_name: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


class User(PublicUser):
    user_uuid: str
    hashed_password: str
    deleted: bool


class SignUp(BaseModel):
    user_name: str
    password: str


class Password(BaseModel):
    old_password: str
    new_password: str


class DisplayName(BaseModel):
    display_name: str
