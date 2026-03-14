from __future__ import annotations

from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.core.deps import get_app_auth_service, get_current_app_user
from app.services import AppAuthService
from app.crud.user_activity_record import (
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_TERMINATED,
)
from app.models import UserActivityRecord
from app.schemas import (
    ActivityEndIn,
    ActivityStartIn,
    AppLoginRequest,
    AppUserOut,
    AudioListResponse,
    AudioOut,
    DailyQuoteOut,
    Token,
    UserActivityListResponse,
    UserActivityRecordOut,
)
from db.session import get_db

router = APIRouter(prefix="/app", tags=["app"])


# ---- Auth ----
@router.post("/auth/login", response_model=Token)
def app_login(
    data: AppLoginRequest,
    svc: AppAuthService = Depends(get_app_auth_service),
) -> Token:
    """App user login by phone or wechat_openid. Returns JWT with user_type=app."""
    token = svc.login(phone=data.phone, wechat_openid=data.wechat_openid)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide phone or wechat_openid",
        )
    return token


@router.get("/auth/me", response_model=AppUserOut)
def app_me(
    current_user: AppUserOut = Depends(get_current_app_user),
) -> AppUserOut:
    """Get current app user info."""
    return current_user


# ---- Home ----
@router.get("/home/daily-quote", response_model=DailyQuoteOut)
def get_daily_quote(
    db: Session = Depends(get_db),
) -> DailyQuoteOut:
    """Get the daily quote card for today (no auth required for public card)."""
    today = date.today()
    quote = crud.get_daily_quote_by_date(db, today)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quote for today",
        )
    return DailyQuoteOut.model_validate(quote)


# ---- Content (audios) ----
@router.get("/audios", response_model=AudioListResponse)
def list_app_audios(
    page: int = 1,
    size: int = 20,
    category: str | None = None,
    scene_tags: str | None = None,
    db: Session = Depends(get_db),
    current_user: AppUserOut = Depends(get_current_app_user),
) -> AudioListResponse:
    """List audios with optional category and scene_tags filters."""
    total, items = crud.list_audios(
        db, page=page, size=size, category=category, scene_tags=scene_tags
    )
    return AudioListResponse(
        total=total,
        items=[AudioOut.model_validate(obj) for obj in items],
    )


# ---- Activities ----
@router.post("/activities/start", response_model=UserActivityRecordOut)
def start_activity(
    data: ActivityStartIn,
    db: Session = Depends(get_db),
    current_user: AppUserOut = Depends(get_current_app_user),
) -> UserActivityRecordOut:
    """Start an activity (sleep, nap, focus, breathe); creates record with status in progress."""
    if data.activity_type not in ("sleep", "nap", "focus", "breathe"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="activity_type must be one of: sleep, nap, focus, breathe",
        )
    record = UserActivityRecord(
        user_id=current_user.id,
        activity_type=data.activity_type,
        start_time=datetime.now(timezone.utc),
        status=STATUS_IN_PROGRESS,
    )
    record = crud.create_activity_record(db, record)
    return UserActivityRecordOut.model_validate(record)


@router.post("/activities/end", response_model=UserActivityRecordOut)
def end_activity(
    data: ActivityEndIn,
    db: Session = Depends(get_db),
    current_user: AppUserOut = Depends(get_current_app_user),
) -> UserActivityRecordOut:
    """End the current in-progress activity; optionally specify which type or duration/status."""
    record = crud.get_in_progress_activity(
        db, user_id=current_user.id, activity_type=data.activity_type
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activity in progress",
        )
    record.end_time = datetime.now(timezone.utc)
    if data.duration_min is not None:
        record.duration_min = data.duration_min
    elif record.start_time:
        delta = record.end_time - record.start_time
        record.duration_min = int(delta.total_seconds() / 60)
    record.status = data.status if data.status in (STATUS_COMPLETED, STATUS_TERMINATED) else STATUS_COMPLETED
    record = crud.update_activity_record(db, record)
    return UserActivityRecordOut.model_validate(record)


@router.get("/activities/history", response_model=UserActivityListResponse)
def activity_history(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: AppUserOut = Depends(get_current_app_user),
) -> UserActivityListResponse:
    """Get current user's activity history (paginated)."""
    total, items = crud.list_activity_records(db, user_id=current_user.id, page=page, size=size)
    return UserActivityListResponse(
        total=total,
        items=[UserActivityRecordOut.model_validate(x) for x in items],
    )
