from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.trophy import Trophy
from schemas.trophy_schema import TrophyCreate, TrophyResponse
from typing import List

router = APIRouter(
    prefix="/trophies",
    tags=["Trophies"]
)

# Create a trophy
@router.post("/", response_model=TrophyResponse)
def create_trophy(request: TrophyCreate, db: Session = Depends(get_db)):
    new_trophy = Trophy(
        name=request.name,
        description=request.description,
        awarded_to=request.awarded_to
    )
    db.add(new_trophy)
    db.commit()
    db.refresh(new_trophy)
    return new_trophy


# Get all trophies
@router.get("/", response_model=List[TrophyResponse])
def get_all_trophies(db: Session = Depends(get_db)):
    return db.query(Trophy).all()


# Get trophies by user
@router.get("/user/{user_id}", response_model=List[TrophyResponse])
def get_user_trophies(user_id: int, db: Session = Depends(get_db)):
    trophies = db.query(Trophy).filter(Trophy.awarded_to == user_id).all()
    if not trophies:
        raise HTTPException(status_code=404, detail="No trophies found for this user.")
    return trophies
