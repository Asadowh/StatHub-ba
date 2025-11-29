# 📧 Email Configuration Guide

## Where to Change the Email Sender Address

The email sender is configured in your **`.env`** file in the backend root directory.

### Location:
```
C:\Users\vaqif\OneDrive\Desktop\StatHub-backend\.env
```

### Required Variables:

```env
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com          # ← CHANGE THIS: Your email address
SMTP_PASSWORD=your-app-password          # ← CHANGE THIS: App password (see below)
EMAIL_FROM=your-email@gmail.com          # ← CHANGE THIS: Same as SMTP_USER usually
```

The code reads these from: `core/config.py` (lines 17-22)

---

## 📝 How to Set Up Gmail:

1. **Enable 2-Factor Authentication** on your Google Account
2. **Generate an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this in `SMTP_PASSWORD` (not your regular password!)

3. **Update your `.env` file**:
   ```env
   SMTP_USER=yourname@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # The app password from step 2
   EMAIL_FROM=yourname@gmail.com
   ```

---

## ✅ Verification System Changed to 6-Digit Codes

The system now sends **6-digit verification codes** instead of links!

- ✅ Users receive email with 6-digit code
- ✅ Code expires after 15 minutes
- ✅ Users enter code in verification page

---

## 🚀 Next Steps:

1. **Run database migration** to add verification code columns:
   ```bash
   python migrations/run_add_verification_code_migration.py
   ```

2. **Update your `.env` file** with your email credentials

3. **Restart your backend server**

4. **Test** by creating a new account or requesting a verification email from Settings

---

## 📧 Email Preview:

Users will receive an email like this:

```
⚽ Welcome to StatHub!

Thanks for signing up! Please verify your email address using the code below:

┌─────────────────┐
│   123456        │  ← 6-digit code
└─────────────────┘

Enter this code in the verification page to complete your registration.
```

---

## 🔧 Troubleshooting:

- **Emails not sending?** Check your `.env` file has correct credentials
- **SMTP error?** Verify your app password is correct (not your regular password)
- **Code not working?** Codes expire after 15 minutes - request a new one

