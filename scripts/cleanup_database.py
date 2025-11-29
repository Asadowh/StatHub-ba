"""
Database Cleanup Script
This script deletes all users except admins and all matches from the database.

WARNING: This is a destructive operation. Use with caution!
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.match import Match
from models.stat import Stat
from models.rating import Rating
from models.reaction import Reaction
from models.comment import Comment
from models.trophy import Trophy
from models.news import News

def cleanup_database():
    """Delete all non-admin users and all matches from the database."""
    db: Session = SessionLocal()
    
    try:
        print("🧹 Starting database cleanup...")
        print("=" * 60)
        
        # Step 1: Get admin users to preserve
        admin_users = db.query(User).filter(User.role == "admin").all()
        admin_user_ids = [user.id for user in admin_users]
        admin_count = len(admin_users)
        
        print(f"\n📊 Found {admin_count} admin user(s) to preserve:")
        for admin in admin_users:
            print(f"   - {admin.username} ({admin.email})")
        
        # Step 2: Delete all matches and related data
        print("\n🗑️  Deleting all matches and related data...")
        
        # Delete stats (related to matches)
        stats_count = db.query(Stat).count()
        db.query(Stat).delete()
        print(f"   ✓ Deleted {stats_count} stats")
        
        # Delete ratings (related to matches)
        ratings_count = db.query(Rating).count()
        db.query(Rating).delete()
        print(f"   ✓ Deleted {ratings_count} ratings")
        
        # Delete reactions (related to matches)
        reactions_count = db.query(Reaction).filter(Reaction.match_id != None).count()
        db.query(Reaction).filter(Reaction.match_id != None).delete()
        print(f"   ✓ Deleted {reactions_count} match reactions")
        
        # Delete comments (related to matches)
        comments_count = db.query(Comment).filter(Comment.match_id != None).count()
        db.query(Comment).filter(Comment.match_id != None).delete()
        print(f"   ✓ Deleted {comments_count} match comments")
        
        # Delete trophies (related to matches)
        trophies_count = db.query(Trophy).count()
        db.query(Trophy).delete()
        print(f"   ✓ Deleted {trophies_count} trophies")
        
        # Delete matches
        matches_count = db.query(Match).count()
        db.query(Match).delete()
        print(f"   ✓ Deleted {matches_count} matches")
        
        # Step 3: Delete all non-admin users and related data
        print("\n🗑️  Deleting all non-admin users and related data...")
        
        # Get all non-admin users
        non_admin_users = db.query(User).filter(User.role != "admin").all()
        non_admin_user_ids = [user.id for user in non_admin_users]
        non_admin_count = len(non_admin_users)
        
        print(f"   Found {non_admin_count} non-admin user(s) to delete")
        
        if non_admin_count > 0:
            # Delete reactions by non-admin users (news-related, match reactions already deleted)
            user_reactions_count = db.query(Reaction).filter(
                Reaction.user_id.in_(non_admin_user_ids)
            ).count()
            db.query(Reaction).filter(Reaction.user_id.in_(non_admin_user_ids)).delete()
            print(f"   ✓ Deleted {user_reactions_count} user reactions")
            
            # Delete comments by non-admin users (news-related, match comments already deleted)
            user_comments_count = db.query(Comment).filter(
                Comment.author_id.in_(non_admin_user_ids)
            ).count()
            db.query(Comment).filter(Comment.author_id.in_(non_admin_user_ids)).delete()
            print(f"   ✓ Deleted {user_comments_count} user comments")
            
            # Delete news created by non-admin users
            news_count = db.query(News).filter(News.author_id.in_(non_admin_user_ids)).count()
            db.query(News).filter(News.author_id.in_(non_admin_user_ids)).delete()
            print(f"   ✓ Deleted {news_count} news posts by non-admin users")
            
            # Delete non-admin users
            deleted_users = db.query(User).filter(User.role != "admin").delete()
            print(f"   ✓ Deleted {deleted_users} non-admin users")
        
        # Commit all changes
        db.commit()
        
        print("\n" + "=" * 60)
        print("✅ Database cleanup completed successfully!")
        print(f"   - Preserved: {admin_count} admin user(s)")
        print(f"   - Deleted: {non_admin_count} non-admin user(s)")
        print(f"   - Deleted: {matches_count} match(es)")
        
        # Verify results
        remaining_users = db.query(User).count()
        remaining_matches = db.query(Match).count()
        
        print(f"\n📊 Current database state:")
        print(f"   - Total users: {remaining_users}")
        print(f"   - Total matches: {remaining_matches}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during cleanup: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Safety confirmation
    print("⚠️  WARNING: This will delete all non-admin users and all matches!")
    print("   This action cannot be undone.\n")
    
    confirmation = input("Are you sure you want to continue? (type 'yes' to confirm): ")
    
    if confirmation.lower() == 'yes':
        cleanup_database()
    else:
        print("❌ Cleanup cancelled.")

