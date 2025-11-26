from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models import rating


class Stat(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(100), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)

    # relationships
    match = relationship("Match", backref="stats")