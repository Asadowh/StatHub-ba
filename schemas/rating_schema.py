from pydantic import BaseModel
from datetime import datetime

class RatingCreate(BaseModel):
    player_id: int
    match_id: int | None = None
    rating: float
    context: str | None = None

class RatingResponse(RatingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
