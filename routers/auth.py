from fastapi import APIRouter, Depends, Form, File, UploadFile
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

import uuid, os, shutil

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ----------------------------------------------------------
# REGISTER with photo upload
# ----------------------------------------------------------
@router.post("/register", response_model=TokenResponse)
def register(
    full_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),

    password: str = Form(...),
    confirm_password: str = Form(...),

    height: int = Form(None),
    jersey_number: int = Form(None),
    nationality: str = Form(...),
    birth_date: str = Form(...),
    favorite_position: str = Form(...),
    personal_quote: str = Form(None),

    photo: UploadFile = File(None),

    db: Session = Depends(get_db),
):
    # Validate using existing Pydantic schema
    data = SignupSchema(
        full_name=full_name,
        username=username,
        email=email,
        password=password,
        confirm_password=confirm_password,
        height=height,
        jersey_number=jersey_number,
        nationality=nationality,
        birth_date=birth_date,
        favorite_position=favorite_position,
        personal_quote=personal_quote,
    )

    # Handle image upload
    photo_url = None
    if photo:
        ext = photo.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{ext}"
        file_path = f"static/profile_pics/{file_name}"

        os.makedirs("static/profile_pics", exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        photo_url = f"/static/profile_pics/{file_name}"

    # Create user with service
    user = register_user(db, data, photo_url=photo_url)

    # Auto-login after register
    token = login_user(db, LoginSchema(credential=user.email, password=password))
    return token


# ----------------------------------------------------------
# LOGIN (JSON body)
# ----------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(db, data)


# ----------------------------------------------------------
# LOGIN (OAuth2 Form - for Swagger Authorize button)
# ----------------------------------------------------------
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token", response_model=TokenResponse)
def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 compatible login for Swagger UI"""
    data = LoginSchema(credential=form_data.username, password=form_data.password)
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
