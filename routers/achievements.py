from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user

from schemas.achievement_schema import AchievementCreate, AchievementResponse
from services.achievement_service import create_achievement
from services.achievement_checker import check_and_unlock_achievements
from models.achievement import Achievement, PlayerAchievement
from models.user import User
from scripts.seed_achievements import seed_achievements

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.post("/", response_model=AchievementResponse)
def create(data: AchievementCreate, db: Session = Depends(get_db)):
    """Create a new achievement (admin only in production)"""
    return create_achievement(db, data)


@router.get("/")
def list_achievements(db: Session = Depends(get_db)):
    """Get all available achievements"""
    achievements = db.query(Achievement).order_by(Achievement.tier, Achievement.target_value).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "tier": a.tier,
            "points": a.points,
            "target_value": a.target_value,
            "created_at": a.created_at,
        }
        for a in achievements
    ]


@router.get("/user/{user_id}")
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user's achievement progress.
    Automatically checks and unlocks achievements based on current stats.
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Auto-check and unlock achievements based on stats
    try:
        check_and_unlock_achievements(db, user_id)
    except Exception as e:
        print(f"⚠️  Error auto-checking achievements for user {user_id}: {e}")
        # Continue anyway - don't fail the request
    
    # Get all achievements
    all_achievements = db.query(Achievement).order_by(Achievement.tier, Achievement.target_value).all()
    
    # Get user's progress on achievements
    user_progress = db.query(PlayerAchievement).filter(
        PlayerAchievement.user_id == user_id
    ).all()
    
    # Create a map of achievement_id -> progress
    progress_map = {p.achievement_id: p for p in user_progress}
    
    result = []
    for ach in all_achievements:
        progress = progress_map.get(ach.id)
        current_value = progress.current_value if progress else 0
        
        # For rating-based achievements, current_value is stored as integer*10 (e.g., 75 for 7.5)
        # Convert to actual rating for display
        if ach.metric == "rating":
            # Divide by 10 to get actual rating (e.g., 75 -> 7.5)
            display_current_value = round(current_value / 10.0, 1) if current_value > 0 else 0.0
        else:
            display_current_value = current_value
        
        result.append({
            "id": ach.id,
            "name": ach.name,
            "description": ach.description,
            "tier": ach.tier,
            "points": ach.points,
            "target_value": ach.target_value,  # Keep as stored (integer)
            "current_value": display_current_value,
            "unlocked": progress.unlocked if progress else False,
            "unlocked_at": progress.unlocked_at if progress else None,
        })
    
    return result


@router.get("/me")
def get_my_achievements(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's achievement progress (refreshes progress automatically)"""
    return get_user_achievements(current_user.id, db)


@router.post("/seed")
def seed_achievements_endpoint(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Seed achievements into the database (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can seed achievements")
    
    try:
        seed_achievements(db)
        return {"message": "Achievements seeded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding achievements: {str(e)}")


@router.post("/check-all")
def check_all_users_achievements(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Check and unlock achievements for all users (admin only, useful for existing data)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can check achievements for all users")
    
    try:
        # Get all players (non-admin users)
        players = db.query(User).filter(User.role == "player").all()
        
        unlocked_count = 0
        for player in players:
            try:
                if check_and_unlock_achievements(db, player.id):
                    unlocked_count += 1
            except Exception as e:
                print(f"Error checking achievements for user {player.id}: {e}")
                continue
        
        return {
            "message": f"Checked achievements for {len(players)} players",
            "players_with_new_achievements": unlocked_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking achievements: {str(e)}")


@router.post("/me/refresh")
def refresh_my_achievements(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Refresh achievements for the current user (updates progress and unlocks if conditions are met)"""
    try:
        unlocked = check_and_unlock_achievements(db, current_user.id)
        return {
            "message": "Achievements refreshed",
            "new_achievements_unlocked": unlocked
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing achievements: {str(e)}")
