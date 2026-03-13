from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import crud
from app.models import AppUser
from app.schemas import UserWithPerms

PERM_CONTENT_MANAGE = "content:manage"
PERM_RBAC_MANAGE = "rbac:manage"


def _ensure_permission(user: UserWithPerms, perm_code: str) -> None:
    from fastapi import HTTPException, status
    if perm_code not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {perm_code}",
        )


class StatsAdminService:
    def __init__(self, db: Session, current_user: UserWithPerms):
        self.db = db
        self.current_user = current_user

    def users_total(self) -> dict:
        """Total registered app users."""
        _ensure_permission(self.current_user, PERM_CONTENT_MANAGE)
        total = self.db.execute(select(func.count()).select_from(AppUser)).scalar_one()
        return {"total": total}

    def activities_summary(self) -> dict:
        """Activity usages today by activity_type."""
        _ensure_permission(self.current_user, PERM_CONTENT_MANAGE)
        by_type = crud.count_activities_today_by_type(self.db)
        return {"by_type": by_type, "today_usage": sum(by_type.values())}
