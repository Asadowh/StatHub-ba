from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.rating import Rating
from schemas.rating_schema import RatingCreate, RatingResponse
from typing import List

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)

# -------------------------------
# Create a rating
# -------------------------------
@router.post("/", response_model=RatingResponse)
def create_rating(request: RatingCreate, db: Session = Depends(get_db)):

    if request.rating < 0 or request.rating > 10:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 0 and 10."
        )

    new_rating = Rating(
        player_name=request.player_name,
        match_id=request.match_id,
        voter_id=request.voter_id,
        rating=request.rating
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating


# -------------------------------
# Get all ratings for a player
# -------------------------------
@router.get("/player/{player_name}", response_model=List[RatingResponse])
def get_player_ratings(player_name: str, db: Session = Depends(get_db)):
    return db.query(Rating).filter(Rating.player_name == player_name).all()


# -------------------------------
# Get average rating for a player (PROFILE PAGE)
# -------------------------------
@router.get("/average/{player_name}")
def get_player_average(player_name: str, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.player_name == player_name).all()

    if not ratings:
        return {"player_name": player_name, "average_rating": 0.0}

    avg_rating = sum(r.rating for r in ratings) / len(ratings)

    return {
        "player_name": player_name,
        "average_rating": round(avg_rating, 2)
    }


# -------------------------------
# Get ratings for a match
# -------------------------------
@router.get("/match/{match_id}", response_model=List[RatingResponse])
def get_match_ratings(match_id: int, db: Session = Depends(get_db)):
    return db.query(Rating).filter(Rating.match_id == match_id).all()


# -------------------------------
# Get average rating for a player in a specific match
# -------------------------------
@router.get("/player/{player_name}/match/{match_id}")
def get_player_match_rating(player_name: str, match_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(
        Rating.player_name == player_name,
        Rating.match_id == match_id
    ).all()

    if not ratings:
        return {"player_name": player_name, "match_id": match_id, "average_rating": 0.0}

    avg_rating = sum(r.rating for r in ratings) / len(ratings)

    return {
        "player_name": player_name,
        "match_id": match_id,
        "average_rating": round(avg_rating, 2)
    }