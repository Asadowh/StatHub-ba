"""
Migration script to add image_url column to news table
Run this script: python migrations/run_migration.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database import engine

def run_migration():
    """Add image_url column to news table if it doesn't exist"""
    print("Running migration: Adding image_url to news table...")
    
    try:
        with engine.connect() as conn:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'news' AND column_name = 'image_url'
            """)
            result = conn.execute(check_query)
            exists = result.fetchone() is not None
            
            if exists:
                print("Column 'image_url' already exists in 'news' table. Skipping migration.")
                return
            
            # Add the column
            alter_query = text("""
                ALTER TABLE news 
                ADD COLUMN image_url VARCHAR
            """)
            conn.execute(alter_query)
            conn.commit()
            
            print("Successfully added 'image_url' column to 'news' table!")
            
    except Exception as e:
        print(f"Error running migration: {e}")
        raise

if __name__ == "__main__":
    run_migration()

