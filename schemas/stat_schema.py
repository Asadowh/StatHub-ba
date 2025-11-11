from pydantic import BaseModel

class StatBase(BaseModel):
    player_name: str
    match_id: int
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0

class StatCreate(StatBase):
    pass

class StatResponse(StatBase):
    id: int

    class Config:
        orm_mode = True
