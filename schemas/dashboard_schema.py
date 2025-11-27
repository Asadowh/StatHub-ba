from pydantic import BaseModel
from typing import List, Optional

class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    value: float

class AchievementSummary(BaseModel):
    total_points: int
    level: int
    unlocked_count: int

class DashboardResponse(BaseModel):
    top_players: List[LeaderboardEntry]
    trophies: int
    achievements: AchievementSummary
    rating_trend: List[float]
    next_match: Optional[dict]
    recent_performance: List[float]

    class Config:
        from_attributes = True
