from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.auth_schema import SignupSchema, LoginSchema, TokenResponse
from services.auth_service import (
    register_user,
    login_user,
    verify_email,
    send_reset_password_email,
    reset_password
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------
@router.post("/register", response_model=TokenResponse)
def register(data: SignupSchema, db: Session = Depends(get_db)):
    user = register_user(db, data)
    token = login_user(db, LoginSchema(credential=user.email, password=data.password))
    return token


# ----------------------------------------------------------
# LOGIN
# ----------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(db, data)


# ----------------------------------------------------------
# VERIFY EMAIL
# ----------------------------------------------------------
@router.get("/verify-email")
def verify_email_route(token: str, db: Session = Depends(get_db)):
    return verify_email(db, token)


# ----------------------------------------------------------
# SEND RESET PASSWORD EMAIL
# ----------------------------------------------------------
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    return send_reset_password_email(db, email)


# ----------------------------------------------------------
# RESET PASSWORD
# ----------------------------------------------------------
@router.post("/reset-password")
def reset_password_route(token: str, new_password: str, db: Session = Depends(get_db)):
    return reset_password(db, token, new_password)
