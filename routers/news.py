from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.news_schema import NewsCreate, NewsResponse
from services.news_service import create_news, list_news

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/", response_model=NewsResponse)
def create(data: NewsCreate, db: Session = Depends(get_db)):
    return create_news(db, data)

@router.get("/", response_model=list[NewsResponse])
def get_news(db: Session = Depends(get_db)):
    return list_news(db)
