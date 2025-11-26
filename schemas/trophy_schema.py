from pydantic import BaseModel
from datetime import datetime

class TrophyCreate(BaseModel):
    name: str
    description: str | None = None
    awarded_to: int

class TrophyResponse(TrophyCreate):
    id: int
    date_awarded: datetime

    class Config:
        orm_mode = True
