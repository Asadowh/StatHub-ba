from sqlalchemy.orm import Session
from models.match import Match

def create_match(db: Session, data):
    match = Match(
        home_team=data.home_team,
        away_team=data.away_team,
        location=data.location,
        match_date=data.match_date
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def list_matches(db: Session):
    return db.query(Match).all()


def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()
