from sqlalchemy.orm import Session
from models.rating import Rating

def create_rating(db: Session, data):
    rating = Rating(
        player_id=data.player_id,
        match_id=data.match_id,
        rating=data.rating,
        context=data.context
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


def get_player_ratings(db: Session, player_id: int):
    return db.query(Rating).filter(Rating.player_id == player_id).all()
