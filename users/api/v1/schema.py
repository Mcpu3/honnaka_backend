from datetime import datetime
from pydantic import BaseModel
from typing import Optional


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
