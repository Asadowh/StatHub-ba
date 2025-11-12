from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared fields
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserLogin(BaseModel):
    identifier: str  # can be username OR email
    password: str

# For creating a new user (register)
class UserCreate(UserBase):
    password: str

# For showing user data in responses
class UserResponse(UserBase):
    id: int
    created_at: datetime
    role: str
    is_active: bool

    class Config:
        orm_mode = True
