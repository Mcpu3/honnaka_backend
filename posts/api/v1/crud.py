import os
from typing import List

import pyodbc

import posts.api.v1.schema as schema


connection = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:honnaka-backend.database.windows.net,1433;Database=honnaka-backend;Uid=iwamoto.keisuke629@honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % os.getenv("PASSWORD"))

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
                tags_uuid = data[4],
                website = data[5],
                location_uuid = data[6],
                since = data[7],
                image_uuid = data[8],
                body = data[9],
                created_at = data[10],
                updated_at = data[11]
            )

    return post

def read_reactions(post_uuid: str):
    reactions = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                sum(like),
                sum(super_like)
            from reactions
            where
                post_uuid ='{post_uuid}' and
                deleted = 0
        """)
        reactions = cursor.fetchone()

    return reactions

def create_post(post: schema.Post):
    post_uuid = post.post_uuid
    user_uuid = post.user_uuid
    title = post.title
    summary = post.summary
    tags_uuid = post.tags_uuid
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

def create_tags(tags: List[schema.Tag]):
    for tag in tags:
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

def read_tag(body: str) -> schema.Tag:
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

def read_location(body: str) -> schema.Location:
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
