from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Trophy(Base):
    __tablename__ = "trophies"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, unique=True)
    awarded_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_awarded = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    match = relationship("Match", backref="trophy")
    player = relationship("User", backref="trophies")
    
    __table_args__ = (
        UniqueConstraint('match_id', name='uq_trophy_match_id'),
    )
