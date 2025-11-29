from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AchievementCreate(BaseModel):
    name: str
    description: str
    tier: str
    points: int
    target_value: int
    metric: Optional[str] = None  # Optional internal field for checker logic

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    tier: str
    points: int
    target_value: int
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
