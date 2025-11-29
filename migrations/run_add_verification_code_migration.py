"""
Migration script to add verification_code columns to users table.
Run this script: python migrations/run_add_verification_code_migration.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database import engine

def run_migration():
    """Add verification_code and verification_code_expires_at columns to users table if they don't exist"""
    print("Running migration: Adding verification_code columns to users table...")
    
    try:
        with engine.connect() as conn:
            # Check if columns already exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name IN ('verification_code', 'verification_code_expires_at')
            """)
            result = conn.execute(check_query)
            existing_columns = [row[0] for row in result]
            
            # Add verification_code column if it doesn't exist
            if 'verification_code' not in existing_columns:
                alter_query1 = text("""
                    ALTER TABLE users 
                    ADD COLUMN verification_code VARCHAR(6) NULL
                """)
                conn.execute(alter_query1)
                conn.commit()
                print("✅ Successfully added 'verification_code' column to 'users' table!")
            else:
                print("✅ Column 'verification_code' already exists. Skipping.")
            
            # Add verification_code_expires_at column if it doesn't exist
            if 'verification_code_expires_at' not in existing_columns:
                alter_query2 = text("""
                    ALTER TABLE users 
                    ADD COLUMN verification_code_expires_at TIMESTAMP WITH TIME ZONE NULL
                """)
                conn.execute(alter_query2)
                conn.commit()
                print("✅ Successfully added 'verification_code_expires_at' column to 'users' table!")
            else:
                print("✅ Column 'verification_code_expires_at' already exists. Skipping.")
            
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        raise

if __name__ == "__main__":
    run_migration()
    print("Migration complete!")

