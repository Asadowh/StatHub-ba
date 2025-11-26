from pydantic import BaseModel, EmailStr
from datetime import datetime
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

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True
