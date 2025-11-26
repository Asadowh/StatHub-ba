from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str

    class Config:
        orm_mode = True


class UserPublic(BaseModel):
    id: int
    username: str
    full_name: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    
    height: Optional[int] = None
    jersey_number: Optional[int] = None
    nationality: Optional[str] = None
    birth_date: Optional[date] = None
    favorite_position: Optional[str] = None
    personal_quote: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str

    height: Optional[int] = None
    jersey_number: Optional[int] = None
    nationality: Optional[str] = None
    birth_date: Optional[date] = None
    favorite_position: Optional[str] = None
    personal_quote: Optional[str] = None

    class Config:
        orm_mode = True
