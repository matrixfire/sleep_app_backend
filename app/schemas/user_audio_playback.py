from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserAudioPlaybackCreate(BaseModel):
    audio_id: int
    listened_at: datetime
    listened_seconds: int = 0
    device_sn: str | None = None


class UserAudioPlaybackOut(BaseModel):
    id: int
    user_id: int
    audio_id: int
    listened_at: datetime
    listened_seconds: int
    device_sn: str | None = None

    class Config:
        from_attributes = True


class UserAudioPlaybackListResponse(BaseModel):
    total: int
    items: list[UserAudioPlaybackOut]

