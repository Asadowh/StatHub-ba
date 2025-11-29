from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models.achievement import Achievement, PlayerAchievement
from services.xp_service import update_user_xp_and_level

def create_achievement(db: Session, data):
    ach = Achievement(
        name=data.name,
        description=data.description,
        tier=data.tier,
        metric=data.metric,
        target_value=data.target_value,
        points=data.points,
    )
    db.add(ach)
    db.commit()
    db.refresh(ach)
    return ach


def update_player_achievement(db: Session, user_id: int, metric: str, increment: int):
    # Find achievement requiring this metric
    achievements = db.query(Achievement).filter(Achievement.metric == metric).all()
    achievement_unlocked = False

    for ach in achievements:
        record = (
            db.query(PlayerAchievement)
            .filter(
                PlayerAchievement.user_id == user_id,
                PlayerAchievement.achievement_id == ach.id,
            )
            .first()
        )

        if not record:
            record = PlayerAchievement(
                user_id=user_id,
                achievement_id=ach.id,
                current_value=0,
                unlocked=False
            )
            db.add(record)

        # Update progress
        record.current_value += increment

        # Unlock if reached target
        if not record.unlocked and record.current_value >= ach.target_value:
            record.unlocked = True
            record.unlocked_at = datetime.now(timezone.utc)
            achievement_unlocked = True

        db.commit()
    
    # Update user XP and level if an achievement was unlocked
    if achievement_unlocked:
        update_user_xp_and_level(db, user_id)
