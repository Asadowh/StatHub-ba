from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.reaction import Reaction

def create_reaction(db: Session, data, user_id: int):
    """Create or toggle a reaction. If reaction exists, delete it (unlike). Otherwise, create it (like)."""
    # Build filter conditions
    filters = [
        Reaction.user_id == user_id,
        Reaction.type == data.type,
    ]
    
    # Add specific filters based on what's provided
    if data.news_id:
        filters.append(Reaction.news_id == data.news_id)
    else:
        filters.append(Reaction.news_id.is_(None))
    
    if data.comment_id:
        filters.append(Reaction.comment_id == data.comment_id)
    else:
        filters.append(Reaction.comment_id.is_(None))
    
    if data.match_id:
        filters.append(Reaction.match_id == data.match_id)
    else:
        filters.append(Reaction.match_id.is_(None))
    
    # Check if reaction already exists
    existing = db.query(Reaction).filter(and_(*filters)).first()
    
    if existing:
        # Toggle: delete existing reaction (unlike)
        db.delete(existing)
        db.commit()
        return None  # Return None to indicate reaction was removed
    
    # Create new reaction (like)
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
