from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user

from schemas.stat_schema import StatCreate, StatResponse
from services.stat_service import create_stat, get_stats_for_match, get_user_recent_performances, get_match_players_detailed

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.post("/", response_model=StatResponse)
def create_stat_endpoint(
    data: StatCreate, 
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only admin can create stats
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create stats")
    return create_stat(db, data)

@router.get("/match/{match_id}", response_model=list[StatResponse])
def get_match_stats(match_id: int, db: Session = Depends(get_db)):
    return get_stats_for_match(db, match_id)

@router.get("/match/{match_id}/players")
def get_match_players(match_id: int, db: Session = Depends(get_db)):
    """Get all players in a match with their details, sorted by jersey number"""
    return get_match_players_detailed(db, match_id)

@router.get("/me/recent")
def get_my_recent_performances(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 3
):
    """Get current user's recent match performances"""
    return get_user_recent_performances(db, current_user.id, limit)

@router.get("/user/{user_id}/recent")
def get_user_recent_performances_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    limit: int = 3
):
    """Get a specific user's recent match performances"""
    return get_user_recent_performances(db, user_id, limit)
