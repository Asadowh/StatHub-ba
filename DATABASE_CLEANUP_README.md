# Database Cleanup Script

## Overview
This script deletes all users except admins and all matches from the database.

## What It Does
1. **Preserves Admin Users**: Keeps all users with `role = "admin"`
2. **Deletes All Matches**: Removes all matches and related data (stats, ratings, reactions, comments, trophies)
3. **Deletes Non-Admin Users**: Removes all users except admins and their related data (achievements, reactions, comments, stats, ratings, news posts)

## How to Run

### Step 1: Navigate to Backend Directory
```bash
cd C:\Users\vaqif\OneDrive\Desktop\StatHub-backend
```

### Step 2: Run the Cleanup Script
```bash
python scripts/cleanup_database.py
```

### Step 3: Confirm
The script will ask for confirmation. Type `yes` to proceed.

## Safety Features
- ✅ Requires explicit confirmation before deleting
- ✅ Shows exactly what will be deleted
- ✅ Preserves all admin users automatically
- ✅ Handles foreign key relationships safely
- ✅ Provides detailed output of what was deleted

## What Gets Deleted

### Matches and Related:
- All matches
- All stats (match-related)
- All ratings (match-related)
- All match reactions
- All match comments
- All trophies

### Non-Admin Users and Related:
- All non-admin users
- All achievements (for deleted users)
- All user reactions
- All user comments
- All user stats
- All user ratings
- All news posts created by non-admin users

## What Gets Preserved
- ✅ All admin users (users with `role = "admin"`)
- ✅ News posts created by admin users

## Example Output
```
🧹 Starting database cleanup...
============================================================

📊 Found 1 admin user(s) to preserve:
   - admin (admin@stathub.team)

🗑️  Deleting all matches and related data...
   ✓ Deleted 25 stats
   ✓ Deleted 15 ratings
   ✓ Deleted 10 match reactions
   ✓ Deleted 5 match comments
   ✓ Deleted 8 trophies
   ✓ Deleted 12 matches

🗑️  Deleting all non-admin users and related data...
   Found 50 non-admin user(s) to delete
   ✓ Deleted 120 achievements
   ✓ Deleted 30 user reactions
   ✓ Deleted 15 user comments
   ✓ Deleted 25 user stats
   ✓ Deleted 20 user ratings
   ✓ Deleted 5 news posts by non-admin users
   ✓ Deleted 50 non-admin users

============================================================
✅ Database cleanup completed successfully!
   - Preserved: 1 admin user(s)
   - Deleted: 50 non-admin user(s)
   - Deleted: 12 match(es)

📊 Current database state:
   - Total users: 1
   - Total matches: 0
```

## ⚠️ WARNING
**This action is irreversible!** Make sure you have a database backup if needed before running this script.


