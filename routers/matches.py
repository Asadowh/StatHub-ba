from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.match_schema import MatchCreate, MatchResponse
from services.match_service import create_match, list_matches

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.post("/", response_model=MatchResponse)
def create_match_endpoint(data: MatchCreate, db: Session = Depends(get_db)):
    return create_match(db, data)

@router.get("/", response_model=list[MatchResponse])
def list_matches_endpoint(db: Session = Depends(get_db)):
    return list_matches(db)
