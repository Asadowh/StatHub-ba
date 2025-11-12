from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared fields
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "player"
    is_active: bool = True
    
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

    class Config:
        orm_mode = True
