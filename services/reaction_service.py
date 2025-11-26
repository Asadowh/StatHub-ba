from sqlalchemy.orm import Session
from models.reaction import Reaction

def create_reaction(db: Session, data, user_id: int):
    reaction = Reaction(
        type=data.type,
        user_id=user_id,
        news_id=data.news_id,
        comment_id=data.comment_id,
        match_id=data.match_id,
    )
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction
