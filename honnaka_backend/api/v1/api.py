from datetime import datetime
import os
import random
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import honnaka_backend.api.v1.crud as crud
import honnaka_backend.api.v1.schema as schema


api_router = APIRouter()

def get_current_user(token: str = Depends(OAuth2PasswordBearer("/api/v1/signin"))) -> schema.PrivateUser:
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
def signup(request_body: schema.Signup):
    user_name = request_body.user_name
    password = request_body.password
    if (not user_name) or (not password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = schema.PrivateUser(
        user_uuid = str(uuid4()),
        user_name = user_name,
        hashed_password = CryptContext(["bcrypt"]).hash(password),
        created_at = datetime.now(),
        deleted = False
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

@api_router.get("/user", response_model = schema.User)
def get_user(current_user: schema.PrivateUser = Depends(get_current_user)) -> schema.User:
    user = schema.User(
        user_uuid = current_user.user_uuid,
        user_name = current_user.user_name,
        display_name = current_user.display_name,
        created_at = current_user.created_at,
        updated_at = current_user.updated_at
    )

    return user

@api_router.post("/user/update_password")
def update_password(request_body: schema.Password, current_user: schema.PrivateUser = Depends(get_current_user)):
    old_password = request_body.old_password
    new_password = request_body.new_password
    if (not old_password) or (not new_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    if not CryptContext(["bcrypt"]).verify(old_password, current_user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    hashed_password = CryptContext(["bcrypt"]).hash(new_password)
    updated_at = datetime.now()
    crud.update_hashed_password(current_user.user_uuid, hashed_password, updated_at)

    return status.HTTP_201_CREATED

@api_router.post("/user/update_display_name")
def update_display_name(request_body: schema.DisplayName, current_user: schema.PrivateUser = Depends(get_current_user)):
    display_name = request_body.display_name
    if not display_name:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    updated_at = datetime.now()
    crud.update_display_name(current_user.user_uuid, display_name, updated_at)

    return status.HTTP_201_CREATED

@api_router.get("/user/{user_uuid}", response_model = schema.User)
def get_user(user_uuid: str) -> schema.User:
    user = crud.read_user_by_user_uuid(user_uuid)
    if not user:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return user

@api_router.get("/post", response_model = schema.Post)
def get_post() -> schema.Post:
    posts = crud.read_posts()
    if len(posts) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    post = random.choice(posts)

    return post

@api_router.get("/post/{post_uuid}", response_model = schema.Post)
def get_post(post_uuid: str) -> schema.Post:
    post = crud.read_post(post_uuid)
    if not post:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return post

@api_router.post("/post")
def post_new_post(request_body: schema.NewPost, current_user: schema.PrivateUser = Depends(get_current_user)):
    summary = "summary"
    tags_uuid = []
    for body in request_body.tags:
        tag = crud.read_tag(body = body)
        if not tag:
            tag = schema.Tag(
                tag_uuid = str(uuid4()),
                body = body,
                created_at = datetime.now()
            )
            crud.create_tag(tag)
        tags_uuid.append(tag.tag_uuid)
    location = crud.read_location(request_body.location)
    if not location:
        location = schema.Location(
            location_uuid = str(uuid4()),
            body = request_body.location,
            created_at = datetime.now()
        )
        crud.create_location(location)
    image = schema.Image(
        image_uuid = str(uuid4()),
        user_uuid = current_user.user_uuid,
        body = request_body.image,
        created_at = datetime.now()
    )
    crud.create_image(image)
    post = schema.Post(
        post_uuid = str(uuid4()),
        user_uuid = current_user.user_uuid,
        title = request_body.title,
        summary = summary,
        tags_uuid = tags_uuid,
        website = request_body.website,
        location_uuid = location.location_uuid,
        since = request_body.since,
        image_uuid = image.image_uuid,
        body = request_body.body,
        created_at = datetime.now()
    )
    crud.create_post(post)

    return status.HTTP_201_CREATED

@api_router.get("/post/{post_uuid}/reactions")
def get_reactions(post_uuid: str) -> schema.Reaction:
    reactions = crud.read_reactions(post_uuid)

    return reactions

@api_router.get("/tags", response_model = List[schema.Tag])
def get_tags(like: str) -> List[schema.Tag]:
    if not like:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    tags = crud.read_tags(like)
    if len(tags) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return tags

@api_router.get("/tag/{tag_uuid}", response_model = schema.Tag)
def get_tag(tag_uuid: str) -> schema.Tag:
    tag = crud.read_tag(tag_uuid = tag_uuid)
    if not tag:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return tag

@api_router.get("/locations", response_model = List[schema.Location])
def get_locations(like: str) -> List[schema.Location]:
    locations = crud.read_locations(like)
    if len(locations) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return locations

@api_router.get("/location/{location_uuid}", response_model = schema.Location)
def get_location(location_uuid: str) -> schema.Location:
    location = crud.read_location(location_uuid = location_uuid)
    if not location:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return location

@api_router.get("/image/{image_uuid}", response_model = schema.Image)
def get_image(image_uuid: str) -> schema.Image:
    image = crud.read_image(image_uuid)
    if not image:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return image
