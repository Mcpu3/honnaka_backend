from datetime import datetime
import json
import os
from typing import List, Optional

import pyodbc

import honnaka_backend.api.v1.schema as schema


connection = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:honnaka-backend.database.windows.net,1433;Database=honnaka-backend;Uid=iwamoto.keisuke629@honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % os.getenv("PASSWORD"))

def create_user(user: schema.PrivateUser):
    user_uuid = user.user_uuid
    user_name = user.user_name
    hashed_password = user.hashed_password
    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    deleted = int(user.deleted)
    with connection.cursor() as cursor:
        cursor.execute(f"""
            insert into users (
                user_uuid,
                user_name,
                hashed_password,
                created_at,
                deleted
            )
            values (
                '{user_uuid}',
                '{user_name}',
                '{hashed_password}',
                '{created_at}',
                {deleted}
            )
        """)

def read_user(user_uuid: Optional[str] = None, user_name: Optional[str] = None) -> schema.PrivateUser:
    user = None

    if user_uuid:
        user = read_user_by_user_uuid(user_uuid)
    if user_name:
        user = read_user_by_user_name(user_name)

    return user

def read_user_by_user_uuid(user_uuid: str) -> schema.PrivateUser:
    user = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                user_uuid,
                user_name,
                hashed_password,
                display_name,
                created_at,
                updated_at,
                deleted
            from users
            where 
                user_uuid = '{user_uuid}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            user = schema.PrivateUser(
                user_uuid = data[0],
                user_name = data[1],
                hashed_password = data[2],
                display_name = data[3],
                created_at = data[4],
                updated_at = data[5],
                deleted = data[6]
            )

    return user

def read_user_by_user_name(user_name: str) -> schema.PrivateUser:
    user = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                user_uuid,
                user_name,
                hashed_password,
                display_name,
                created_at,
                updated_at,
                deleted
            from users
            where 
                user_name = '{user_name}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            user = schema.PrivateUser(
                user_uuid = data[0],
                user_name = data[1],
                hashed_password = data[2],
                display_name = data[3],
                created_at = data[4],
                updated_at = data[5],
                deleted = data[6]
            )

    return user

def update_hashed_password(user_uuid: str, hashed_password: str, updated_at: datetime):
    updated_at = updated_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update users
            set
                hashed_password = '{hashed_password}',
                updated_at = '{updated_at}'
            where
                user_uuid = '{user_uuid}' and
                deleted = 0
        """)

def update_display_name(user_uuid: str, display_name: str, updated_at: datetime):
    updated_at = updated_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update users
            set
                display_name = '{display_name}',
                updated_at = '{updated_at}'
            where
                user_uuid = '{user_uuid}' and
                deleted = 0
        """)

def create_post(post: schema.Post):
    post_uuid = post.post_uuid
    user_uuid = post.user_uuid
    title = post.title
    summary = post.summary
    tags_uuid = json.dumps(post.tags_uuid)
    website = post.website
    location_uuid = post.location_uuid
    since = post.since
    image_uuid = post.image_uuid
    body = post.body
    created_at = post.created_at.strftime("%Y-%m-%d %H:%M:%S")

    with connection.cursor() as cursor:
        cursor.execute(f"""
            insert into posts(
                post_uuid,
                user_uuid,
                title,
                summary,
                tags_uuid,
                website,
                location_uuid,
                since,
                image_uuid,
                body,
                created_at,
                deleted
            )
            values (
                '{post_uuid}',
                '{user_uuid}',
                '{title}',
                '{summary}',
                '{tags_uuid}',
                '{website}',
                '{location_uuid}',
                '{since}',
                '{image_uuid}',
                '{body}',
                '{created_at}',
                0
            )
        """)

def read_post(post_uuid: str) -> schema.Post:
    post = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                post_uuid,
                user_uuid,
                title,
                summary,
                tags_uuid,
                website,
                location_uuid,
                since,
                image_uuid,
                body,
                created_at,
                updated_at
            from posts
            where
                post_uuid = '{post_uuid}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            post = schema.Post(
                post_uuid = data[0],
                user_uuid = data[1],
                title = data[2],
                summary = data[3],
                tags_uuid = json.loads(data[4]),
                website = data[5],
                location_uuid = data[6],
                since = data[7],
                image_uuid = data[8],
                body = data[9],
                created_at = data[10],
                updated_at = data[11]
            )

    return post

def read_posts() -> List[schema.Post]:
    posts = []

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                post_uuid,
                user_uuid,
                title,
                summary,
                tags_uuid,
                website,
                location_uuid,
                since,
                image_uuid,
                body,
                created_at,
                updated_at
            from posts
            where
                deleted = 0
        """)
        data = cursor.fetchall()
        for element_of_data in data:
            post = schema.Post(
                post_uuid = element_of_data[0],
                user_uuid = element_of_data[1],
                title = element_of_data[2],
                summary = element_of_data[3],
                tags_uuid = json.loads(element_of_data[4]),
                website = element_of_data[5],
                location_uuid = element_of_data[6],
                since = element_of_data[7],
                image_uuid = element_of_data[8],
                body = element_of_data[9],
                created_at = element_of_data[10],
                updated_at = element_of_data[11]
            )
            posts.append(post)

    return posts

def create_tag(tag: schema.Tag):
    tag_uuid = tag.tag_uuid
    body = tag.body
    created_at = tag.created_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            insert into tags (
                tag_uuid,
                body,
                created_at,
                deleted
            )
            values (
                '{tag_uuid}',
                '{body}',
                '{created_at}',
                0
            )
        """)

