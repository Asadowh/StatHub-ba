from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from models.trophy import Trophy
from models.stat import Stat
from datetime import datetime

def award_trophy_for_match(db: Session, match_id: int):
    """
    Award trophy to the best player of a match based on:
    1. Highest rating
    2. If tied: highest goals
    3. If still tied: highest assists
    4. If still tied: earliest created_at stat record
    
    This function will recalculate and update the trophy if one already exists.
    """
    # Get all stats for this match
    stats = db.query(Stat).filter(Stat.match_id == match_id).all()
    
    if not stats:
        # No stats yet, delete existing trophy if any
        existing_trophy = db.query(Trophy).filter(Trophy.match_id == match_id).first()
        if existing_trophy:
            db.delete(existing_trophy)
            db.commit()
        return None
    
    # Find the best player
    best_stat = None
    for stat in stats:
        if best_stat is None:
            best_stat = stat
            continue
        
        # Compare by rating (highest first)
        if stat.rating > best_stat.rating:
            best_stat = stat
        elif stat.rating == best_stat.rating:
            # Tiebreaker 1: Goals
            if stat.goals > best_stat.goals:
                best_stat = stat
            elif stat.goals == best_stat.goals:
                # Tiebreaker 2: Assists
                if stat.assists > best_stat.assists:
                    best_stat = stat
                elif stat.assists == best_stat.assists:
                    # Tiebreaker 3: Earliest created_at
                    if stat.created_at < best_stat.created_at:
                        best_stat = stat
    
    # Check if trophy already exists
    existing_trophy = db.query(Trophy).filter(Trophy.match_id == match_id).first()
    
    if existing_trophy:
        # Update existing trophy if the best player changed
        if existing_trophy.awarded_to != best_stat.player_id:
            existing_trophy.awarded_to = best_stat.player_id
            existing_trophy.date_awarded = datetime.utcnow()
            db.commit()
            db.refresh(existing_trophy)
        return existing_trophy
    else:
        # Create new trophy
        trophy = Trophy(
            match_id=match_id,
            awarded_to=best_stat.player_id,
            date_awarded=datetime.utcnow()
        )
        db.add(trophy)
        db.commit()
        db.refresh(trophy)
        return trophy


def get_user_trophy_count(db: Session, user_id: int) -> int:
    """Get total trophy count for a user"""
    return db.query(Trophy).filter(Trophy.awarded_to == user_id).count()


def get_user_trophies(db: Session, user_id: int):
    """Get all trophies for a user"""
    return db.query(Trophy).filter(Trophy.awarded_to == user_id).order_by(desc(Trophy.date_awarded)).all()


def award_trophy(db: Session, data):
    """Legacy function for manual trophy creation - kept for backward compatibility"""
    trophy = Trophy(
        match_id=data.get('match_id'),
        awarded_to=data.awarded_to
    )
    db.add(trophy)
    db.commit()
    db.refresh(trophy)
    return trophy
