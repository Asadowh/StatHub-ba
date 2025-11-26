from pydantic import BaseModel
from datetime import datetime

class MatchCreate(BaseModel):
    home_team: str
    away_team: str
    location: str
    match_date: datetime

class MatchResponse(BaseModel):
    id: int
    home_team: str
    away_team: str
    location: str
    match_date: datetime
    winner_team: str | None

    class Config:
        orm_mode = True
