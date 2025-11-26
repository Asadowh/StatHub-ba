from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from models import rating

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # e.g. "like", "love", "fire", "goal"
    user_id = Column(Integer, ForeignKey("users.id"))
    news_id = Column(Integer, ForeignKey("news.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    news = relationship("News", backref="reactions")
    comment = relationship("Comment", backref="reactions")
    match = relationship("Match", backref="reactions")
