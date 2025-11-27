from sqlalchemy.orm import Session
from models.match import Match

def create_match(db: Session, data):
    # Auto-determine winner based on scores
    winner = None
    if data.home_score > data.away_score:
        winner = "home"
    elif data.away_score > data.home_score:
        winner = "away"
    elif data.home_score == data.away_score and data.home_score > 0:
        winner = "draw"

    match = Match(
        home_team=data.home_team,
        away_team=data.away_team,
        home_score=data.home_score,
        away_score=data.away_score,
        match_date=data.match_date,
        winner_team=winner
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def list_matches(db: Session):
    return db.query(Match).order_by(Match.match_date.desc()).all()


def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()
