from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Trophy(Base):
    __tablename__ = "trophies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)               # e.g. "Top Scorer"
    description = Column(String(255), nullable=True)
    awarded_to = Column(Integer, ForeignKey("users.id"))     # link to user
    date_awarded = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    player = relationship("User", backref="trophies")
