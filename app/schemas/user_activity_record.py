from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


# status: 0 = in progress, 1 = completed, 2 = terminated early
class ActivityStartIn(BaseModel):
    activity_type: str  # sleep, nap, focus, breathe


class ActivityEndIn(BaseModel):
    activity_type: str | None = None  # optional; can infer from in-progress record
    duration_min: int | None = None
    status: int = 1  # 1 completed, 2 terminated early


class UserActivityRecordOut(BaseModel):
    id: int
    user_id: int
    activity_type: str
    start_time: datetime
    end_time: datetime | None
    duration_min: int | None
    status: int

    class Config:
        from_attributes = True


class UserActivityListResponse(BaseModel):
    total: int
    items: list[UserActivityRecordOut]
