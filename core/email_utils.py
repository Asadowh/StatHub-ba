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
# Placeholder Send Function
# (You can replace with actual SMTP or SendGrid later)
# ------------------------------------------------------
def send_email(to_email: str, subject: str, html_content: str):
    print("------ EMAIL SEND SIMULATION ------")
    print("To:", to_email)
    print("Subject:", subject)
    print("HTML Content:", html_content)
    print("------ END EMAIL ------")
    # In production:
    # integrate SendGrid / SMTP here
