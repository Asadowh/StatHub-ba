from sqlalchemy.orm import Session
from models.user import User
from models.match import Match

def search_players(db: Session, query: str):
    return db.query(User).filter(User.username.ilike(f"%{query}%")).all()

def search_matches(db: Session, team_query: str):
    return (
        db.query(Match)
        .filter(
            (Match.home_team.ilike(f"%{team_query}%")) |
            (Match.away_team.ilike(f"%{team_query}%"))
        )
        .all()
    )
