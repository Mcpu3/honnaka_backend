from datetime import datetime
import os
import random
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import posts.api.v1.crud as crud
import posts.api.v1.schema as schema


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
        tag = crud.read_tag(body)
        if not tag:
            tag = schema.Tag(
                tag_uuid = uuid4(),
                body = body,
                created_at = datetime.now()
            )
    location = crud.read_location(request_body.location)
    if not location:
        location = schema.Location(
            location_uuid = uuid4(),
            body = request_body.location,
            created_at = datetime.now()
        )
        crud.create_location(location)
    image = schema.Image(
        image_uuid = uuid4(),
        user_uuid = current_user.user_uuid,
        body = request_body.image,
        created_at = datetime.now()
    )
    crud.create_image(image)
    post = schema.Post(
        post_uuid = uuid4(),
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
