from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.stat import Stat
from models.user import User
from models.match import Match
from schemas.stat_schema import StatCreate, StatResponse
from typing import List

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

# ------------------------------------------------
# Create a stat record
# ------------------------------------------------
@router.post("/", response_model=StatResponse)
def create_stat(request: StatCreate, db: Session = Depends(get_db)):

    # --- Check if player exists ---
    player = db.query(User).filter(User.username == request.player_name).first()
    if not player:
        raise HTTPException(
            status_code=400,
            detail=f"Player '{request.player_name}' does not exist. Cannot add stats."
        )
    
    # --- Check if match exists ---
    match = db.query(Match).filter(Match.id == request.match_id).first()
    if not match:
        raise HTTPException(
            status_code=400,
            detail=f"Match with id={request.match_id} does not exist."
        )

    # --- Create the stat ---
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


# ------------------------------------------------
# Get ALL stats
# ------------------------------------------------
@router.get("/", response_model=List[StatResponse])
def get_all_stats(db: Session = Depends(get_db)):
    return db.query(Stat).all()
