from datetime import datetime
import os
from typing import Optional

import pyodbc

import locations.api.v1.schema as schema


connection = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:honnaka-backend.database.windows.net,1433;Database=honnaka-backend;Uid=iwamoto.keisuke629@honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % os.getenv("PASSWORD"))

def read_location(location_uuid: str):
    location = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
        select
            location_uuid,
            body,
            created_at

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
                created_at = data[2]
            )
    return location

def read_locations(like: str):
    locations = None

    with connection.cursor() as cursor:
        cursor.execute(f"""
            select
                location_uuid
            from locations
            where body = '%{like}%' and
            deleted = 0
        """)

        locations = cursor.fetchall()

        return locations