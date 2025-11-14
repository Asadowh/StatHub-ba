from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models import rating

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    match_date = Column(DateTime, nullable=False)
    score_home = Column(Integer, default=0)
    score_away = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Safe relationship (DO NOT REMOVE)
#    creator = relationship("User", backref="created_matches")
    creator = relationship("User")