from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    tier = Column(String(20), nullable=False)  # "Beginner", "Advanced", "Expert", "All"
    metric = Column(String(50), nullable=False)  # "goals", "assists", "matches", etc.
    target_value = Column(Integer, nullable=False)
    points = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlayerAchievement(Base):
    __tablename__ = "player_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"))

    current_value = Column(Integer, default=0)
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime(timezone=True), nullable=True)

    player = relationship("User", backref="achievements")
    achievement = relationship("Achievement", backref="players")
