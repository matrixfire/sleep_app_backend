from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AppUser(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # Phone (kept as mobile for backward compatibility; design "phone")
    mobile: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
    wechat_openid: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    register_time: Mapped[object] = mapped_column(DateTime, nullable=False, default=_utcnow)
    device_sn: Mapped[str | None] = mapped_column(String(50), nullable=True)
    device_mac: Mapped[str | None] = mapped_column(String(50), nullable=True)

