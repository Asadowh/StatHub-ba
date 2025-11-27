from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Auth fields
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    # Profile fields
    full_name = Column(String(100), nullable=True)
    photo_url = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    jersey_number = Column(Integer, nullable=True)
    nationality = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    favorite_position = Column(String(10), nullable=True)
    personal_quote = Column(String(200), nullable=True)

    # Status fields
    role = Column(String(20), default="player")
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    
    # XP and Level (calculated from achievements)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
