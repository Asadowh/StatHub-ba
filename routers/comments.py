from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user

from schemas.comment_schema import CommentCreate, CommentResponse
from services.comment_service import create_comment, get_comments_for_news, delete_comment

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
def make_comment(data: CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_comment(db, data, user.id)

@router.get("/news/{news_id}", response_model=list[CommentResponse])
def list_news_comments(news_id: int, db: Session = Depends(get_db)):
    return get_comments_for_news(db, news_id)

@router.delete("/{comment_id}")
def delete_comment_endpoint(
    comment_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Delete a comment. Only the comment author or an admin can delete it."""
    try:
        return delete_comment(db, comment_id, user.id, user.role)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 403, detail=str(e))
