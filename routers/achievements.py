from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.achievement_schema import AchievementCreate, AchievementResponse
from services.achievement_service import create_achievement

router = APIRouter(prefix="/achievements", tags=["Achievements"])

@router.post("/", response_model=AchievementResponse)
def create(data: AchievementCreate, db: Session = Depends(get_db)):
    return create_achievement(db, data)
