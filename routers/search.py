from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.match import Match
from models.stat import Stat

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

@router.get("/")
def search_items(
    q: str = Query(..., description="Search term (player name, match team, etc.)"),
    db: Session = Depends(get_db)
):
    results = {
        "players": [],
        "matches": [],
        "stats": []
    }

    # Search players
    players = db.query(User).filter(User.username.ilike(f"%{q}%")).all()
    results["players"] = [{"id": p.id, "username": p.username, "email": p.email} for p in players]

    # Search matches (by team name)
    matches = db.query(Match).filter(
        (Match.home_team.ilike(f"%{q}%")) | (Match.away_team.ilike(f"%{q}%"))
    ).all()
    results["matches"] = [{"id": m.id, "home_team": m.home_team, "away_team": m.away_team} for m in matches]

    # Search stats (by player_name)
    stats = db.query(Stat).filter(Stat.player_name.ilike(f"%{q}%")).all()
    results["stats"] = [
        {"id": s.id, "player_name": s.player_name, "goals": s.goals, "assists": s.assists}
        for s in stats
    ]

    if not any(results.values()):
        raise HTTPException(status_code=404, detail="No results found")

    return results
