from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, HttpUrl


class AudioBase(BaseModel):
    title: str
    cover_url: Optional[HttpUrl] = None
    audio_url: HttpUrl


class AudioCreate(AudioBase):
    pass


class AudioUpdate(BaseModel):
    title: Optional[str] = None
    cover_url: Optional[HttpUrl] = None
    audio_url: Optional[HttpUrl] = None


class AudioOut(AudioBase):
    id: int

    class Config:
        from_attributes = True


class AudioListResponse(BaseModel):
    total: int
    items: list[AudioOut]

