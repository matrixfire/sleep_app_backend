from __future__ import annotations

from pydantic import BaseModel


class AppUserCreate(BaseModel):
    mobile: str | None = None
    nickname: str | None = None
    device_sn: str | None = None


class AppUserOut(BaseModel):
    id: int
    mobile: str | None = None
    nickname: str | None = None
    device_sn: str | None = None

    class Config:
        from_attributes = True

