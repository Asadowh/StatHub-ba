from pydantic import BaseModel, ConfigDict
from datetime import datetime

class StatCreate(BaseModel):
    match_id: int
    player_id: int
    team: str = "home"  # "home" or "away"
    goals: int = 0
    assists: int = 0
    rating: float = 0.0

class StatResponse(StatCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
