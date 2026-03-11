from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AppUser(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mobile: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    device_sn: Mapped[str | None] = mapped_column(String(50), nullable=True)

