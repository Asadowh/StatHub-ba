from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.news import News
from schemas.news_schema import NewsCreate, NewsResponse
from typing import List

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

# Create a news post
@router.post("/", response_model=NewsResponse)
def create_news(request: NewsCreate, db: Session = Depends(get_db)):
    new_post = News(
        title=request.title,
        content=request.content,
        author_id=request.author_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get all news posts
@router.get("/", response_model=List[NewsResponse])
def get_all_news(db: Session = Depends(get_db)):
    posts = db.query(News).order_by(News.created_at.desc()).all()
    return posts


# Get a single news post by ID
@router.get("/{news_id}", response_model=NewsResponse)
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    post = db.query(News).filter(News.id == news_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="News post not found")
    return post


# Delete a news post
@router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    post = db.query(News).filter(News.id == news_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="News post not found")
    db.delete(post)
    db.commit()
    return {"message": "News post deleted successfully"}
