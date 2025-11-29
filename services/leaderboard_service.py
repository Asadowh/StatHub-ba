from sqlalchemy.orm import Session
from sqlalchemy import func
from models.user import User
from models.stat import Stat
from models.trophy import Trophy
from models.achievement import PlayerAchievement
from services.xp_service import update_user_xp_and_level


def get_leaderboard(db: Session, limit: int = 50):
    """
    Get StatHub ranking leaderboard ranked by average StatHub rating.
    Includes ALL players, even those with 0 rating or no matches.
    Excludes admin users.
    """
    # Get aggregated stats for each user
    stats_subquery = (
        db.query(
            Stat.player_id,
            func.sum(Stat.goals).label("total_goals"),
            func.sum(Stat.assists).label("total_assists"),
            func.avg(Stat.rating).label("avg_rating"),
            func.count(Stat.id).label("matches_played")
        )
        .group_by(Stat.player_id)
        .subquery()
    )

    # Get trophy counts
    trophy_subquery = (
        db.query(
            Trophy.awarded_to,
            func.count(Trophy.id).label("trophy_count")
        )
        .group_by(Trophy.awarded_to)
        .subquery()
    )

    # Start from User table to ensure ALL players are included
    # Use func.coalesce to ensure XP and level default to 0 and 1 if None
    results = (
        db.query(
            User.id,
            User.username,
            User.full_name,
            User.photo_url,
            User.nationality,
            User.favorite_position,
            func.coalesce(User.xp, 0).label("xp"),
            func.coalesce(User.level, 1).label("level"),
            func.coalesce(stats_subquery.c.total_goals, 0).label("total_goals"),
            func.coalesce(stats_subquery.c.total_assists, 0).label("total_assists"),
            func.coalesce(stats_subquery.c.avg_rating, 0).label("avg_rating"),
            func.coalesce(stats_subquery.c.matches_played, 0).label("matches_played"),
            func.coalesce(trophy_subquery.c.trophy_count, 0).label("trophy_count"),
        )
        .filter(User.role == "player")  # Exclude admin - do this first
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .outerjoin(trophy_subquery, User.id == trophy_subquery.c.awarded_to)
        .all()
    )

    # Build leaderboard with average rating
    leaderboard = []
    for r in results:
        # Get XP and level for display purposes (but not for ranking)
        xp_info = update_user_xp_and_level(db, r.id)
        current_xp = xp_info["xp"] if xp_info else (r.xp if r.xp is not None else 0)
        current_level = xp_info["level"] if xp_info else (r.level if r.level is not None else 1)
        
        # Average rating is the primary ranking metric
        avg_rating_value = round(float(r.avg_rating) if r.avg_rating else 0, 1)
        
        leaderboard.append({
            "user_id": r.id,
            "username": r.username,
            "full_name": r.full_name,
            "photo_url": r.photo_url,
            "nationality": r.nationality,
            "position": r.favorite_position,
            "total_goals": int(r.total_goals) if r.total_goals else 0,
            "total_assists": int(r.total_assists) if r.total_assists else 0,
            "avg_rating": avg_rating_value,
            "matches_played": int(r.matches_played) if r.matches_played else 0,
            "trophy_count": int(r.trophy_count) if r.trophy_count else 0,
            "xp": int(current_xp),
            "level": int(current_level),
            "points": avg_rating_value,  # Use avg_rating as "points" for ranking display
        })

    # Sort by average rating descending and add rank to ALL players
    # This ensures players with 0 rating still appear at the bottom
    leaderboard.sort(key=lambda x: x["avg_rating"], reverse=True)
    
    # Rank ALL players first (not just the limited set)
    for i, player in enumerate(leaderboard, 1):
        player["rank"] = i

    # Return the limited set (but all players have been ranked)
    return leaderboard[:limit]


