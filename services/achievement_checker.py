from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from models.achievement import Achievement, PlayerAchievement
from models.stat import Stat
from services.xp_service import update_user_xp_and_level


def check_and_unlock_achievements(db: Session, user_id: int, current_stat_id: int = None):
    """
    Check all achievements for a user based on their current stats and unlock them if conditions are met.
    This should be called after stats are created or updated.
    
    Args:
        db: Database session
        user_id: User ID to check achievements for
        current_stat_id: Optional stat ID that was just created/updated (for checking match-specific achievements)
    """
    # Get user's aggregated stats
    stats_query = (
        db.query(
            func.sum(Stat.goals).label("total_goals"),
            func.sum(Stat.assists).label("total_assists"),
            func.avg(Stat.rating).label("avg_rating"),
            func.count(Stat.id).label("matches_played"),
            func.max(Stat.goals).label("max_goals_in_match")
        )
        .filter(Stat.player_id == user_id)
        .first()
    )
    
    total_goals = stats_query.total_goals or 0
    total_assists = stats_query.total_assists or 0
    matches_played = stats_query.matches_played or 0
    max_goals_in_match = stats_query.max_goals_in_match or 0
    
    # Get goals in current match if stat_id is provided
    current_match_goals = 0
    if current_stat_id:
        current_stat = db.query(Stat).filter(Stat.id == current_stat_id).first()
        if current_stat:
            current_match_goals = current_stat.goals or 0
    
    # Get average rating across last 5 matches
    recent_matches = (
        db.query(Stat.rating)
        .filter(Stat.player_id == user_id)
        .order_by(Stat.created_at.desc())
        .limit(5)
        .all()
    )
    
    avg_rating_last_5 = 0.0
    if len(recent_matches) > 0:
        # Calculate average rating of available matches (even if < 5)
        avg_rating_last_5 = sum(r.rating for r in recent_matches) / len(recent_matches)
    
    # Get all achievements
    all_achievements = db.query(Achievement).all()
    
    if not all_achievements:
        print(f"No achievements found in database. Please seed achievements first.")
        return False
    
    achievement_unlocked = False
    
    for achievement in all_achievements:
        # Get or create player achievement record
        player_achievement = (
            db.query(PlayerAchievement)
            .filter(
                PlayerAchievement.user_id == user_id,
                PlayerAchievement.achievement_id == achievement.id
            )
            .first()
        )
        
        if not player_achievement:
            player_achievement = PlayerAchievement(
                user_id=user_id,
                achievement_id=achievement.id,
                current_value=0,
                unlocked=False
            )
            db.add(player_achievement)
        
        # Skip if already unlocked
        if player_achievement.unlocked:
            continue
        
        # Check achievement conditions based on metric (not name) - this allows custom achievements
        should_unlock = False
        current_value = 0
        target_value = achievement.target_value
        
        # Track achievements by metric instead of name - this supports custom achievements
        if achievement.metric == "matches":
            current_value = matches_played
            should_unlock = matches_played >= target_value
        
        elif achievement.metric == "assists":
            current_value = total_assists
            should_unlock = total_assists >= target_value
        
        elif achievement.metric == "goals":
            current_value = total_goals
            should_unlock = total_goals >= target_value
        
        elif achievement.metric == "goals_per_match":
            # Check if player scored target_value+ goals in any single match
            # Use current match goals if available, otherwise use max from all matches
            if current_stat_id and current_match_goals >= target_value:
                current_value = current_match_goals
                should_unlock = True
            else:
                current_value = max_goals_in_match
                should_unlock = max_goals_in_match >= target_value
        
        elif achievement.metric == "rating":
            # For rating-based achievements, check average rating
            # Note: target_value is Integer in DB. For 7.5 rating, you can store as 75 (divide by 10) or 7/8
            # We'll handle both: if target_value > 10, assume it's stored as integer*10 (e.g., 75 for 7.5)
            # Otherwise, compare directly
            if target_value > 10:
                # Stored as integer*10 (e.g., 75 for 7.5)
                target_rating = target_value / 10.0
            else:
                # Stored as integer (e.g., 7 for 7.0, 8 for 8.0)
                target_rating = float(target_value)
            
            # Special handling for "Elite Performer" which requires 5+ matches
            if achievement.name == "Elite Performer":
                # Elite Performer: requires 5+ matches AND rating >= target
                if len(recent_matches) >= 5:
                    # Store rating as integer*10 (e.g., 75 for 7.5) to match target_value format
                    current_value = int(round(avg_rating_last_5 * 10))
                else:
                    current_value = 0
                # Only unlock if user has 5+ matches AND average meets target
                should_unlock = len(recent_matches) >= 5 and avg_rating_last_5 >= target_rating
            else:
                # Generic rating achievement: check average rating across all matches
                if len(recent_matches) > 0:
                    # Store rating as integer*10 (e.g., 75 for 7.5) to match target_value format
                    current_value = int(round(avg_rating_last_5 * 10))
                    should_unlock = avg_rating_last_5 >= target_rating
                else:
                    current_value = 0
                    should_unlock = False
        
        else:
            # Unknown metric - log a warning but don't skip (might be a future metric)
            print(f"Warning: Unknown achievement metric '{achievement.metric}' for achievement '{achievement.name}' - cannot track progress")
            # Set current_value to 0 but don't unlock
            current_value = 0
            should_unlock = False
        
        # Update current value
        player_achievement.current_value = current_value
        
        # Unlock if condition is met
        if should_unlock and not player_achievement.unlocked:
            player_achievement.unlocked = True
            player_achievement.unlocked_at = datetime.now(timezone.utc)
            achievement_unlocked = True
            print(f"✅ Achievement unlocked: {achievement.name} for user {user_id}")
    
    # Commit all changes at once
    db.commit()
    
    # Update user XP and level if an achievement was unlocked
    if achievement_unlocked:
        update_user_xp_and_level(db, user_id)
    
    return achievement_unlocked

