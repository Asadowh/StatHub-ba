import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import settings
from utils.email_templates import (
    verification_email_template,
    reset_password_template,
    email_verified_welcome_template,
)
from utils.jwt_handler import create_email_token, create_reset_token


# ------------------------------------------------------
# Generate Email Verification Code (6 digits)
# ------------------------------------------------------
import random

def generate_verification_code() -> str:
    """Generate a random 6-digit verification code."""
    return str(random.randint(100000, 999999))

def generate_verification_email(email: str, code: str):
    """Generate verification email with 6-digit code."""
    html = verification_email_template(code)
    return html


# ------------------------------------------------------
# Generate Password Reset Code (6 digits)
# ------------------------------------------------------
def generate_reset_email(email: str, code: str):
    """Generate password reset email with 6-digit code."""
    html = reset_password_template(code)
    return html


# ------------------------------------------------------
# Generate Welcome Email (after verification)
# ------------------------------------------------------
def generate_welcome_email(user_name: str = None):
    """Generate welcome email after email verification."""
    html = email_verified_welcome_template(user_name)
    return html


# ------------------------------------------------------
# Send Email via SMTP (Gmail)
# ------------------------------------------------------
def send_email(to_email: str, subject: str, html_content: str):
    # Check if SMTP is configured
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("⚠️  SMTP not configured - Email simulation:")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        return

    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM or settings.SMTP_USER
        msg["To"] = to_email

        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        # Connect to SMTP server and send
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM or settings.SMTP_USER, [to_email], msg.as_string())

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise
