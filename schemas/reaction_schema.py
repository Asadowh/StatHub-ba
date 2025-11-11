from pydantic import BaseModel
from datetime import datetime

class ReactionBase(BaseModel):
    type: str
    user_id: int
    news_id: int | None = None
    comment_id: int | None = None
    match_id: int | None = None

class ReactionCreate(ReactionBase):
    pass

class ReactionResponse(ReactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
