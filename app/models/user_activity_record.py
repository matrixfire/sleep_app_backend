from __future__ import annotations

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


# Status: 0 = in progress, 1 = completed normally, 2 = terminated early
class UserActivityRecord(Base):
    __tablename__ = "user_activity_record"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), index=True, nullable=False)
    activity_type: Mapped[str] = mapped_column(String(20), index=True, nullable=False)  # sleep, nap, focus, breathe
    start_time: Mapped[object] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[object | None] = mapped_column(DateTime, nullable=True)
    duration_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0, 1, 2
