from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Image(BaseModel):
    image_uuid: str
    user_uuid: str
    body: str
    created_at: str
    updated_at: Optional[str]


