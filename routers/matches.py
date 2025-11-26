from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.match import Match
from schemas.match_schema import MatchCreate, MatchResponse, DATE_FORMAT
from datetime import datetime
from typing import List

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)


# Create a match
@router.post("/", response_model=MatchResponse)
def create_match(request: MatchCreate, db: Session = Depends(get_db)):
    # Convert string date to datetime
    match_date = datetime.strptime(request.match_date, DATE_FORMAT)

    new_match = Match(
        home_team=request.home_team,
        away_team=request.away_team,
        location=request.location,
        match_date=match_date,
        score_home=request.score_home,
        score_away=request.score_away,
        created_by=1  # temporary until JWT auth
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match


# Get all matches
@router.get("/", response_model=List[MatchResponse])
def get_all_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).all()
    return matches