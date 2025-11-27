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

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/")
def leaderboard(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get the StatHub ranking leaderboard ranked by XP (from achievements)"""
    return get_leaderboard(db, limit)


@router.get("/achievements")
def achievements_leaderboard(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get the achievements leaderboard ranked by number of unlocked achievements"""
    return get_achievements_leaderboard(db, limit)


@router.get("/trophies")
def trophies_leaderboard(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get the trophies leaderboard ranked by number of trophies"""
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
