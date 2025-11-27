from pydantic import BaseModel
from datetime import datetime

class AchievementCreate(BaseModel):
    name: str
    description: str
    tier: str
    metric: str
    target_value: int
    points: int = 0

class AchievementResponse(AchievementCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PlayerAchievementResponse(BaseModel):
    id: int
    user_id: int
    achievement_id: int
    current_value: int
    unlocked: bool
    unlocked_at: datetime | None

    class Config:
        from_attributes = True
