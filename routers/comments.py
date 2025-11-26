from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user

from schemas.comment_schema import CommentCreate, CommentResponse
from services.comment_service import create_comment, get_comments_for_news

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
def make_comment(data: CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_comment(db, data, user.id)

@router.get("/news/{news_id}", response_model=list[CommentResponse])
def list_news_comments(news_id: int, db: Session = Depends(get_db)):
    return get_comments_for_news(db, news_id)
