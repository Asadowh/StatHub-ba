from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.match import Match
from models.user import User
from schemas.match_schema import MatchCreate, MatchResponse
from datetime import datetime
from typing import List

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

# TEMP ADMIN (because your auth is not ready yet)
TEMP_ADMIN_ID = 1


@router.post("/", response_model=MatchResponse)
def create_match(request: MatchCreate, db: Session = Depends(get_db)):

    # Ensure the admin user exists
    admin = db.query(User).filter(User.id == TEMP_ADMIN_ID).first()
    if not admin:
        raise HTTPException(
            status_code=400,
            detail="Admin user with ID=1 not found. Create it first."
        )

    # Parse date format (MM/DD/YYYY HH:MM)
    try:
        match_date = datetime.strptime(request.match_date, "%m/%d/%Y %H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Use format MM/DD/YYYY HH:MM"
        )

    new_match = Match(
        home_team=request.home_team,
        away_team=request.away_team,
        location=request.location,
        match_date=match_date,
        score_home=request.score_home,
        score_away=request.score_away,
        created_by=1  # <-- IMPORTANT
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    # return manually formatted JSON
    return {
        "id": new_match.id,
        "home_team": new_match.home_team,
        "away_team": new_match.away_team,
        "location": new_match.location,
        "match_date": new_match.match_date.strftime("%m/%d/%Y %H:%M"),
        "score_home": new_match.score_home,
        "score_away": new_match.score_away,
        "created_by": new_match.created_by
    }


@router.get("/", response_model=List[MatchResponse])
def get_all_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).all()

    return [
        {
            "id": m.id,
            "home_team": m.home_team,
            "away_team": m.away_team,
            "location": m.location,
            "match_date": m.match_date.strftime("%m/%d/%Y %H:%M"),
            "score_home": m.score_home,
            "score_away": m.score_away,
            "created_by": m.created_by
        }
        for m in matches
    ]