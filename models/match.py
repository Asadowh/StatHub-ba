from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    match_date = Column(DateTime(timezone=True), server_default=func.now())
    score_home = Column(Integer, default=0)
    score_away = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.id"))  # who created the match

    # relationships
    creator = relationship("User")