def read_tag(tag_uuid: Optional[str] = None, body: Optional[str] = None) -> schema.Tag:
    tag = None

    if tag_uuid:
        tag = read_tag_by_tag_uuid(tag_uuid)
    if body:
        tag = read_tag_by_body(body)

    return tag

def read_tag_by_tag_uuid(tag_uuid: str) -> schema.Tag:
    tag = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                tag_uuid,
                body,
                created_at,
                updated_at
            from tags
            where
                tag_uuid = '{tag_uuid}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            tag = schema.Tag(
                tag_uuid = data[0],
                body = data[1],
                created_at = data[2],
                updated_at = data[3]
            )

    return tag

def read_tag_by_body(body: str) -> schema.Tag:
    tag = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                tag_uuid,
                body,
                created_at,
                updated_at
            from tags
            where
                body = '{body}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            tag = schema.Tag(
                tag_uuid = data[0],
                body = data[1],
                created_at = data[2],
                updated_at = data[3]
            )

    return tag

def read_tags(like: str):
    tags = []

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                tag_uuid,
                body,
                created_at,
                updated_at
            from tags
            where
                body like '%{like}%' and
                deleted = 0
        """)
        data = cursor.fetchall()
        for element_of_data in data:
            tag = schema.Tag(
                tag_uuid = element_of_data[0],
                body = element_of_data[1],
                created_at = element_of_data[2],
                updated_at = element_of_data[3]
            )
            tags.append(tag)

    return tags

def create_location(location: schema.Location):
    location_uuid = location.location_uuid
    body = location.body
    created_at = location.created_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            insert into locations (
                location_uuid,
                body,
                created_at,
                deleted
            )
            values (
                '{location_uuid}',
                '{body}',
                '{created_at}',
                0
            )
        """)

def read_location(location_uuid: Optional[str] = None, body: Optional[str] = None) -> schema.Location:
    location = None

    if location_uuid:
        location = read_location_by_location_uuid(location_uuid)
    if body:
        location = read_location_by_body(body)

    return location

def read_location_by_location_uuid(location_uuid: str) -> schema.Location:
    location = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                location_uuid,
                body,
                created_at,
                updated_at
            from locations
            where
                location_uuid = '{location_uuid}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            location = schema.Location(
                location_uuid = data[0],
                body = data[1],
                created_at = data[2],
                updated_at = data[3]
            )

    return location

def read_location_by_body(body: str) -> schema.Location:
    location = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                location_uuid,
                body,
                created_at,
                updated_at
            from locations
            where
                body = '{body}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            location = schema.Location(
                location_uuid = data[0],
                body = data[1],
                created_at = data[2],
                updated_at = data[3]
            )

    return location

def read_locations(like: str) -> List[schema.Location]:
    locations = []

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                location_uuid,
                body,
                created_at,
                updated_at
            from locations
            where
                body like '%{like}%' and
                deleted = 0
        """)
        data = cursor.fetchall()
        for element_of_data in data:
            location = schema.Location(
                location_uuid = element_of_data[0],
                body = element_of_data[1],
                created_at = element_of_data[2],
                updated_at = element_of_data[3]
            )
            locations.append(location)

    return locations

def create_image(image: schema.Image):
    image_uuid = image.image_uuid
    user_uuid = image.user_uuid
    body = image.body
    created_at = image.created_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            insert into images (
                image_uuid,
                user_uuid,
                body,
                created_at,
                deleted
            )
            values (
                '{image_uuid}',
                '{user_uuid}',
                '{body}',
                '{created_at}',
                0
            )
        """)

def read_reactions(post_uuid: str):
    reactions = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                sum(cast(normal_like as int)),
                sum(cast(super_like as int))
            from reactions
            where
                post_uuid = '{post_uuid}' and
                deleted = 0
        """)
        reactions = cursor.fetchone()

    return reactions

def create_reaction(reaction: schema.NewReaction):
    reaction_uuid = reaction.reaction_uuid
    post_uuid = reaction.post_uuid
    user_uuid = reaction.user_uuid
    like = reaction.like
    super_like = reaction.super_like
    created_at = reaction.created_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            insert into reactions (
                reaction_uuid,
                post_uuid,
                user_uuid,
                like,
                super_like,
                created_at,
                deleted
            )
            values (
                '{reaction_uuid}',
                '{post_uuid}',
                '{user_uuid}',
                '{like}',
                '{super_like}',
                '{created_at}',
                0
            )
        """)

def read_reactioned_posts(user_uuid: str):
    liked_posts = []
    super_liked_posts = []

    with connection.cursor() as cursor:
        cursor.execute(f""""
            select 
                post_uuid
            where
                user_uuid = '{user_uuid}' and
                like = True
        """)
        liked_posts = cursor.fetchall()
        cursor.execute_(f"""
            select
                post_uuid
            where
                user_uuid = '{user_uuid}' and
                super_like = True
        """)
        super_liked_posts = cursor.fetchall()

    reactioned_posts = schema.ReactionedPosts(
        liked_posts_uuid = liked_posts,
        super_liked_posts_uuid = super_liked_posts
    )

    return reactioned_posts

def read_reactioned_post(post_uuid: str,user_uuid: str):
    reactioned_post = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                post_uuid,
                like,
                super_like,
                created_at,
                updated_at
            where
                user_uuid = '{user_uuid}' and
                post_uuid = '{post_uuid}' 
            """)
        reactioned_post = cursor.fetchone()
    
    return reactioned_post



