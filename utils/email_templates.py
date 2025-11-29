def verification_email_template(verification_code: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 500px; margin: 0 auto; background: #fff; border-radius: 10px; padding: 30px; }}
            h2 {{ color: #1a1a2e; }}
            .code-box {{ background: #f0f0f0; border: 2px dashed #4f46e5; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
            .code {{ font-size: 32px; font-weight: bold; color: #4f46e5; letter-spacing: 8px; font-family: 'Courier New', monospace; }}
            .footer {{ margin-top: 30px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>⚽ Welcome to StatHub!</h2>
            <p>Thanks for signing up! Please verify your email address using the code below:</p>
            <div class="code-box">
                <div class="code">{verification_code}</div>
            </div>
            <p>Enter this code in the verification page to complete your registration.</p>
            <p class="footer">This code expires in 15 minutes. If you didn't create this account, you can ignore this email.</p>
        </div>
    </body>
    </html>
    """


def reset_password_template(reset_code: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 500px; margin: 0 auto; background: #fff; border-radius: 10px; padding: 30px; }}
            h2 {{ color: #1a1a2e; }}
            .code-box {{ background: #f0f0f0; border: 2px dashed #4f46e5; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
            .code {{ font-size: 32px; font-weight: bold; color: #4f46e5; letter-spacing: 8px; font-family: 'Courier New', monospace; }}
            .footer {{ margin-top: 30px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔑 Reset Your Password</h2>
            <p>We received a request to reset your password. Use the code below to reset your password:</p>
            <div class="code-box">
                <div class="code">{reset_code}</div>
            </div>
            <p>Enter this code on the password reset page along with your new password.</p>
            <p class="footer">This code expires in 15 minutes. If you didn't request this, ignore this email.</p>
        </div>
    </body>
    </html>
    """


def email_verified_welcome_template(user_name: str = None):
    """Welcome email template sent after email verification"""
    greeting = f"Hey {user_name}!" if user_name else "Hey there!"
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; margin: 0; }}
            .wrapper {{ max-width: 600px; margin: 0 auto; }}
            .container {{ background: #ffffff; border-radius: 16px; padding: 40px 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .icon {{ font-size: 64px; margin-bottom: 20px; }}
            h1 {{ color: #1a1a2e; margin: 0; font-size: 28px; font-weight: 700; }}
            .subtitle {{ color: #4f46e5; font-size: 18px; margin-top: 10px; font-weight: 600; }}
            .content {{ color: #333; line-height: 1.6; font-size: 16px; }}
            .success-box {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 20px; border-radius: 12px; text-align: center; margin: 30px 0; }}
            .success-box h2 {{ margin: 0; font-size: 24px; color: white; }}
            .features {{ margin: 30px 0; }}
            .feature-item {{ display: flex; align-items: center; margin: 15px 0; padding: 12px; background: #f8fafc; border-radius: 8px; }}
            .feature-icon {{ font-size: 24px; margin-right: 12px; }}
            .feature-text {{ color: #1a1a2e; font-size: 15px; }}
            .cta-button {{ display: inline-block; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 14px 32px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; margin: 20px 0; text-align: center; }}
            .cta-container {{ text-align: center; margin: 30px 0; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280; font-size: 14px; line-height: 1.5; }}
            .footer a {{ color: #4f46e5; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="container">
                <div class="header">
                    <div class="icon">⚽</div>
                    <h1>Welcome to StatHub!</h1>
                    <div class="subtitle">Your Email is Verified ✅</div>
                </div>
                
                <div class="content">
                    <p>{greeting}</p>
                    <p>Great news! Your email address has been successfully verified. You're all set to start your journey with StatHub!</p>
                    
                    <div class="success-box">
                        <h2>🎉 You're All Set!</h2>
                        <p style="margin: 10px 0 0 0; opacity: 0.95;">Your account is now fully activated</p>
                    </div>
                    
                    <p>Now you can:</p>
                    
                    <div class="features">
                        <div class="feature-item">
                            <span class="feature-icon">📊</span>
                            <span class="feature-text">Track your match statistics and performance</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">🏆</span>
                            <span class="feature-text">Earn achievements and climb the leaderboard</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">📰</span>
                            <span class="feature-text">Stay updated with team news and updates</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">👥</span>
                            <span class="feature-text">Connect with your teammates and see their progress</span>
                        </div>
                    </div>
                    
                    <div class="cta-container">
                        <a href="http://localhost:8080" class="cta-button">Get Started Now →</a>
                    </div>
                    
                    <p style="margin-top: 30px;">We're excited to have you on board! Have fun tracking your progress and achieving your goals. 🚀</p>
                    
                    <p style="margin-top: 20px;">If you have any questions or need help, feel free to reach out to us anytime.</p>
                    
                    <p style="margin-top: 20px;">Best regards,<br><strong>The StatHub Team</strong></p>
                </div>
                
                <div class="footer">
                    <p>You're receiving this email because you just verified your email address on StatHub.</p>
                    <p>© 2024 StatHub. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """ 
