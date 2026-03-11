from __future__ import annotations

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserAudioPlayback(Base):
    __tablename__ = "user_audio_playback"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), index=True, nullable=False)
    audio_id: Mapped[int] = mapped_column(ForeignKey("audio_resource.id"), index=True, nullable=False)
    listened_at: Mapped[object] = mapped_column(DateTime, nullable=False)
    listened_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    device_sn: Mapped[str | None] = mapped_column(String(50), nullable=True)

