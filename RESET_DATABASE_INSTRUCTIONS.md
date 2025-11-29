# Database Reset - Keep User ID 2

## ⚠️ IMPORTANT: Stop Backend Server First!

**Before running the reset script, you MUST stop your FastAPI backend server!**

The backend server holds database connections that will prevent tables from being dropped, causing the script to hang.

### Steps:

1. **Stop your backend server** (Ctrl+C in the terminal where it's running)

2. **Wait a few seconds** for connections to close

3. **Run the reset script:**
   ```bash
   cd C:\Users\vaqif\OneDrive\Desktop\StatHub-backend
   python scripts/reset_database_keep_user_2.py
   ```

4. **After the script completes**, you can restart your backend server

## What If It Still Hangs?

If the script still hangs even after stopping the backend:

1. **Check for other connections:**
   - Make sure no other Python scripts are using the database
   - Close any database management tools (pgAdmin, DBeaver, etc.)
   - Make sure no other backend instances are running

2. **Alternative: Use the simpler cleanup script instead:**
   ```bash
   python scripts/cleanup_database.py
   ```
   This deletes all data but keeps the tables (faster, less likely to hang)

## Troubleshooting

- **Script hangs on "Dropping tables"**: Backend server or other connections are still active
- **Error about connections**: Close all database clients and try again
- **Permission errors**: Check your database user has DROP TABLE permissions



