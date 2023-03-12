from datetime import datetime
import os
from typing import Optional

import pyodbc

import posts.api.v1.schema as schema


connection = pyodbc.connect()

def read_post(post_uuid: str):
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
                post_uuid,
                sum(like),
                sum(superlike)
            from reactions
            where post_uuid ='{post_uuid}' and
            deleted = 0
        """)

        reactions = cursor.fetchone()

        return reactions
    
    def create_new_post(post: schema.NewPost,user: schema.User):
        post_uuid = a                   #多分自動生成なのかな？
        user_uuid = user.user_uuid
        title = post.title
        summary = b                     #ここは結局どうする？
        tags_uuid = c                   #ここはタグのDBから検索する形？
        website = post.website
        location_uuid = d               #タグと同様
        since = post.since
        image_uuid = e                  #タグと同様
        body = post.body
        created_at =post.created_at.strftime("%Y-%m-%d %H:%M:%S")
        deleted = 0

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
                values(
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
                    '{deleted}'
                )
            """)

