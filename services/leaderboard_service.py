from sqlalchemy.orm import Session
from sqlalchemy import func
from models.user import User
from models.stat import Stat
from models.trophy import Trophy
from models.achievement import PlayerAchievement
from services.xp_service import update_user_xp_and_level


def get_leaderboard(db: Session, limit: int = 50):
    """
    Get StatHub ranking leaderboard ranked by XP (from achievements).
    XP is calculated from unlocked achievements.
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

    # Join with users - now using XP and level from User model
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
            func.coalesce(stats_subquery.c.total_goals, 0).label("total_goals"),
            func.coalesce(stats_subquery.c.total_assists, 0).label("total_assists"),
            func.coalesce(stats_subquery.c.avg_rating, 0).label("avg_rating"),
            func.coalesce(stats_subquery.c.matches_played, 0).label("matches_played"),
            func.coalesce(trophy_subquery.c.trophy_count, 0).label("trophy_count"),
        )
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .outerjoin(trophy_subquery, User.id == trophy_subquery.c.awarded_to)
        .filter(User.role == "player")  # Exclude admin
        .all()
    )

    # Build leaderboard with XP
    leaderboard = []
    for r in results:
        # Ensure XP is up to date
        update_user_xp_and_level(db, r.id)
        db.refresh(r)
        
        leaderboard.append({
            "user_id": r.id,
            "username": r.username,
            "full_name": r.full_name,
            "photo_url": r.photo_url,
            "nationality": r.nationality,
            "position": r.favorite_position,
            "total_goals": r.total_goals or 0,
            "total_assists": r.total_assists or 0,
            "avg_rating": round(r.avg_rating or 0, 1),
            "matches_played": r.matches_played or 0,
            "trophy_count": r.trophy_count or 0,
            "xp": r.xp or 0,
            "level": r.level or 1,
            "points": r.xp or 0,  # Keep "points" for backward compatibility
        })

    # Sort by XP descending and add rank
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    for i, player in enumerate(leaderboard[:limit], 1):
        player["rank"] = i

    return leaderboard[:limit]


def get_achievements_leaderboard(db: Session, limit: int = 50):
    """
    Get achievements leaderboard ranked by number of unlocked achievements.
    Excludes admin users.
    """
    # Get achievement counts for each user
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
        .outerjoin(achievement_subquery, User.id == achievement_subquery.c.user_id)
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .filter(User.role == "player")  # Exclude admin
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
    leaderboard.sort(key=lambda x: (x["achievement_count"], x["xp"]), reverse=True)
    for i, player in enumerate(leaderboard[:limit], 1):
        player["rank"] = i

    return leaderboard[:limit]


def get_trophies_leaderboard(db: Session, limit: int = 50):
    """
    Get trophies leaderboard ranked by number of trophies.
    Excludes admin users.
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
        .outerjoin(trophy_subquery, User.id == trophy_subquery.c.awarded_to)
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .filter(User.role == "player")  # Exclude admin
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
            "trophy_count": r.trophy_count or 0,
            "total_goals": r.total_goals or 0,
            "total_assists": r.total_assists or 0,
            "avg_rating": round(r.avg_rating or 0, 1),
            "matches_played": r.matches_played or 0,
            "xp": r.xp or 0,
            "level": r.level or 1,
        })

    # Sort by trophy count descending, then by XP as tiebreaker
    leaderboard.sort(key=lambda x: (x["trophy_count"], x["xp"]), reverse=True)
    for i, player in enumerate(leaderboard[:limit], 1):
        player["rank"] = i

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
