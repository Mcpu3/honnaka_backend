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
                0
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

def delete_user(user_uuid: str):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update users
            set
                deleted = 1
            where
                user_uuid = '{user_uuid}' and
                deleted = 0
        """)

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

def read_posts_by_user_uuid(user_uuid: str) -> schema.Posts:
    posts_uuid = []

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                post_uuid
            from posts
            where
                user_uuid = '{user_uuid}' and
                deleted = 0
        """)
        data = cursor.fetchall()
        for element_of_data in data:
            post_uuid = element_of_data[0]
            posts_uuid.append(post_uuid)
    posts = schema.Posts(
        posts_uuid = posts_uuid
    )

    return posts

def delete_post(post_uuid: str):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update posts
            set
                deleted = 1
            where
                post_uuid = '{post_uuid}' and
                deleted = 0
        """)

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

def read_tags(like: str) -> List[schema.Tag]:
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

def read_image(image_uuid: str) -> schema.Image:
    image = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                image_uuid,
                user_uuid,
                body,
                created_at,
                updated_at
            from images
            where
                image_uuid = '{image_uuid}' and
                deleted = 0
        """)
        data = cursor.fetchone()
        if data:
            image = schema.Image(
                image_uuid = data[0],
                user_uuid = data[1],
                body = data[2],
                created_at = data[3],
                updated_at = data[4]
            )

    return image

def read_reactions(post_uuid: str) -> schema.Reactions:
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
        data = cursor.fetchone()
        if data:
            reactions = schema.Reactions(
                like = data[0],
                super_like = data[1]
            )

    return reactions

def create_reaction(reaction: schema.Reaction):
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
                normal_like,
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

def read_reaction(reaction_uuid: Optional[str] = None, user_uuid: Optional[str] = None, post_uuid: Optional[str] = None) -> schema.Reaction:
    reaction = None

    if reaction_uuid:
        reaction = read_reaction_by_reaction_uuid(reaction_uuid)
    if user_uuid and post_uuid:
        reaction = read_reaction_by_user_uuid_and_post_uuid(user_uuid, post_uuid)

    return reaction

def read_reaction_by_reaction_uuid(reaction_uuid: str) -> schema.Reaction:
    reaction = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                reaction_uuid,
                user_uuid,
                post_uuid,
                normal_like,
                super_like,
                created_at,
                updated_at
            from reactions
            where
                reaction_uuid = '{reaction_uuid}'
            """)
        data = cursor.fetchone()
        if data:
            reaction = schema.Reaction(
                reaction_uuid = data[0],
                user_uuid = data[1],
                post_uuid = data[2],
                like = data[3],
                super_like = data[4],
                created_at = data[5],
                updated_at = data[6]
            )

    return reaction

def read_reaction_by_user_uuid_and_post_uuid(user_uuid: str, post_uuid: str) -> schema.Reaction:
    reaction = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                reaction_uuid,
                user_uuid,
                post_uuid,
                normal_like,
                super_like,
                created_at,
                updated_at
            from reactions
            where
                user_uuid = '{user_uuid}' and
                post_uuid = '{post_uuid}'
            """)
        data = cursor.fetchone()
        if data:
            reaction = schema.Reaction(
                reaction_uuid = data[0],
                user_uuid = data[1],
                post_uuid = data[2],
                like = data[3],
                super_like = data[4],
                created_at = data[5],
                updated_at = data[6]
            )
    
    return reaction

def read_reacted_posts(user_uuid: str) -> schema.ReactedPosts:
    liked_posts_uuid, super_liked_posts_uuid = [], []

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                post_uuid
            from reactions
            where
                user_uuid = '{user_uuid}' and
                normal_like = 1
        """)
        data = cursor.fetchall()
        for element_of_data in data:
            liked_post_uuid = element_of_data[0]
            liked_posts_uuid.append(liked_post_uuid)
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                post_uuid
            from reactions
            where
                user_uuid = '{user_uuid}' and
                super_like = 1
        """)
        data = cursor.fetchall()
        for element_of_data in data:
            super_liked_post_uuid = element_of_data[0]
            super_liked_posts_uuid.append(super_liked_post_uuid)
    reacted_posts = schema.ReactedPosts(
        liked_posts_uuid = liked_posts_uuid,
        super_liked_posts_uuid = super_liked_posts_uuid
    )

    return reacted_posts

def update_reaction(reaction_uuid: str, like: bool, super_like: bool, updated_at: datetime):
    like = int(like)
    super_like = int(super_like)
    updated_at = updated_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update reactions
            set
                normal_like = {like},
                super_like = {super_like},
                updated_at = '{updated_at}'
            where
                reaction_uuid = '{reaction_uuid}' and
                deleted = 0
        """)
