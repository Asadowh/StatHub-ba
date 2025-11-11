from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.comment import Comment
from schemas.comment_schema import CommentCreate, CommentResponse
from typing import List

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

# Create a comment
@router.post("/", response_model=CommentResponse)
def create_comment(request: CommentCreate, db: Session = Depends(get_db)):
    new_comment = Comment(
        content=request.content,
        author_id=request.author_id,
        news_id=request.news_id,
        match_id=request.match_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# Get all comments
@router.get("/", response_model=List[CommentResponse])
def get_all_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()


# Get comments for a specific news post
@router.get("/news/{news_id}", response_model=List[CommentResponse])
def get_comments_for_news(news_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.news_id == news_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this news post.")
    return comments


# Get comments for a specific match
@router.get("/match/{match_id}", response_model=List[CommentResponse])
def get_comments_for_match(match_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.match_id == match_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this match.")
    return comments