def get_achievements_leaderboard(db: Session, limit: int = 50):
    """
    Get achievements leaderboard ranked by number of unlocked achievements.
    Includes ALL players, even those with 0 achievements.
    Excludes admin users.
    """
    # Get achievement counts for each user (only unlocked ones)
    achievement_subquery = (
        db.query(
            PlayerAchievement.user_id,
            func.count(PlayerAchievement.id).label("achievement_count")
        )
        .filter(PlayerAchievement.unlocked == True)
        .group_by(PlayerAchievement.user_id)
        .subquery()
    )

    # Get aggregated stats
    stats_subquery = (
        db.query(
            Stat.player_id,
            func.sum(Stat.goals).label("total_goals"),
            func.sum(Stat.assists).label("total_assists"),
            func.avg(Stat.rating).label("avg_rating"),
            func.count(Stat.id).label("matches_played")
        )
        .group_by(Stat.player_id)
        .subquery()
    )

    # Start from User table to ensure ALL players are included
    results = (
        db.query(
            User.id,
            User.username,
            User.full_name,
            User.photo_url,
            User.nationality,
            User.favorite_position,
            User.xp,
            User.level,
            func.coalesce(achievement_subquery.c.achievement_count, 0).label("achievement_count"),
            func.coalesce(stats_subquery.c.total_goals, 0).label("total_goals"),
            func.coalesce(stats_subquery.c.total_assists, 0).label("total_assists"),
            func.coalesce(stats_subquery.c.avg_rating, 0).label("avg_rating"),
            func.coalesce(stats_subquery.c.matches_played, 0).label("matches_played"),
        )
        .filter(User.role == "player")  # Exclude admin - do this first
        .outerjoin(achievement_subquery, User.id == achievement_subquery.c.user_id)
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .all()
    )

    leaderboard = []
    for r in results:
        leaderboard.append({
            "user_id": r.id,
            "username": r.username,
            "full_name": r.full_name,
            "photo_url": r.photo_url,
            "nationality": r.nationality,
            "position": r.favorite_position,
            "achievement_count": r.achievement_count or 0,
            "total_goals": r.total_goals or 0,
            "total_assists": r.total_assists or 0,
            "avg_rating": round(r.avg_rating or 0, 1),
            "matches_played": r.matches_played or 0,
            "xp": r.xp or 0,
            "level": r.level or 1,
        })

    # Sort by achievement count descending, then by XP as tiebreaker
    # This ensures players with 0 achievements still appear
    leaderboard.sort(key=lambda x: (x["achievement_count"], x["xp"]), reverse=True)
    for i, player in enumerate(leaderboard[:limit], 1):
        player["rank"] = i

    return leaderboard[:limit]


def get_trophies_leaderboard(db: Session, limit: int = 1000):
    """
    Get trophies leaderboard ranked by number of trophies.
    Includes ALL players (non-admin), even those with 0 trophies.
    """
    # Get trophy counts
    trophy_subquery = (
        db.query(
            Trophy.awarded_to,
            func.count(Trophy.id).label("trophy_count")
        )
        .group_by(Trophy.awarded_to)
        .subquery()
    )

    # Get aggregated stats
    stats_subquery = (
        db.query(
            Stat.player_id,
            func.sum(Stat.goals).label("total_goals"),
            func.sum(Stat.assists).label("total_assists"),
            func.avg(Stat.rating).label("avg_rating"),
            func.count(Stat.id).label("matches_played")
        )
        .group_by(Stat.player_id)
        .subquery()
    )

    # Start from User table to ensure ALL players are included
    results = (
        db.query(
            User.id,
            User.username,
            User.full_name,
            User.photo_url,
            User.nationality,
            User.favorite_position,
            User.xp,
            User.level,
            func.coalesce(trophy_subquery.c.trophy_count, 0).label("trophy_count"),
            func.coalesce(stats_subquery.c.total_goals, 0).label("total_goals"),
            func.coalesce(stats_subquery.c.total_assists, 0).label("total_assists"),
            func.coalesce(stats_subquery.c.avg_rating, 0).label("avg_rating"),
            func.coalesce(stats_subquery.c.matches_played, 0).label("matches_played"),
        )
        .filter(User.role == "player")  # Exclude admin - do this first
        .outerjoin(trophy_subquery, User.id == trophy_subquery.c.awarded_to)
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .all()
    )

    leaderboard = []
    for r in results:
        leaderboard.append({
            "user_id": r.id,
            "username": r.username,
            "full_name": r.full_name,
            "photo_url": r.photo_url,
            "nationality": r.nationality,
            "position": r.favorite_position,
            "trophy_count": int(r.trophy_count) if r.trophy_count else 0,
            "total_goals": int(r.total_goals) if r.total_goals else 0,
            "total_assists": int(r.total_assists) if r.total_assists else 0,
            "avg_rating": round(float(r.avg_rating) if r.avg_rating else 0, 1),
            "matches_played": int(r.matches_played) if r.matches_played else 0,
            "xp": int(r.xp) if r.xp else 0,
            "level": int(r.level) if r.level else 1,
        })

    # Sort by trophy count descending, then by user_id for consistent ranking
    # This ensures players with 0 trophies still appear at the bottom
    leaderboard.sort(key=lambda x: (-x["trophy_count"], x["user_id"]))
    
    # Rank ALL players first (not just the limited set)
    for i, player in enumerate(leaderboard, 1):
        player["rank"] = i

    # Return the limited set (but all players have been ranked)
    return leaderboard[:limit]


def get_user_rank(db: Session, user_id: int):
    """Get a specific user's rank on the StatHub ranking leaderboard"""
    leaderboard = get_leaderboard(db, limit=1000)
    for player in leaderboard:
        if player["user_id"] == user_id:
            return player
    return None


def get_user_achievement_rank(db: Session, user_id: int):
    """Get a specific user's rank on the achievements leaderboard"""
    leaderboard = get_achievements_leaderboard(db, limit=1000)
    for player in leaderboard:
        if player["user_id"] == user_id:
            return player
    return None


def get_user_trophy_rank(db: Session, user_id: int):
    """Get a specific user's rank on the trophies leaderboard"""
    leaderboard = get_trophies_leaderboard(db, limit=1000)
    for player in leaderboard:
        if player["user_id"] == user_id:
            return player
    return None
