from sqlalchemy.orm import Session
from sqlalchemy import func
from models.user import User
from models.achievement import PlayerAchievement, Achievement
from core.levels import get_level_from_xp, get_xp_progress


def calculate_user_xp(db: Session, user_id: int) -> int:
    """
    Calculate total XP from unlocked achievements.
    XP = sum of points from all unlocked achievements
    """
    unlocked_achievements = (
        db.query(PlayerAchievement)
        .join(Achievement, PlayerAchievement.achievement_id == Achievement.id)
        .filter(
            PlayerAchievement.user_id == user_id,
            PlayerAchievement.unlocked == True
        )
        .all()
    )
    
    total_xp = sum(ach.achievement.points for ach in unlocked_achievements)
    return total_xp


def update_user_xp_and_level(db: Session, user_id: int):
    """
    Calculate and update user's XP and level based on achievements
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    # Calculate XP from achievements
    total_xp = calculate_user_xp(db, user_id)
    
    # Calculate level from XP
    level = get_level_from_xp(total_xp)
    
    # Update user
    user.xp = total_xp
    user.level = level
    db.commit()
    db.refresh(user)
    
    return {
        "xp": total_xp,
        "level": level,
        "level_info": get_xp_progress(total_xp, level)
    }


def get_user_xp_info(db: Session, user_id: int) -> dict:
    """Get user's XP and level information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    return get_xp_progress(user.xp, user.level)

