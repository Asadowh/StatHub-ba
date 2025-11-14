from pydantic import BaseModel

class RatingBase(BaseModel):
    player_name: str
    match_id: int
    voter_id: int
    rating: float  # 0–10

class RatingCreate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int

    class Config:
        orm_mode = True