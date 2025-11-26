from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)

    full_name = Column(String(100), nullable=True)  # used on signup/profile
    hashed_password = Column(String, nullable=False)

    role = Column(String(20), default="player")  # "player", "admin", "coach", etc.
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
