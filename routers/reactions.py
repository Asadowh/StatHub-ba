from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user
from sqlalchemy import func

from schemas.reaction_schema import ReactionCreate, ReactionResponse
from services.reaction_service import create_reaction
from models.reaction import Reaction

router = APIRouter(prefix="/reactions", tags=["Reactions"])

@router.post("/")
def react(data: ReactionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Toggle a reaction (like/unlike). Returns reaction if created, or null if removed."""
    result = create_reaction(db, data, user.id)
    if result:
        return {"reaction": result, "action": "added"}
    return {"reaction": None, "action": "removed"}

@router.get("/news/{news_id}/counts")
def get_news_reaction_counts(news_id: int, db: Session = Depends(get_db)):
    """Get reaction counts for a news post grouped by type"""
    counts = db.query(
        Reaction.type,
        func.count(Reaction.id).label("count")
    ).filter(
        Reaction.news_id == news_id
    ).group_by(Reaction.type).all()
    
    return {count.type: count.count for count in counts}

@router.get("/news/{news_id}/user/{user_id}")
def get_user_reactions_for_news(news_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get all reaction types that a user has on a news post"""
    reactions = db.query(Reaction.type).filter(
        Reaction.news_id == news_id,
        Reaction.user_id == user_id
    ).all()
    
    return {"reactions": [r.type for r in reactions]}
