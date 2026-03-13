from __future__ import annotations

from datetime import date

from pydantic import BaseModel, HttpUrl


class DailyQuoteBase(BaseModel):
    show_date: date
    content: str
    author: str | None = None
    bg_image_url: str  # OSS link


class DailyQuoteCreate(DailyQuoteBase):
    pass


class DailyQuoteUpdate(BaseModel):
    show_date: date | None = None
    content: str | None = None
    author: str | None = None
    bg_image_url: str | None = None


class DailyQuoteOut(DailyQuoteBase):
    id: int

    class Config:
        from_attributes = True


class DailyQuoteListResponse(BaseModel):
    total: int
    items: list[DailyQuoteOut]
