from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.stat_schema import StatCreate, StatResponse
from services.stat_service import create_stat, get_stats_for_match

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.post("/", response_model=StatResponse)
def create_stat_endpoint(data: StatCreate, db: Session = Depends(get_db)):
    return create_stat(db, data)

@router.get("/match/{match_id}", response_model=list[StatResponse])
def get_match_stats(match_id: int, db: Session = Depends(get_db)):
    return get_stats_for_match(db, match_id)
