def verification_email_template(verification_url: str):
    return f"""
    <h2>Verify Your Email</h2>
    <p>Click the link below to verify your account:</p>
    <a href="{verification_url}">Verify Email</a>
    """


def reset_password_template(reset_url: str):
    return f"""
    <h2>Reset Your Password</h2>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_url}">Reset Password</a>
    """ 
