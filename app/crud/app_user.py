from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AppUser


def create_app_user(db: Session, user: AppUser) -> AppUser:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_app_user(db: Session, user_id: int) -> Optional[AppUser]:
    return db.get(AppUser, user_id)


def list_app_users(db: Session, page: int, size: int) -> Tuple[int, list[AppUser]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    total = db.execute(select(func.count()).select_from(AppUser)).scalar_one()
    stmt = (
        select(AppUser)
        .order_by(AppUser.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items

