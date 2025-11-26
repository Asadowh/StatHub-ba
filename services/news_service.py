from sqlalchemy.orm import Session
from models.news import News

def create_news(db: Session, data):
    news = News(
        title=data.title,
        content=data.content,
        author_id=data.author_id
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def list_news(db: Session):
    return db.query(News).order_by(News.created_at.desc()).all()
