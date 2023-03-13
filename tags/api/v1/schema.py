from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Tag(BaseModel):
    tag_uuid: str
    body: str
    created_at: str
    updated_at: Optional[str]

class Tags(BaseModel):
    tagas_uuid: list[str] 

class NewTag(BaseModel):
    body: str
    created_at: str