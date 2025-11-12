from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # fallback just in case
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour token lifespan


def create_access_token(data: dict):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    """
    Verify and decode a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
# --- Email Verification Token Helpers ---

EMAIL_TOKEN_EXPIRE_HOURS = 24  # token valid for 1 day

def create_email_token(email: str):
    """
    Create a JWT token used for email verification.
    Encodes the user's email and an expiry time.
    """
    expire = datetime.utcnow() + timedelta(hours=EMAIL_TOKEN_EXPIRE_HOURS)
    payload = {"sub": email, "exp": expire, "type": "email_verification"}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_email_token(token: str):
    """
    Verify an email verification token and return the email if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "email_verification":
            return None  # not a verification token
        return payload.get("sub")  # return email
    except JWTError:
        return None


if __name__ == "__main__":
    test_email = "omar@gmail.com"
    token = create_email_token(test_email)
    print("Generated Token:", token)

    decoded = verify_email_token(token)
    print("Decoded Email:", decoded)
