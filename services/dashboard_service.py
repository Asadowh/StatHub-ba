from sqlalchemy.orm import Session
from models.user import User
from models.trophy import Trophy
from models.stat import Stat

def get_dashboard_data(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    total_goals = db.query(Stat).filter(Stat.player_id == user_id).with_entities(
        Stat.goals
    )
    total_goals = sum([s for s in (g[0] for g in total_goals)])

    trophies = db.query(Trophy).filter(Trophy.awarded_to == user_id).count()

    return {
        "user_id": user_id,
        "total_goals": total_goals,
        "trophies": trophies,
    }
