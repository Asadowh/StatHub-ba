from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.rating_schema import RatingCreate, RatingResponse
from services.rating_service import create_rating, get_player_ratings

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse)
def rate_player(data: RatingCreate, db: Session = Depends(get_db)):
    if not 0 <= data.rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be 0–10.")
    return create_rating(db, data)

@router.get("/player/{player_id}", response_model=list[RatingResponse])
def get_ratings(player_id: int, db: Session = Depends(get_db)):
    return get_player_ratings(db, player_id)
