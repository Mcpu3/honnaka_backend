from datetime import datetime
import os
from typing import Optional

import pyodbc

import images.api.v1.schema as schema


connection = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:honnaka-backend.database.windows.net,1433;Database=honnaka-backend;Uid=iwamoto.keisuke629@honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % os.getenv("PASSWORD"))

def read_image(image_uuid: str):
    image = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
        select
            image_uuid,
            user_uuid,
            body,
            created_at
        from tags
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
                created_at = data[3]
            )
    return image

