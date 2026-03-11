from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import UserSleepRecord


def create_sleep_record(db: Session, rec: UserSleepRecord) -> UserSleepRecord:
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def get_sleep_record(db: Session, record_id: int) -> Optional[UserSleepRecord]:
    return db.get(UserSleepRecord, record_id)


def list_sleep_records_for_user(db: Session, user_id: int, page: int, size: int) -> Tuple[int, list[UserSleepRecord]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    base = select(UserSleepRecord).where(UserSleepRecord.user_id == user_id)
    total = db.execute(select(func.count()).select_from(base.subquery())).scalar_one()
    stmt = (
        base.order_by(UserSleepRecord.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items

