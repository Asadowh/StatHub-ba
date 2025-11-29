from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from core.security import get_current_user
from schemas.user_schema import UserResponse, UserUpdate
from services.user_service import update_user, get_user_by_id
from services.xp_service import get_user_xp_info, update_user_xp_and_level
from models.user import User
from models.stat import Stat
from models.trophy import Trophy
from models.achievement import PlayerAchievement
import shutil
import os
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

# Ensure upload directory exists
UPLOAD_DIR = "static/profile_pics"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(data: UserUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user(db, current_user, data)


@router.post("/me/photo", response_model=UserResponse)
def upload_photo(
    photo: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload or update user's profile photo"""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    if photo.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Use JPEG, PNG, WebP or GIF.")
    
    # Generate unique filename
    ext = photo.filename.split(".")[-1] if "." in photo.filename else "jpg"
    file_name = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    # Delete old photo if exists
    if current_user.photo_url:
        old_path = current_user.photo_url.lstrip("/")
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except:
                pass
    
    # Save new photo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    # Update user's photo_url
    current_user.photo_url = f"/static/profile_pics/{file_name}"
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user's public profile by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "photo_url": user.photo_url,
        "nationality": user.nationality,
        "favorite_position": user.favorite_position,
        "jersey_number": user.jersey_number,
    }


@router.get("/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """Get aggregated stats for a user"""
    # Check user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get aggregated stats
    stats = db.query(
        func.count(Stat.id).label("matches_played"),
        func.coalesce(func.sum(Stat.goals), 0).label("total_goals"),
        func.coalesce(func.sum(Stat.assists), 0).label("total_assists"),
        func.coalesce(func.avg(Stat.rating), 0).label("avg_rating"),
    ).filter(Stat.player_id == user_id).first()

    # Get trophy count
    trophy_count = db.query(func.count(Trophy.id)).filter(Trophy.awarded_to == user_id).scalar()

    # Get achievement count
    unlocked_achievements = db.query(func.count(PlayerAchievement.id)).filter(
        PlayerAchievement.user_id == user_id,
        PlayerAchievement.unlocked == True
    ).scalar()

    return {
        "user_id": user_id,
        "matches_played": stats.matches_played or 0,
        "total_goals": stats.total_goals or 0,
        "total_assists": stats.total_assists or 0,
        "avg_rating": round(stats.avg_rating or 0, 1),
        "trophy_count": trophy_count or 0,
        "achievements_unlocked": unlocked_achievements or 0,
    }


@router.get("/me/xp")
def get_my_xp_info(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's XP and level information"""
    # Ensure XP is up to date
    update_user_xp_and_level(db, current_user.id)
    return get_user_xp_info(db, current_user.id)


@router.get("/{user_id}/xp")
def get_user_xp(user_id: int, db: Session = Depends(get_db)):
    """Get a user's XP and level information"""
    return get_user_xp_info(db, user_id)


@router.post("/recalculate-xp")
def recalculate_all_xp(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Recalculate XP for all users (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can recalculate XP")
    
    users = db.query(User).all()
    updated = 0
    for user in users:
        update_user_xp_and_level(db, user.id)
        updated += 1
    
    return {"message": f"Recalculated XP for {updated} users"}


@router.put("/{user_id}/make-admin")
def make_admin(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Make a user an admin (admin only, or first user becomes admin)"""
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Allow if current user is admin, OR if this is the first user in the system
    is_first_user = db.query(User).count() == 1
    if current_user.role != "admin" and not is_first_user:
        raise HTTPException(status_code=403, detail="Only admin can promote users to admin")
    
    target_user.role = "admin"
    db.commit()
    db.refresh(target_user)
    
    return {
        "message": f"User {target_user.username} is now an admin",
        "user": {
            "id": target_user.id,
            "username": target_user.username,
            "role": target_user.role
        }
    }
