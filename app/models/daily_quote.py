from __future__ import annotations

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DailyQuote(Base):
    __tablename__ = "daily_quote"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    show_date: Mapped[object] = mapped_column(Date, unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bg_image_url: Mapped[str] = mapped_column(String(255), nullable=False)
