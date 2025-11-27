from pydantic import BaseModel
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    content: str

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
