from sqlalchemy.orm import Session
from models.stat import Stat
from models.match import Match
from models.user import User

def create_stat(db: Session, data):
    stat = Stat(
        match_id=data.match_id,
        player_id=data.player_id,
        team=data.team,  # "home" or "away"
        goals=data.goals,
        assists=data.assists,
        rating=data.rating
    )
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


def get_stats_for_match(db: Session, match_id: int):
    return db.query(Stat).filter(Stat.match_id == match_id).all()


def get_user_recent_performances(db: Session, user_id: int, limit: int = 3):
    """Get user's recent match performances with match details"""
    stats = (
        db.query(Stat)
        .filter(Stat.player_id == user_id)
        .join(Match, Stat.match_id == Match.id)
        .order_by(Match.match_date.desc())
        .limit(limit)
        .all()
    )
    
    results = []
    for stat in stats:
        match = stat.match
        # Determine if player won, lost, or drew
        if match.winner_team == "draw":
            player_result = "D"
        elif stat.team == match.winner_team:
            player_result = "W"
        elif match.winner_team is None:
            player_result = "D"  # No winner set yet
        else:
            player_result = "L"
        
        results.append({
            "id": stat.id,
            "match_id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date.strftime("%b %d"),
            "rating": stat.rating,
            "goals": stat.goals,
            "assists": stat.assists,
            "player_team": stat.team,
            "player_result": player_result
        })
    
    return results


def get_match_players_detailed(db: Session, match_id: int):
    """Get all players in a match with their details, sorted by jersey number"""
    stats = db.query(Stat).filter(Stat.match_id == match_id).all()
    
    home_players = []
    away_players = []
    
    for stat in stats:
        player = db.query(User).filter(User.id == stat.player_id).first()
        if not player:
            continue
            
        player_data = {
            "id": player.id,
            "username": player.username,
            "full_name": player.full_name,
            "photo_url": player.photo_url,
            "jersey_number": player.jersey_number or 99,  # Default to 99 if no jersey
            "favorite_position": player.favorite_position,
            "nationality": player.nationality,
            "goals": stat.goals,
            "assists": stat.assists,
            "rating": stat.rating,
        }
        
        if stat.team == "home":
            home_players.append(player_data)
        else:
            away_players.append(player_data)
    
    # Sort by jersey number
    home_players.sort(key=lambda x: x["jersey_number"])
    away_players.sort(key=lambda x: x["jersey_number"])
    
    return {
        "home_players": home_players,
        "away_players": away_players
    }
