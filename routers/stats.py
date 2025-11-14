from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.stat import Stat
from schemas.stat_schema import StatCreate, StatResponse
from typing import List

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

# Create a stat record
@router.post("/", response_model=StatResponse)
def create_stat(request: StatCreate, db: Session = Depends(get_db)):
    new_stat = Stat(
        player_name=request.player_name,
        match_id=request.match_id,
        goals=request.goals,
        assists=request.assists,
    )
    db.add(new_stat)
    db.commit()
    db.refresh(new_stat)
    return new_stat


# Get all stats
@router.get("/", response_model=List[StatResponse])
def get_all_stats(db: Session = Depends(get_db)):
    return db.query(Stat).all()