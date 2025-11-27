from pydantic import BaseModel
from datetime import datetime

class ReactionCreate(BaseModel):
    type: str
    news_id: int | None = None
    comment_id: int | None = None
    match_id: int | None = None

class ReactionResponse(ReactionCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
