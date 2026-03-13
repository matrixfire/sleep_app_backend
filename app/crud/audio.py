from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AudioResource


def get_audio(db: Session, audio_id: int) -> Optional[AudioResource]:
    stmt = select(AudioResource).where(AudioResource.id == audio_id)
    return db.execute(stmt).scalar_one_or_none()


def list_audios(
    db: Session,
    page: int,
    size: int,
    category: Optional[str] = None,
    scene_tags: Optional[str] = None,
) -> Tuple[int, list[AudioResource]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    base = select(AudioResource)
    count_base = select(func.count()).select_from(AudioResource)
    if category:
        base = base.where(AudioResource.category == category)
        count_base = count_base.where(AudioResource.category == category)
    if scene_tags:
        tags = [t.strip() for t in scene_tags.split(",") if t.strip()]
        for tag in tags:
            base = base.where(AudioResource.scene_tags.contains(tag))
            count_base = count_base.where(AudioResource.scene_tags.contains(tag))
    total = db.execute(count_base).scalar_one()
    stmt = (
        base.order_by(AudioResource.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items


def create_audio(db: Session, audio: AudioResource) -> AudioResource:
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio


def update_audio(db: Session, db_obj: AudioResource) -> AudioResource:
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_audio(db: Session, db_obj: AudioResource) -> None:
    db.delete(db_obj)
    db.commit()

