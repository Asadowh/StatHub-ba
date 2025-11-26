from pydantic import BaseModel, validator
from datetime import datetime

DATE_FORMAT = "%m/%d/%Y %H:%M"

class MatchBase(BaseModel):
    home_team: str
    away_team: str
    location: str
    match_date: str  # user must send MM/DD/YYYY HH:MM
    score_home: int = 0
    score_away: int = 0

    @validator("match_date")
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("match_date must be in format MM/DD/YYYY HH:MM")
        return value


class MatchCreate(MatchBase):
    pass


class MatchResponse(MatchBase):
    id: int
    created_by: int

    @validator("match_date", pre=True)
    def format_output_date(cls, value):
        if isinstance(value, datetime):
            return value.strftime(DATE_FORMAT)
        return value

    class Config:
        orm_mode = True