"""
Migration script to add category column to news table.
Run this script to add the category field to the news table.
"""
import sys
import os

# Add parent directory to path to import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from sqlalchemy import text

def run_migration():
    """Add category column to news table."""
    print("Running migration: Adding category column to news table...")
    
    try:
        with engine.connect() as conn:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'news' AND column_name = 'category'
            """)
            result = conn.execute(check_query)
            exists = result.fetchone() is not None
            
            if exists:
                print("✅ Column 'category' already exists in 'news' table. Skipping migration.")
                return
            
            # Add the column
            alter_query = text("""
                ALTER TABLE news 
                ADD COLUMN category VARCHAR(50) NULL
            """)
            conn.execute(alter_query)
            conn.commit()
            
            print("✅ Successfully added 'category' column to 'news' table!")
            
            # Verify the column was added
            verify_result = conn.execute(check_query)
            if verify_result.fetchone():
                print("✅ Verified: category column exists in news table")
                
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        raise

if __name__ == "__main__":
    print("Running migration: Add category column to news table...")
    run_migration()
    print("Migration complete!")

