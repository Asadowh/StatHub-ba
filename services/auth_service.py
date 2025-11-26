from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from utils.hashing import Hash
from utils.jwt_handler import create_access_token, verify_email_token, verify_reset_token
from core.security import validate_password
from core.email_utils import generate_verification_email, generate_reset_email, send_email


# ----------------------------------------------------
# Create User (Signup)
# ----------------------------------------------------
def register_user(db: Session, data):
    # Check email
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    # Check username
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Validate password
    validate_password(data.password)

    new_user = User(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        hashed_password=Hash.hash(data.password),
        is_active=True,
        is_email_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate verification email
    html, token = generate_verification_email(data.email)
    send_email(
        to_email=data.email,
        subject="Verify your StatHub account",
        html_content=html
    )

    return new_user


# ----------------------------------------------------
# Login
# ----------------------------------------------------
def login_user(db: Session, data):
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


# ----------------------------------------------------
# Email Verification
# ----------------------------------------------------
def verify_email(db: Session, token: str):
    email = verify_email_token(token)
    if email is None:
        raise HTTPException(status_code=400, detail="Invalid email verification token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_email_verified = True
    db.commit()

    return {"message": "Email verified successfully"}


# ----------------------------------------------------
# Forgot Password
# ----------------------------------------------------
def send_reset_password_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    html, token = generate_reset_email(email)
    send_email(email, "Reset your password", html)

    return {"message": "Password reset email sent"}


# ----------------------------------------------------
# Reset Password
# ----------------------------------------------------
def reset_password(db: Session, token: str, new_password: str):
    email = verify_reset_token(token)
    if email is None:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    validate_password(new_password)
    user.hashed_password = Hash.hash(new_password)
    db.commit()

    return {"message": "Password updated successfully"}
