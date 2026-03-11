from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import UserAudioPlayback


def create_playback(db: Session, rec: UserAudioPlayback) -> UserAudioPlayback:
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def get_playback(db: Session, playback_id: int) -> Optional[UserAudioPlayback]:
    return db.get(UserAudioPlayback, playback_id)


def list_playbacks_for_user(
    db: Session, user_id: int, page: int, size: int
) -> Tuple[int, list[UserAudioPlayback]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    base = select(UserAudioPlayback).where(UserAudioPlayback.user_id == user_id)
    total = db.execute(select(func.count()).select_from(base.subquery())).scalar_one()
    stmt = (
        base.order_by(UserAudioPlayback.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items

