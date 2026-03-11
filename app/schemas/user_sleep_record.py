from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UserSleepRecordCreate(BaseModel):
    device_sn: str
    start_time: datetime
    end_time: datetime
    raw_data_url: HttpUrl
    analysis_result: str | None = None


class UserSleepRecordOut(BaseModel):
    id: int
    user_id: int
    device_sn: str
    start_time: datetime
    end_time: datetime
    raw_data_url: HttpUrl
    analysis_result: str | None = None

    class Config:
        from_attributes = True


class UserSleepRecordListResponse(BaseModel):
    total: int
    items: list[UserSleepRecordOut]

