import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import settings
from utils.email_templates import (
    verification_email_template,
    reset_password_template,
)
from utils.jwt_handler import create_email_token, create_reset_token


# ------------------------------------------------------
# Generate Email Verification Link
# ------------------------------------------------------
def generate_verification_email(email: str):
    token = create_email_token(email)
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    html = verification_email_template(verification_url)
    return html, token


# ------------------------------------------------------
# Generate Password Reset Link
# ------------------------------------------------------
def generate_reset_email(email: str):
    token = create_reset_token(email)
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    html = reset_password_template(reset_url)
    return html, token


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
            server.sendmail(settings.SMTP_USER, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise
