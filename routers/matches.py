from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from core.security import get_current_user

from schemas.match_schema import MatchCreate, MatchResponse
from services.match_service import create_match, list_matches, get_match
from models.stat import Stat
from models.match import Match

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/", response_model=MatchResponse)
def create_match_endpoint(
    data: MatchCreate, 
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only admin can create matches
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create matches")
    return create_match(db, data)


@router.get("/")
def list_matches_endpoint(db: Session = Depends(get_db)):
    """Get all matches with team average ratings"""
    matches = db.query(Match).order_by(Match.match_date.desc()).all()
    
    result = []
    for match in matches:
        # Get average ratings for each team
        home_stats = db.query(func.avg(Stat.rating)).filter(
            Stat.match_id == match.id, 
            Stat.team == "home"
        ).scalar()
        
        away_stats = db.query(func.avg(Stat.rating)).filter(
            Stat.match_id == match.id, 
            Stat.team == "away"
        ).scalar()
        
        result.append({
            "id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date,
            "winner_team": match.winner_team,
            "home_avg_rating": round(home_stats, 1) if home_stats else None,
            "away_avg_rating": round(away_stats, 1) if away_stats else None,
        })
    
    return result


@router.get("/{match_id}", response_model=MatchResponse)
def get_match_endpoint(match_id: int, db: Session = Depends(get_db)):
    """Get a specific match by ID"""
    match = get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/user/{user_id}")
def get_user_matches(user_id: int, db: Session = Depends(get_db)):
    """Get all matches a user participated in"""
    # Find match IDs where user has stats
    user_stats = db.query(Stat).filter(Stat.player_id == user_id).all()
    match_ids = [s.match_id for s in user_stats]
    
    # Get those matches
    matches = db.query(Match).filter(Match.id.in_(match_ids)).order_by(Match.match_date.desc()).all()
    
    result = []
    for match in matches:
        # Get user's stats for this match
        user_stat = next((s for s in user_stats if s.match_id == match.id), None)
        result.append({
            "id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date,
            "winner_team": match.winner_team,
            "player_goals": user_stat.goals if user_stat else 0,
            "player_assists": user_stat.assists if user_stat else 0,
            "player_rating": user_stat.rating if user_stat else 0,
        })
    
    return result


@router.get("/me/history")
def get_my_matches(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's match history"""
    return get_user_matches(current_user.id, db)
