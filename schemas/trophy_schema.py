from pydantic import BaseModel
from datetime import datetime

class TrophyBase(BaseModel):
    name: str
    description: str | None = None
    awarded_to: int

class TrophyCreate(TrophyBase):
    pass

class TrophyResponse(TrophyBase):
    id: int
    date_awarded: datetime

    class Config:
        orm_mode = True
