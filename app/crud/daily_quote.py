from __future__ import annotations

from datetime import date
from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import DailyQuote


def get_daily_quote_by_date(db: Session, show_date: date) -> Optional[DailyQuote]:
    stmt = select(DailyQuote).where(DailyQuote.show_date == show_date)
    return db.execute(stmt).scalar_one_or_none()


def get_daily_quote(db: Session, quote_id: int) -> Optional[DailyQuote]:
    return db.get(DailyQuote, quote_id)


def list_daily_quotes(
    db: Session, page: int, size: int
) -> Tuple[int, list[DailyQuote]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    total = db.execute(select(func.count()).select_from(DailyQuote)).scalar_one()
    stmt = (
        select(DailyQuote)
        .order_by(DailyQuote.show_date.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items


def create_daily_quote(db: Session, quote: DailyQuote) -> DailyQuote:
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def update_daily_quote(db: Session, db_obj: DailyQuote) -> DailyQuote:
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_daily_quote(db: Session, db_obj: DailyQuote) -> None:
    db.delete(db_obj)
    db.commit()
