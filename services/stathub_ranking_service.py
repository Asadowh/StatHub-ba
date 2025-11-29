from sqlalchemy.orm import Session
from sqlalchemy import func
from models.user import User
from models.stat import Stat


def get_stathub_ranking(db: Session, sort_by: str = "rating", limit: int = 50):
    """
    Get StatHub ranking leaderboard sorted by different metrics.
    sort_by options: "rating", "goals", "assists", "combined"
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

    # Join with users
    results = (
        db.query(
            User.id,
            User.username,
            User.full_name,
            User.photo_url,
            User.nationality,
            User.favorite_position,
            func.coalesce(stats_subquery.c.total_goals, 0).label("total_goals"),
            func.coalesce(stats_subquery.c.total_assists, 0).label("total_assists"),
            func.coalesce(stats_subquery.c.avg_rating, 0).label("avg_rating"),
            func.coalesce(stats_subquery.c.matches_played, 0).label("matches_played"),
        )
        .outerjoin(stats_subquery, User.id == stats_subquery.c.player_id)
        .filter(User.role == "player")  # Exclude admin
        .all()
    )

    # Build leaderboard
    leaderboard = []
    for r in results:
        combined = (r.total_goals or 0) + (r.total_assists or 0)
        
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
            "combined": combined,
        })

    # Sort by the selected metric
    if sort_by == "rating":
        leaderboard.sort(key=lambda x: x["avg_rating"], reverse=True)
    elif sort_by == "goals":
        leaderboard.sort(key=lambda x: x["total_goals"], reverse=True)
    elif sort_by == "assists":
        leaderboard.sort(key=lambda x: x["total_assists"], reverse=True)
    elif sort_by == "combined":
        leaderboard.sort(key=lambda x: x["combined"], reverse=True)
    else:
        leaderboard.sort(key=lambda x: x["avg_rating"], reverse=True)

    # Add rank
    for i, player in enumerate(leaderboard[:limit], 1):
        player["rank"] = i

    return leaderboard[:limit]

