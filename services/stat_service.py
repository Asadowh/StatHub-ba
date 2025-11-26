from sqlalchemy.orm import Session
from models.stat import Stat

def create_stat(db: Session, data):
    stat = Stat(
        match_id=data.match_id,
        player_id=data.player_id,
        goals=data.goals,
        assists=data.assists,
        rating=data.rating
    )
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


def get_stats_for_match(db: Session, match_id: int):
    return db.query(Stat).filter(Stat.match_id == match_id).all()
