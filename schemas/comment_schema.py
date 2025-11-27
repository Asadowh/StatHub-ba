from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    news_id: int | None = None
    match_id: int | None = None

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
