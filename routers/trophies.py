from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.trophy_schema import TrophyCreate, TrophyResponse
from services.trophy_service import award_trophy, get_user_trophies

router = APIRouter(prefix="/trophies", tags=["Trophies"])

@router.post("/", response_model=TrophyResponse)
def award(data: TrophyCreate, db: Session = Depends(get_db)):
    return award_trophy(db, data)

@router.get("/user/{user_id}", response_model=list[TrophyResponse])
def list_trophies(user_id: int, db: Session = Depends(get_db)):
    return get_user_trophies(db, user_id)
