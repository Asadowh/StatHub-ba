from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsBase(BaseModel):
    title: str
    content: str

class NewsCreate(NewsBase):
    category: Optional[str] = None

class NewsResponse(NewsBase):
    id: int
    author_id: int
    image_url: Optional[str] = None
    category: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
