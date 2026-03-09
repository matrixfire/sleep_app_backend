from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AudioResource(Base):
    __tablename__ = "audio_resource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    cover_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    audio_url: Mapped[str] = mapped_column(String(255), nullable=False)

