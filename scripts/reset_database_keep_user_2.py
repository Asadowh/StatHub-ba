"""
Database Reset Script - Keep Only User ID 2
This script will:
1. Backup user with id 2
2. Drop all tables
3. Recreate all tables
4. Restore only user with id 2

WARNING: This is a destructive operation. Use with caution!

IMPORTANT: Stop your FastAPI backend server before running this script!
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine, Base
from models.user import User
from datetime import date
import time

def reset_database_keep_user_2():
    """Reset database, keeping only user with id 2."""
    db: Session = SessionLocal()
    
    try:
        print("🔄 Starting database reset...")
        print("=" * 60)
        
        # Step 1: Backup user with id 2
        print("\n📦 Step 1: Backing up user with id 2...")
        user_2 = db.query(User).filter(User.id == 2).first()
        
        if not user_2:
            print("❌ ERROR: User with id 2 not found!")
            print("   Cannot proceed without user id 2.")
            return
        
        # Create backup dictionary
        user_backup = {
            'username': user_2.username,
            'email': user_2.email,
            'hashed_password': user_2.hashed_password,
            'full_name': user_2.full_name,
            'photo_url': user_2.photo_url,
            'height': user_2.height,
            'jersey_number': user_2.jersey_number,
            'nationality': user_2.nationality,
            'birth_date': user_2.birth_date.isoformat() if user_2.birth_date else None,
            'favorite_position': user_2.favorite_position,
            'personal_quote': user_2.personal_quote,
            'role': user_2.role,
            'is_active': user_2.is_active,
            'is_email_verified': user_2.is_email_verified,
            'xp': user_2.xp,
            'level': user_2.level,
        }
        
        print(f"   ✓ Backed up user: {user_2.username} ({user_2.email})")
        print(f"   - Role: {user_2.role}")
        
        # Step 2: Close session and drop all tables
        print("\n🗑️  Step 2: Dropping all tables...")
        
        # Close the current session
        db.close()
        
        # Dispose all connections from the engine
        engine.dispose()
        
        # Wait a moment for connections to close
        time.sleep(2)
        
        # Get all table names
        print("   Getting list of tables...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]
        
        print(f"   Found {len(tables)} table(s) to drop:")
        for table in tables:
            print(f"   - {table}")
        
        # Drop all tables with CASCADE
        print("\n   Dropping tables one by one...")
        dropped_count = 0
        with engine.begin() as conn:
            for table in tables:
                try:
                    conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                    dropped_count += 1
                    print(f"   ✓ Dropped {table} ({dropped_count}/{len(tables)})")
                except Exception as e:
                    print(f"   ⚠️  Error dropping {table}: {str(e)}")
        
        print(f"\n   ✓ Dropped {dropped_count}/{len(tables)} tables")
        
        # Verify all tables are dropped
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """))
            remaining_tables = [row[0] for row in result]
        
        if remaining_tables:
            print(f"   ⚠️  Warning: {len(remaining_tables)} table(s) still exist: {remaining_tables}")
        else:
            print("   ✓ All tables dropped successfully")
        
        # Step 3: Recreate all tables
        print("\n🔨 Step 3: Recreating all tables...")
        
        # Import all models to ensure they're registered
        import models.user
        import models.match
        import models.stat
        import models.rating
        import models.trophy
        import models.news
        import models.comment
        import models.reaction
        import models.achievement
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("   ✓ All tables recreated successfully")
        
        # Step 4: Restore user with id 2
        print("\n📥 Step 4: Restoring user with id 2...")
        
        # Create new session
        db = SessionLocal()
        
        # Parse birth_date if it exists
        birth_date_value = None
        if user_backup['birth_date']:
            try:
                birth_date_value = date.fromisoformat(user_backup['birth_date'])
            except:
                birth_date_value = None
        
        # Use raw SQL to insert with specific ID 2
        db.execute(text("""
            INSERT INTO users (
                id, username, email, hashed_password, full_name, photo_url,
                height, jersey_number, nationality, birth_date, favorite_position,
                personal_quote, role, is_active, is_email_verified, xp, level,
                created_at
            ) VALUES (
                :id, :username, :email, :hashed_password, :full_name, :photo_url,
                :height, :jersey_number, :nationality, :birth_date, :favorite_position,
                :personal_quote, :role, :is_active, :is_email_verified, :xp, :level,
                NOW()
            )
        """), {
            'id': 2,
            'username': user_backup['username'],
            'email': user_backup['email'],
            'hashed_password': user_backup['hashed_password'],
            'full_name': user_backup['full_name'],
            'photo_url': user_backup['photo_url'],
            'height': user_backup['height'],
            'jersey_number': user_backup['jersey_number'],
            'nationality': user_backup['nationality'],
            'birth_date': birth_date_value,
            'favorite_position': user_backup['favorite_position'],
            'personal_quote': user_backup['personal_quote'],
            'role': user_backup['role'],
            'is_active': user_backup['is_active'],
            'is_email_verified': user_backup['is_email_verified'],
            'xp': user_backup['xp'] or 0,
            'level': user_backup['level'] or 1,
        })
        
        # Reset the sequence for users table
        try:
            db.execute(text("SELECT setval('users_id_seq', GREATEST(2, COALESCE((SELECT MAX(id) FROM users), 2)))"))
        except Exception as e:
            # Sequence might not exist yet, that's okay
            print(f"   ⚠️  Note: Could not reset sequence: {str(e)}")
        
        db.commit()
        
        # Verify the user was created with id 2
        restored_user = db.query(User).filter(User.id == 2).first()
        if restored_user:
            print(f"   ✓ User restored: {restored_user.username} (ID: {restored_user.id})")
            print(f"   - Email: {restored_user.email}")
            print(f"   - Role: {restored_user.role}")
        else:
            print("   ⚠️  Warning: User was created but couldn't verify ID 2")
        
        # Step 5: Verify
        print("\n📊 Step 5: Verification...")
        remaining_users = db.query(User).count()
        
        print(f"   ✓ Total users in database: {remaining_users}")
        print(f"   ✓ User ID 2 exists: {db.query(User).filter(User.id == 2).first() is not None}")
        
        print("\n" + "=" * 60)
        print("✅ Database reset completed successfully!")
        print(f"   - User with id 2 has been preserved")
        print(f"   - All other data has been removed")
        print(f"   - All tables have been recreated fresh")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during database reset: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    # Safety confirmation
    print("⚠️  WARNING: This will DROP ALL TABLES and DELETE ALL DATA!")
    print("   Only user with id 2 will be preserved.")
    print("   This action CANNOT be undone.\n")
    
    print("⚠️  IMPORTANT: Make sure your FastAPI backend server is STOPPED!")
    print("   The backend server holds database connections that can prevent table drops.\n")
    
    print("This will:")
    print("  1. Backup user with id 2")
    print("  2. Drop ALL tables in the database")
    print("  3. Recreate all tables (empty)")
    print("  4. Restore only user with id 2\n")
    
    confirmation = input("Are you absolutely sure? Type 'yes' to confirm: ")
    
    if confirmation.lower() == 'yes':
        reset_database_keep_user_2()
    else:
        print("❌ Database reset cancelled.")
