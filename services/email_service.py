from core.email_utils import send_email

def send(to: str, subject: str, html: str):
    send_email(to, subject, html)
