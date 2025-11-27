from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from models.user import User
from models.match import Match
from models.stat import Stat

def search_players(db: Session, query: str):
    """Search players by username, full_name, or nationality"""
    try:
        users = db.query(User).filter(
            or_(
                User.username.ilike(f"%{query}%"),
                User.full_name.ilike(f"%{query}%"),
                User.nationality.ilike(f"%{query}%")
            )
        ).limit(20).all()
        
        # Get stats for each user
        results = []
        for user in users:
            try:
                stats = db.query(
                    func.count(Stat.id).label("matches_played"),
                    func.coalesce(func.sum(Stat.goals), 0).label("total_goals"),
                    func.coalesce(func.sum(Stat.assists), 0).label("total_assists"),
                    func.coalesce(func.avg(Stat.rating), 0).label("avg_rating"),
                ).filter(Stat.player_id == user.id).first()
                
                player_stats = {
                    "matches": stats.matches_played or 0 if stats else 0,
                    "goals": int(stats.total_goals or 0) if stats else 0,
                    "assists": int(stats.total_assists or 0) if stats else 0,
                    "rating": round(float(stats.avg_rating or 0), 1) if stats else 0,
                }
            except Exception:
                player_stats = {"matches": 0, "goals": 0, "assists": 0, "rating": 0}
            
            results.append({
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "photo_url": user.photo_url,
                "nationality": user.nationality,
                "favorite_position": user.favorite_position,
                "jersey_number": user.jersey_number,
                "stats": player_stats
            })
        
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def search_matches(db: Session, team_query: str):
    return (
        db.query(Match)
        .filter(
            (Match.home_team.ilike(f"%{team_query}%")) |
            (Match.away_team.ilike(f"%{team_query}%"))
        )
        .all()
    )
