from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import random

from models.user import User
from utils.hashing import Hash
from utils.jwt_handler import create_access_token, verify_email_token, verify_reset_token
from core.security import validate_password
from core.email_utils import generate_verification_email, generate_reset_email, send_email, generate_verification_code


# ----------------------------------------------------
# Create User (Signup)
# ----------------------------------------------------
def register_user(db, data, photo_url=None):
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        full_name=data.full_name,
        username=data.username,
        email=data.email,
        hashed_password=Hash.hash(data.password),

        # Profile fields
        height=data.height,
        jersey_number=data.jersey_number,
        nationality=data.nationality,
        birth_date=data.birth_date,
        favorite_position=data.favorite_position,
        personal_quote=data.personal_quote,

        role="player",
        is_active=True,
        is_email_verified=False,

        photo_url=photo_url
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate 6-digit verification code
    verification_code = generate_verification_code()
    new_user.verification_code = verification_code
    new_user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    db.commit()
    db.refresh(new_user)
    
    # Generate and send verification email (optional - won't crash if SMTP fails)
    try:
        html = generate_verification_email(data.email, verification_code)
        send_email(
            to_email=data.email,
            subject="Verify your StatHub account",
            html_content=html
        )
    except Exception as e:
        print(f"⚠️ Email sending skipped: {e}")

    return new_user


# ----------------------------------------------------
# Login
# ----------------------------------------------------
def login_user(db: Session, data):
    try:
        identifier = data.credential

        # Identify email OR username
        user = (
            db.query(User)
            .filter(
                (User.email == identifier) |
                (User.username == identifier)
            )
            .first()
        )

        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not Hash.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        token = create_access_token({"user_id": user.id})

        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch database errors and other exceptions
        import traceback
        print(f"Error in login_user: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ----------------------------------------------------
# Email Verification (with 6-digit code)
# ----------------------------------------------------
def verify_email(db: Session, code: str, user_id: int = None):
    """Verify email using 6-digit code. Can verify by code only or code + user_id."""
    if user_id:
        # Verify for specific user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if code matches and hasn't expired
        if user.verification_code != code:
            raise HTTPException(status_code=400, detail="Invalid verification code")
        
        if user.verification_code_expires_at and user.verification_code_expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Verification code has expired. Please request a new one.")
        
        user.is_email_verified = True
        user.verification_code = None
        user.verification_code_expires_at = None
        db.commit()
        
        # Send welcome email after successful verification
        try:
            from core.email_utils import generate_welcome_email, send_email
            welcome_html = generate_welcome_email(user.full_name or user.username)
            send_email(
                to_email=user.email,
                subject="🎉 Welcome to StatHub - Your Email is Verified!",
                html_content=welcome_html
            )
        except Exception as e:
            print(f"⚠️ Failed to send welcome email: {e}")
            # Don't fail the verification if email fails
        
        return {"message": "Email verified successfully"}
    else:
        # Legacy token-based verification (for backward compatibility)
        email = verify_email_token(code)
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid email verification token")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_email_verified = True
        user.verification_code = None
        user.verification_code_expires_at = None
        db.commit()
        
        # Send welcome email after successful verification
        try:
            from core.email_utils import generate_welcome_email, send_email
            welcome_html = generate_welcome_email(user.full_name or user.username)
            send_email(
                to_email=user.email,
                subject="🎉 Welcome to StatHub - Your Email is Verified!",
                html_content=welcome_html
            )
        except Exception as e:
            print(f"⚠️ Failed to send welcome email: {e}")
            # Don't fail the verification if email fails

        return {"message": "Email verified successfully"}


# ----------------------------------------------------
# Forgot Password (Send 6-digit code)
# ----------------------------------------------------
def send_reset_password_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate 6-digit reset code
    reset_code = generate_verification_code()
    user.reset_code = reset_code
    user.reset_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    db.commit()
    db.refresh(user)
    
    # Generate and send reset email
    html = generate_reset_email(email, reset_code)
    try:
        send_email(email, "Reset your password", html)
    except Exception as e:
        print(f"⚠️ Email sending failed: {e}")
        # Don't fail the request if email fails - user still gets the code
        pass

    return {"message": "Password reset code sent to your email"}


# ----------------------------------------------------
# Validate Reset Code (separate validation step)
# ----------------------------------------------------
def validate_reset_code(db: Session, email: str, code: str):
    """Validate a reset code without resetting the password."""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if reset_code column exists (migration might not have been run)
        if not hasattr(user, 'reset_code') or user.reset_code is None:
            raise HTTPException(
                status_code=500, 
                detail="Reset code feature not configured. Please run the database migration: python migrations/run_add_reset_code_migration.py"
            )
        
        # Verify reset code
        if user.reset_code != code:
            raise HTTPException(status_code=400, detail="Invalid reset code")
        
        # Check if code has expired
        if user.reset_code_expires_at and user.reset_code_expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Reset code has expired. Please request a new one.")
        
        return {"message": "Reset code is valid", "valid": True}
    except HTTPException:
        raise
    except Exception as e:
        # Catch database errors (missing columns, etc.)
        import traceback
        error_msg = str(e)
        if 'reset_code' in error_msg.lower() or 'column' in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail="Database error: Reset code columns may not exist. Please run: python migrations/run_add_reset_code_migration.py"
            )
        raise HTTPException(status_code=500, detail=f"Error validating reset code: {error_msg}")


# ----------------------------------------------------
# Reset Password (with validated code)
# ----------------------------------------------------
def reset_password(db: Session, email: str, code: str, new_password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify reset code again (security check)
    if user.reset_code != code:
        raise HTTPException(status_code=400, detail="Invalid reset code")
    
    # Check if code has expired
    if user.reset_code_expires_at and user.reset_code_expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset code has expired. Please request a new one.")
    
    # Validate and update password
    validate_password(new_password)
    user.hashed_password = Hash.hash(new_password)
    
    # Clear reset code after successful reset
    user.reset_code = None
    user.reset_code_expires_at = None
    
    db.commit()

    return {"message": "Password updated successfully"}


# ----------------------------------------------------
# Change Password (requires current password)
# ----------------------------------------------------
def change_password(db: Session, user_id: int, current_password: str, new_password: str):
    """Change password for logged-in user. Requires current password verification."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not Hash.verify(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Validate new password
    validate_password(new_password)
    
    # Update password
    user.hashed_password = Hash.hash(new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


# ----------------------------------------------------
# Resend Verification Email
# ----------------------------------------------------
def resend_verification_email(db: Session, user_id: int):
    """Resend email verification code to user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_email_verified:
        raise HTTPException(status_code=400, detail="Email is already verified")
    
    # Generate new 6-digit verification code
    verification_code = generate_verification_code()
    user.verification_code = verification_code
    user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    db.commit()
    
    # Generate and send verification email
    try:
        html = generate_verification_email(user.email, verification_code)
        send_email(
            to_email=user.email,
            subject="Verify your StatHub account",
            html_content=html
        )
        return {"message": "Verification email sent successfully"}
    except Exception as e:
        print(f"⚠️ Email sending failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email")
