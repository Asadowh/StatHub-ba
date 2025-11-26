from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re
from datetime import date

class SignupSchema(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    height: Optional[int] = None
    jersey_number: Optional[int] = None
    nationality: str
    birth_date: date
    favorite_position: str
    personal_quote: Optional[str] = None

    # VALIDATIONS
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

class LoginSchema(BaseModel):
    # user can login with email OR username
    credential: str  # email OR username
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
