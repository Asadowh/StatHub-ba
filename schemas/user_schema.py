from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from typing import Optional

class UserLogin(BaseModel):
    identifier: str   # username OR email
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    height: Optional[int] = None
    jersey_number: Optional[int] = None
    nationality: Optional[str] = None
    birth_date: Optional[date] = None
    favorite_position: Optional[str] = None
    personal_quote: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    photo_url: Optional[str]
    height: Optional[int]
    jersey_number: Optional[int]
    nationality: Optional[str]
    birth_date: Optional[date]
    favorite_position: Optional[str]
    personal_quote: Optional[str]
    role: str
    is_active: bool
    is_email_verified: bool
    xp: int
    level: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
