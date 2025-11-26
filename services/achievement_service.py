from sqlalchemy.orm import Session
from models.achievement import Achievement, PlayerAchievement

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

        db.commit()
