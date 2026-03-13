from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud
from app.core.deps import get_current_user
from app.schemas import UserWithPerms
from app.services.stats_admin import StatsAdminService
from db.session import get_db

router = APIRouter(prefix="/admin/stats", tags=["admin-stats"])


def get_stats_service(
    db: Session = Depends(get_db),
    current_user: UserWithPerms = Depends(get_current_user),
) -> StatsAdminService:
    return StatsAdminService(db=db, current_user=current_user)


@router.get("/users/total")
def get_users_total(
    svc: StatsAdminService = Depends(get_stats_service),
) -> dict:
    """Total registered app users. Requires content:manage (or rbac:manage)."""
    return svc.users_total()


@router.get("/activities/summary")
def get_activities_summary(
    svc: StatsAdminService = Depends(get_stats_service),
) -> dict:
    """Activity usages today by category. Requires content:manage (or rbac:manage)."""
    return svc.activities_summary()
