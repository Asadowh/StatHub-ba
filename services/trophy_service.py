from sqlalchemy.orm import Session
from models.trophy import Trophy

def award_trophy(db: Session, data):
    trophy = Trophy(
        name=data.name,
        description=data.description,
        awarded_to=data.awarded_to
    )
    db.add(trophy)
    db.commit()
    db.refresh(trophy)
    return trophy


def get_user_trophies(db: Session, user_id: int):
    return db.query(Trophy).filter(Trophy.awarded_to == user_id).all()
