# Reset Code Migration Check

## Important: Run This Migration First!

Before using the password reset feature, you must run the database migration to add the `reset_code` columns to the `users` table.

### Steps:

1. Navigate to the backend directory:
   ```bash
   cd C:\Users\vaqif\OneDrive\Desktop\StatHub-backend
   ```

2. Run the migration script:
   ```bash
   python migrations/run_add_reset_code_migration.py
   ```

3. Restart your backend server

### What This Does:

- Adds `reset_code VARCHAR(6) NULL` column to `users` table
- Adds `reset_code_expires_at TIMESTAMP WITH TIME ZONE NULL` column to `users` table

### If You Skip This:

The password reset feature will fail with database errors because the columns don't exist!


