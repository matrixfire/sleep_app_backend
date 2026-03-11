from __future__ import annotations

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserSleepRecord(Base):
    __tablename__ = "user_sleep_record"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), index=True, nullable=False)
    device_sn: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    start_time: Mapped[object] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[object] = mapped_column(DateTime, nullable=False)
    raw_data_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    analysis_result: Mapped[str | None] = mapped_column(Text, nullable=True)

