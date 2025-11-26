from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    location = Column(String, nullable=False)
    match_date = Column(DateTime, nullable=False)

    winner_team = Column(String, nullable=True)  # "home", "away", or None
    created_at = Column(DateTime, default=datetime.utcnow)
