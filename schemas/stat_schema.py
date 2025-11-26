from pydantic import BaseModel
from datetime import datetime

class StatCreate(BaseModel):
    match_id: int
    player_id: int
    goals: int = 0
    assists: int = 0
    rating: float = 0.0

class StatResponse(StatCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
