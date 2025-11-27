from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    match_date = Column(DateTime, nullable=False)

    winner_team = Column(String, nullable=True)  # "home", "away", "draw", or None
    created_at = Column(DateTime, default=datetime.utcnow)
