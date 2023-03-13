from datetime import datetime
import os
from typing import Optional

import pyodbc

import tags.api.v1.schema as schema


connection = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:honnaka-backend.database.windows.net,1433;Database=honnaka-backend;Uid=iwamoto.keisuke629@honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % os.getenv("PASSWORD"))

def read_tag(tag_uuid: str):
    tag = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
        select
            tag_uuid,
            body,
            created_at

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
                created_at = data[2]
            )
    return tag

def read_tags(like: str):
    tags = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                tag_uuid
            from tags
            where body = '%{like}%' and
            deleted = 0
        """)

        tags = cursor.fetchall()

        return tags

