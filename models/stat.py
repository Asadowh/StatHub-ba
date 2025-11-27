from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Stat(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Which team the player was on: "home" or "away"
    team = Column(String, default="home")

    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    rating = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    match = relationship("Match", backref="stats")
    player = relationship("User", backref="stats")
