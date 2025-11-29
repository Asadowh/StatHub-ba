from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from core.security import get_current_admin
import os
import shutil
import uuid

from schemas.news_schema import NewsResponse
from services.news_service import create_news, list_news
from models.news import News
from models.comment import Comment

router = APIRouter(prefix="/news", tags=["News"])

# Ensure upload directory exists
UPLOAD_DIR = "static/news_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=NewsResponse)
def create(
    title: str = Form(...),
    content: str = Form(...),
    category: Optional[str] = Form(None),
    image: UploadFile = File(None),
    admin_user = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a news post (admin only). Can include optional image and category."""
    image_url = None
    
    if image:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
        if image.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Use JPEG, PNG, WebP or GIF.")
        
        # Generate unique filename
        ext = image.filename.split(".")[-1] if "." in image.filename else "jpg"
        file_name = f"news_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        # Save image
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/static/news_images/{file_name}"
    
    return create_news(db, title, content, admin_user.id, image_url, category)

@router.get("/", response_model=list[NewsResponse])
def get_news(db: Session = Depends(get_db)):
    return list_news(db)

@router.delete("/{news_id}")
def delete_news(
    news_id: int,
    admin_user = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a news post and all its comments (admin only)."""
    # Get the news item
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    
    # Delete all comments associated with this news item FIRST
    db.query(Comment).filter(Comment.news_id == news_id).delete()
    
    # Then delete the news item
    db.delete(news)
    db.commit()
    
    return {"message": "News deleted successfully"}
