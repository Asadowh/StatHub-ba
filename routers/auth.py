from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from schemas.auth_schema import SignupSchema, LoginSchema, TokenResponse
from pydantic import BaseModel
from services.auth_service import (
    register_user,
    login_user,
    verify_email,
    send_reset_password_email,
    validate_reset_code,
    reset_password,
    change_password,
    resend_verification_email
)
from core.security import get_current_user

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
        file_path = f"uploads/avatars/{file_name}"

        os.makedirs("uploads/avatars", exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        photo_url = f"/uploads/avatars/{file_name}"

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
    try:
        return login_user(db, data)
    except HTTPException:
        # Re-raise HTTP exceptions (like invalid credentials)
        raise
    except Exception as e:
        # Catch any other errors (database, etc.) and return a proper error message
        import traceback
        print(f"Login error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


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
# VERIFY EMAIL (with 6-digit code)
# ----------------------------------------------------------
from pydantic import BaseModel

class VerifyEmailSchema(BaseModel):
    code: str

@router.post("/verify-email")
def verify_email_route(
    data: VerifyEmailSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Verify email using 6-digit code. Requires authentication."""
    return verify_email(db, data.code, current_user.id)

# Legacy token-based verification (for backward compatibility)
@router.get("/verify-email-token")
def verify_email_token_route(token: str, db: Session = Depends(get_db)):
    """Legacy token-based verification. Use POST /verify-email with code instead."""
    return verify_email(db, token)


# ----------------------------------------------------------
# SEND RESET PASSWORD EMAIL
# ----------------------------------------------------------
class ForgotPasswordSchema(BaseModel):
    email: str

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordSchema, db: Session = Depends(get_db)):
    return send_reset_password_email(db, data.email)


# ----------------------------------------------------------
# VALIDATE RESET CODE
# ----------------------------------------------------------
class ValidateResetCodeSchema(BaseModel):
    email: str
    code: str

@router.post("/validate-reset-code")
def validate_reset_code_route(data: ValidateResetCodeSchema, db: Session = Depends(get_db)):
    """Validate a reset code. Returns success if code is valid."""
    try:
        return validate_reset_code(db, data.email, data.code)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other errors (database, etc.) and return a proper error message
        import traceback
        print(f"Error validating reset code: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error validating reset code: {str(e)}")


# ----------------------------------------------------------
# RESET PASSWORD (with validated 6-digit code)
# ----------------------------------------------------------
class ResetPasswordSchema(BaseModel):
    email: str
    code: str
    new_password: str

@router.post("/reset-password")
def reset_password_route(data: ResetPasswordSchema, db: Session = Depends(get_db)):
    return reset_password(db, data.email, data.code, data.new_password)


# ----------------------------------------------------------
# CHANGE PASSWORD (requires authentication)
# ----------------------------------------------------------
class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str

@router.post("/change-password")
def change_password_route(
    data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Change password for logged-in user. Requires current password."""
    return change_password(db, current_user.id, data.current_password, data.new_password)


# ----------------------------------------------------------
# RESEND VERIFICATION EMAIL
# ----------------------------------------------------------
@router.post("/resend-verification")
def resend_verification_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Resend email verification link to logged-in user."""
    return resend_verification_email(db, current_user.id)
