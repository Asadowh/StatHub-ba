from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.reaction import Reaction
from schemas.reaction_schema import ReactionCreate, ReactionResponse
from typing import List

router = APIRouter(
    prefix="/reactions",
    tags=["Reactions"]
)

# Create a reaction
@router.post("/", response_model=ReactionResponse)
def create_reaction(request: ReactionCreate, db: Session = Depends(get_db)):
    new_reaction = Reaction(
        type=request.type,
        user_id=request.user_id,
        news_id=request.news_id,
        comment_id=request.comment_id,
        match_id=request.match_id
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    return new_reaction


# Get all reactions
@router.get("/", response_model=List[ReactionResponse])
def get_all_reactions(db: Session = Depends(get_db)):
    return db.query(Reaction).all()


# Get reactions for a specific post/comment/match
@router.get("/by")
def get_reactions_by_target(
    news_id: int | None = None,
    comment_id: int | None = None,
    match_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Reaction)
    if news_id:
        query = query.filter(Reaction.news_id == news_id)
    elif comment_id:
        query = query.filter(Reaction.comment_id == comment_id)
    elif match_id:
        query = query.filter(Reaction.match_id == match_id)
    else:
        raise HTTPException(status_code=400, detail="You must specify one target (news_id, comment_id, or match_id).")

    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No reactions found.")
    return results
