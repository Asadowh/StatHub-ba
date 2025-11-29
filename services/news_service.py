from sqlalchemy.orm import Session
from models.news import News

def create_news(db: Session, title: str, content: str, author_id: int, image_url: str = None, category: str = None):
    news = News(
        title=title,
        content=content,
        author_id=author_id,
        image_url=image_url,
        category=category if category and category.strip() else None
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def list_news(db: Session):
    return db.query(News).order_by(News.created_at.desc()).all()
