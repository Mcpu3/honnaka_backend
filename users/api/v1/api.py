from datetime import datetime
import os
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import users.api.v1.crud as crud
import users.api.v1.schema as schema


api_router = APIRouter()

def get_current_user(token: str = Depends(OAuth2PasswordBearer("/api/v1/signin"))) -> schema.User:
    try:
        data = jwt.decode(token, os.getenv("SECRET_KEY"), "HS256")
        user_name = data.get("sub")
        if not user_name:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = crud.read_user(user_name = user_name)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user

@api_router.post("/signup")
def signup(request_body: schema.SignUp):
    user_name = request_body.username
    password = request_body.password
    if (not user_name) or (not password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = schema.User(
        user_uuid = uuid4(),
        user_name = user_name,
        hashed_password = CryptContext(["bcrypt"]).hash(password),
        created_at = datetime.now()
    )
    crud.create_user(user)

    return status.HTTP_201_CREATED

@api_router.post("/signin", response_model = schema.Token)
def signin(request_body: OAuth2PasswordRequestForm = Depends()) -> schema.Token:
    user_name = request_body.username
    password = request_body.password
    if (not user_name) or (not password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = crud.read_user(user_name = user_name)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    hashed_password = user.hashed_password
    if not CryptContext(["bcrypt"]).verify(password, hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    token = schema.Token(
        access_token = jwt.encode({"sub": user_name}, os.getenv("SECRET_KEY"), "HS256"),
    )

    return token

@api_router.get("/user", response_model = schema.PublicUser)
def get_user(current_user: schema.User = Depends(get_current_user)) -> schema.PublicUser:
    user = crud.read_user_by_user_name(current_user.user_name)
    if not user:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return user

@api_router.post("/user/update_password")
def update_password(request_body: schema.Password, current_user: schema.User = Depends(get_current_user)):
    old_password = request_body.old_password
    new_password = request_body.new_password
    if (not old_password) or (not new_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    if not CryptContext(["bcrypt"]).verify(old_password, current_user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    hashed_password = CryptContext(["bcrypt"]).hash(new_password)
    updated_at = datetime.now()
    crud.update_hashed_password(current_user.user_name, hashed_password, updated_at)

    return status.HTTP_201_CREATED

@api_router.post("/user/update_display_name")
def update_display_name(request_body: schema.DisplayName, current_user: schema.User = Depends(get_current_user)):
    display_name = request_body.display_name
    if not display_name:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    updated_at = datetime.now()
    crud.update_display_name(current_user.user_name, display_name, updated_at)

    return status.HTTP_201_CREATED

@api_router.get("/user/{user_uuid}", response_model = schema.PublicUser)
def get_user(user_uuid: str) -> schema.PublicUser:
    user = crud.read_user_by_user_uuid(user_uuid)
    if not user:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return user
