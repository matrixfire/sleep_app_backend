from __future__ import annotations

from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import UserActivityRecord


STATUS_IN_PROGRESS = 0
STATUS_COMPLETED = 1
STATUS_TERMINATED = 2


def get_activity_record(db: Session, record_id: int) -> Optional[UserActivityRecord]:
    return db.get(UserActivityRecord, record_id)


def get_in_progress_activity(
    db: Session, user_id: int, activity_type: Optional[str] = None
) -> Optional[UserActivityRecord]:
    stmt = select(UserActivityRecord).where(
        UserActivityRecord.user_id == user_id,
        UserActivityRecord.status == STATUS_IN_PROGRESS,
    )
    if activity_type:
        stmt = stmt.where(UserActivityRecord.activity_type == activity_type)
    stmt = stmt.order_by(UserActivityRecord.start_time.desc()).limit(1)
    return db.execute(stmt).scalar_one_or_none()


def list_activity_records(
    db: Session, user_id: int, page: int, size: int
) -> Tuple[int, list[UserActivityRecord]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    total = (
        db.execute(
            select(func.count()).select_from(UserActivityRecord).where(
                UserActivityRecord.user_id == user_id
            )
        )
        .scalar_one()
    )
    stmt = (
        select(UserActivityRecord)
        .where(UserActivityRecord.user_id == user_id)
        .order_by(UserActivityRecord.start_time.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items


def create_activity_record(db: Session, record: UserActivityRecord) -> UserActivityRecord:
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_activity_record(db: Session, db_obj: UserActivityRecord) -> UserActivityRecord:
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def count_activities_today_by_type(db: Session) -> dict[str, int]:
    """Return counts of activity usages today by activity_type. Used for admin stats."""
    today = datetime.utcnow().date()
    stmt = (
        select(UserActivityRecord.activity_type, func.count(UserActivityRecord.id))
        .where(func.date(UserActivityRecord.start_time) == today)
        .group_by(UserActivityRecord.activity_type)
    )
    rows = db.execute(stmt).all()
    return {row[0]: row[1] for row in rows}
