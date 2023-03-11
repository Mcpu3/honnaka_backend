from datetime import datetime
import os
from typing import Optional

import pyodbc

import posts.api.v1.schema as schema


connection = pyodbc.connect()

