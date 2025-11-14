from pydantic import BaseModel
from datetime import datetime

class MatchBase(BaseModel):
    home_team: str
    away_team: str
    location: str
    match_date: datetime | None = None
    score_home: int = 0
    score_away: int = 0

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int
    created_by: int
    class Config:
        orm_mode = True