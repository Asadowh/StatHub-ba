from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.leaderboard_service import (
    get_leaderboard, 
    get_user_rank,
    get_achievements_leaderboard,
    get_trophies_leaderboard,
    get_user_achievement_rank,
    get_user_trophy_rank
)
from services.stathub_ranking_service import get_stathub_ranking

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/")
def leaderboard(limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get the StatHub ranking leaderboard ranked by average StatHub rating. Includes ALL players, even with 0 rating."""
    return get_leaderboard(db, limit)


@router.get("/achievements")
def achievements_leaderboard(limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get the achievements leaderboard ranked by number of unlocked achievements. Includes ALL players, even with 0 achievements."""
    return get_achievements_leaderboard(db, limit)


@router.get("/trophies")
def trophies_leaderboard(limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get the trophies leaderboard ranked by number of trophies. Includes ALL players, even with 0 trophies."""
    return get_trophies_leaderboard(db, limit)


@router.get("/user/{user_id}")
def user_rank(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user's rank on the StatHub ranking leaderboard"""
    result = get_user_rank(db, user_id)
    if not result:
        return {"error": "User not found or has no stats"}
    return result


@router.get("/achievements/user/{user_id}")
def user_achievement_rank(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user's rank on the achievements leaderboard"""
    result = get_user_achievement_rank(db, user_id)
    if not result:
        return {"error": "User not found or has no achievements"}
    return result


@router.get("/trophies/user/{user_id}")
def user_trophy_rank(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user's rank on the trophies leaderboard"""
    result = get_user_trophy_rank(db, user_id)
    if not result:
        return {"error": "User not found or has no trophies"}
    return result


@router.get("/stathub-ranking")
def stathub_ranking(
    sort_by: str = Query("rating", regex="^(rating|goals|assists|combined)$"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get StatHub ranking sorted by rating, goals, assists, or combined (goals+assists)"""
    return get_stathub_ranking(db, sort_by, limit)
