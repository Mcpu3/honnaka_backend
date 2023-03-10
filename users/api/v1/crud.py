from datetime import datetime
import os
from typing import Optional

import pyodbc

import users.api.v1.schema as schema


connection = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:honnaka-backend.database.windows.net,1433;Database=honnaka-backend;Uid=iwamoto.keisuke629@honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % os.getenv("PASSWORD"))

def create_user(user: schema.User):
    user_uuid = user.user_uuid
    user_name = user.user_name
    hashed_password = user.hashed_password
    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    deleted = 0
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

def read_user(user_uuid: Optional[str] = None, user_name: Optional[str] = None) -> schema.User:
    user = None

    if user_uuid:
        user = read_user_by_user_uuid(user_uuid)
    if user_name:
        user = read_user_by_user_name(user_name)

    return user

def read_user_by_user_uuid(user_uuid: str) -> schema.User:
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
            user = schema.User(
                user_uuid = data[0],
                user_name = data[1],
                hashed_password = data[2],
                display_name = data[3],
                created_at = data[4],
                updated_at = data[5],
                deleted = data[6]
            )

    return user

def read_user_by_user_name(user_name: str) -> schema.User:
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
            user = schema.User(
                user_uuid = data[0],
                user_name = data[1],
                hashed_password = data[2],
                display_name = data[3],
                created_at = data[4],
                updated_at = data[5],
                deleted = data[6]
            )

    return user

def update_hashed_password(user_name: str, hashed_password: str, updated_at: datetime):
    updated_at = updated_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update users
            set
                hashed_password = '{hashed_password}',
                updated_at = '{updated_at}'
            where
                user_name = '{user_name}' and
                deleted = 0
        """)

def update_display_name(user_name: str, display_name: str, updated_at: datetime):
    updated_at = updated_at.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update users
            set
                display_name = '{display_name}',
                updated_at = '{updated_at}'
            where
                user_name = '{user_name}' and
                deleted = 0
        """)
