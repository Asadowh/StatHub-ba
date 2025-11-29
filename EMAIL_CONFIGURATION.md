# Email Configuration Guide

## Where to Change the Email Sender

The email sender configuration is in **`.env`** file in your backend root directory.

### Required Environment Variables:

```env
# SMTP Configuration (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com

# Frontend URL (for email links - not used for code verification)
FRONTEND_URL=http://localhost:8080
```

### File Location:
- Configuration file: `C:\Users\vaqif\OneDrive\Desktop\StatHub-backend\core\config.py`
- These values are read from your `.env` file

### How to Set Up Gmail:
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an "App Password" for email
4. Use that app password in `SMTP_PASSWORD`
5. Use your Gmail address in `SMTP_USER` and `EMAIL_FROM`

### For Other Email Providers:
- **Outlook/Hotmail**: 
  - SMTP_HOST=smtp-mail.outlook.com
  - SMTP_PORT=587

- **Yahoo**: 
  - SMTP_HOST=smtp.mail.yahoo.com
  - SMTP_PORT=587

- **Custom SMTP**: Check your email provider's documentation

---

## Verification System Changed to 6-Digit Codes

✅ **The system now sends 6-digit verification codes instead of links!**

- Users receive an email with a 6-digit code
- They enter the code in the verification page
- Codes expire after 15 minutes



