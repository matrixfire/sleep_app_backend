from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, HttpUrl


# Category: sleep, meditation, sound. Scene tags: nap, focus, breathe (comma-sep).
class AudioBase(BaseModel):
    title: str
    category: Optional[str] = "sound"  # sleep | meditation | sound (optional for legacy rows)
    scene_tags: Optional[str] = None
    cover_url: Optional[HttpUrl] = None
    audio_url: HttpUrl
    duration: Optional[int] = None  # seconds


class AudioCreate(AudioBase):
    pass


class AudioUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    scene_tags: Optional[str] = None
    cover_url: Optional[HttpUrl] = None
    audio_url: Optional[HttpUrl] = None
    duration: Optional[int] = None


class AudioOut(AudioBase):
    id: int

    class Config:
        from_attributes = True


class AudioListResponse(BaseModel):
    total: int
    items: list[AudioOut]

