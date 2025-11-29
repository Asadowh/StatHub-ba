"""
Script to seed achievements into the database.
This script inserts the following achievements if they do not already exist:
- 5 Beginner Missions
- 3 Advanced Missions  
- 1 Expert Mission

Achievements are inserted without creating duplicates.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
from models.achievement import Achievement
from models.user import User
from models.stat import Stat  # Import to ensure relationships are set up
from models.match import Match  # Import to ensure relationships are set up
from services.achievement_checker import check_and_unlock_achievements

# Define all achievements exactly as specified
ACHIEVEMENTS = [
    # ⭐ Beginner Missions
    {
        "name": "First Match",
        "description": "Play your first recorded match.",
        "tier": "Beginner",
        "metric": "matches",
        "target_value": 1,
        "points": 100
    },
    {
        "name": "Helping Hand",
        "description": "Register your first assist.",
        "tier": "Beginner",
        "metric": "assists",
        "target_value": 1,
        "points": 100
    },
    {
        "name": "Maiden Goal",
        "description": "Score your first goal.",
        "tier": "Beginner",
        "metric": "goals",
        "target_value": 1,
        "points": 150
    },
    {
        "name": "Five-Goal Club",
        "description": "Reach a total of 5 goals.",
        "tier": "Beginner",
        "metric": "goals",
        "target_value": 5,
        "points": 150
    },
    {
        "name": "Reliable Starter",
        "description": "Participate in 5 matches.",
        "tier": "Beginner",
        "metric": "matches",
        "target_value": 5,
        "points": 200
    },
    # 🔥 Advanced Missions
    {
        "name": "Hat-trick Hero",
        "description": "Score 3 goals in a single match.",
        "tier": "Advanced",
        "metric": "goals_per_match",
        "target_value": 3,
        "points": 300
    },
    {
        "name": "Goal Machine",
        "description": "Reach a total of 30 goals.",
        "tier": "Advanced",
        "metric": "goals",
        "target_value": 30,
        "points": 400
    },
    {
        "name": "Elite Performer",
        "description": "Maintain an average rating of 7.5+ across 5 matches.",
        "tier": "Advanced",
        "metric": "rating",
        "target_value": 75,  # Stored as 75 (7.5 * 10) since target_value is Integer
        "points": 500
    },
    # 💀 Expert Mission
    {
        "name": "Century Scorer",
        "description": "Reach a total of 100 goals.",
        "tier": "Expert",
        "metric": "goals",
        "target_value": 100,
        "points": 1000
    },
]


def seed_achievements(db: Session = None, check_existing_players: bool = True):
    """
    Seed achievements into the database.
    
    Args:
        db: Database session (if None, creates a new one)
        check_existing_players: If True, checks and unlocks achievements for existing players
    
    Returns:
        tuple: (new_achievements_count, updated_achievements_count)
    """
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        # Check which achievements already exist by name
        existing_achievements = {a.name: a for a in db.query(Achievement).all()}
        new_achievements_count = 0
        updated_achievements_count = 0
        
        # Create or update achievements
        for ach_data in ACHIEVEMENTS:
            if ach_data["name"] in existing_achievements:
                # Achievement exists - update if needed (points, description, etc.)
                existing = existing_achievements[ach_data["name"]]
                updated = False
                
                if existing.points != ach_data["points"]:
                    existing.points = ach_data["points"]
                    updated = True
                if existing.description != ach_data["description"]:
                    existing.description = ach_data["description"]
                    updated = True
                if existing.tier != ach_data["tier"]:
                    existing.tier = ach_data["tier"]
                    updated = True
                if existing.target_value != ach_data["target_value"]:
                    existing.target_value = ach_data["target_value"]
                    updated = True
                if existing.metric != ach_data["metric"]:
                    existing.metric = ach_data["metric"]
                    updated = True
                
                if updated:
                    updated_achievements_count += 1
            else:
                # Create new achievement
                achievement = Achievement(
                    name=ach_data["name"],
                    description=ach_data["description"],
                    tier=ach_data["tier"],
                    metric=ach_data["metric"],
                    target_value=ach_data["target_value"],
                    points=ach_data["points"]
                )
                db.add(achievement)
                new_achievements_count += 1
        
        # Commit changes
        if new_achievements_count > 0 or updated_achievements_count > 0:
            db.commit()
            if new_achievements_count > 0:
                print(f"✅ Successfully seeded {new_achievements_count} new achievement(s)!")
            if updated_achievements_count > 0:
                print(f"✅ Updated {updated_achievements_count} existing achievement(s)!")
        else:
            print("ℹ️  All achievements already exist in database with correct values.")
        
        # Check existing players for achievements they may have already earned
        if check_existing_players:
            print("\n🔍 Checking existing players for achievements...")
            players = db.query(User).filter(User.role == "player").all()
            unlocked_count = 0
            for player in players:
                try:
                    if check_and_unlock_achievements(db, player.id):
                        unlocked_count += 1
                except Exception as e:
                    print(f"⚠️  Error checking achievements for user {player.id}: {e}")
                    continue
            
            if unlocked_count > 0:
                print(f"✅ Checked {len(players)} players. {unlocked_count} player(s) had new achievements unlocked.")
            else:
                print(f"ℹ️  Checked {len(players)} players. No new achievements unlocked.")
        
        return (new_achievements_count, updated_achievements_count)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding achievements: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    print("🌱 Starting achievement seeding...")
    print("=" * 60)
    seed_achievements(check_existing_players=True)
    print("=" * 60)
    print("✅ Achievement seeding completed!")
