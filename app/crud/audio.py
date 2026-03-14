from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy import func, select  # Import functions for building SQL queries and aggregation
from sqlalchemy.orm import Session    # Import Session for database interaction

from app.models import AudioResource  # Import our AudioResource SQLAlchemy model


def get_audio(db: Session, audio_id: int) -> Optional[AudioResource]:
    # Build a query to select the audio item with the given ID
    stmt = select(AudioResource).where(AudioResource.id == audio_id)
    # Execute the query, and return the first matching AudioResource or None if not found
    return db.execute(stmt).scalar_one_or_none()


def list_audios(
    db: Session,
    page: int,
    size: int,
    category: Optional[str] = None,
    scene_tags: Optional[str] = None,
) -> Tuple[int, list[AudioResource]]:
    # Validation to ensure page is at least 1
    if page < 1:
        page = 1
    # Validation to ensure size is at least 1
    if size < 1:
        size = 10
    # Start building the base query for selecting audios
    base = select(AudioResource)
    # Build a query for counting the total number of matching audios
    count_base = select(func.count()).select_from(AudioResource)
    # If a category is specified, filter both queries by category
    if category:
        base = base.where(AudioResource.category == category)
        count_base = count_base.where(AudioResource.category == category)
    # If scene_tags are specified, split tags and filter to require all provided tags
    if scene_tags:
        # Split scene_tags by comma and strip blanks
        tags = [t.strip() for t in scene_tags.split(",") if t.strip()]
        for tag in tags:
            # For each tag, require that the scene_tags column contains the tag (simple partial match)
            base = base.where(AudioResource.scene_tags.contains(tag))
            count_base = count_base.where(AudioResource.scene_tags.contains(tag))
    # Execute the count query to get the total number of matching audio records
    total = db.execute(count_base).scalar_one()
    # Add ordering (newest first), apply pagination with offset and limit
    stmt = (
        base.order_by(AudioResource.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    # Run the final query and collect all AudioResource objects into a list
    items = db.execute(stmt).scalars().all()
    # Return the total count and the list of audio resources
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

