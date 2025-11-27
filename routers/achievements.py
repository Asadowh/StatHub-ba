from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user

from schemas.achievement_schema import AchievementCreate, AchievementResponse
from services.achievement_service import create_achievement
from models.achievement import Achievement, PlayerAchievement

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.post("/", response_model=AchievementResponse)
def create(data: AchievementCreate, db: Session = Depends(get_db)):
    """Create a new achievement (admin only in production)"""
    return create_achievement(db, data)


@router.get("/")
def list_achievements(db: Session = Depends(get_db)):
    """Get all available achievements"""
    achievements = db.query(Achievement).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "tier": a.tier,
            "metric": a.metric,
            "target_value": a.target_value,
            "points": a.points,
        }
        for a in achievements
    ]


@router.get("/user/{user_id}")
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    """Get a user's achievement progress"""
    # Get all achievements
    all_achievements = db.query(Achievement).all()
    
    # Get user's progress on achievements
    user_progress = db.query(PlayerAchievement).filter(
        PlayerAchievement.user_id == user_id
    ).all()
    
    # Create a map of achievement_id -> progress
    progress_map = {p.achievement_id: p for p in user_progress}
    
    result = []
    for ach in all_achievements:
        progress = progress_map.get(ach.id)
        result.append({
            "id": ach.id,
            "name": ach.name,
            "description": ach.description,
            "tier": ach.tier,
            "points": ach.points,
            "target_value": ach.target_value,
            "current_value": progress.current_value if progress else 0,
            "unlocked": progress.unlocked if progress else False,
            "unlocked_at": progress.unlocked_at if progress else None,
        })
    
    return result


@router.get("/me")
def get_my_achievements(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's achievement progress"""
    return get_user_achievements(current_user.id, db)
