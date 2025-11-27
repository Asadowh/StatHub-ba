def verification_email_template(verification_url: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 500px; margin: 0 auto; background: #fff; border-radius: 10px; padding: 30px; }}
            h2 {{ color: #1a1a2e; }}
            .btn {{ display: inline-block; background: #4f46e5; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin-top: 20px; }}
            .footer {{ margin-top: 30px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>⚽ Welcome to StatHub!</h2>
            <p>Thanks for signing up! Please verify your email address to get started.</p>
            <a href="{verification_url}" class="btn">Verify Email</a>
            <p class="footer">If you didn't create this account, you can ignore this email.</p>
        </div>
    </body>
    </html>
    """


def reset_password_template(reset_url: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 500px; margin: 0 auto; background: #fff; border-radius: 10px; padding: 30px; }}
            h2 {{ color: #1a1a2e; }}
            .btn {{ display: inline-block; background: #4f46e5; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin-top: 20px; }}
            .footer {{ margin-top: 30px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔑 Reset Your Password</h2>
            <p>We received a request to reset your password. Click the button below to set a new password.</p>
            <a href="{reset_url}" class="btn">Reset Password</a>
            <p class="footer">This link expires in 30 minutes. If you didn't request this, ignore this email.</p>
        </div>
    </body>
    </html>
    """ 
