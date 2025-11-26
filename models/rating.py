from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)

    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)

    rating = Column(Float, nullable=False)  # e.g. StatHub rating snapshot
    context = Column(String(100), nullable=True)  # e.g. "overall", "form", etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("User", backref="ratings")
    match = relationship("Match", backref="ratings")
