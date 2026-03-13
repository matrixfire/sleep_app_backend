from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AppUserCreate(BaseModel):
    mobile: str | None = None
    wechat_openid: str | None = None
    nickname: str | None = None
    device_sn: str | None = None
    device_mac: str | None = None


class AppUserOut(BaseModel):
    id: int
    mobile: str | None = None
    wechat_openid: str | None = None
    nickname: str
    register_time: datetime
    device_sn: str | None = None
    device_mac: str | None = None

    class Config:
        from_attributes = True

