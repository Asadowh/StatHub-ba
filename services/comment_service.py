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


def delete_comment(db: Session, comment_id: int, user_id: int, user_role: str):
    """Delete a comment. Only the comment author or an admin can delete it."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise ValueError("Comment not found")
    
    # Check if user is admin or the comment author
    if user_role != "admin" and comment.author_id != user_id:
        raise ValueError("You don't have permission to delete this comment")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}