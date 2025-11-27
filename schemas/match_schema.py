from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MatchCreate(BaseModel):
    home_team: str
    away_team: str
    home_score: int = 0
    away_score: int = 0
    match_date: datetime

class MatchResponse(BaseModel):
    id: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    match_date: datetime
    winner_team: Optional[str]

    class Config:
        from_attributes = True
