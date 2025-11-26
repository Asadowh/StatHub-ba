from sqlalchemy.orm import Session
from models.comment import Comment

def create_comment(db: Session, data, author_id: int):
    comment = Comment(
        content=data.content,
        author_id=author_id,
        news_id=data.news_id,
        match_id=data.match_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments_for_news(db: Session, news_id: int):
    return db.query(Comment).filter(Comment.news_id == news_id).all()
