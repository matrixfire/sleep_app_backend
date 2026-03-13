from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.schemas import DailyQuoteCreate, DailyQuoteListResponse, DailyQuoteOut, DailyQuoteUpdate, UserWithPerms
from app.services.daily_quote_admin import DailyQuoteAdminService
from db.session import get_db

router = APIRouter(prefix="/admin/daily-quotes", tags=["admin-daily-quotes"])


def get_daily_quote_admin_service(
    db: Session = Depends(get_db),
    current_user: UserWithPerms = Depends(get_current_user),
) -> DailyQuoteAdminService:
    return DailyQuoteAdminService(db=db, current_user=current_user)


@router.get("", response_model=DailyQuoteListResponse)
def list_daily_quotes(
    page: int = 1,
    size: int = 20,
    svc: DailyQuoteAdminService = Depends(get_daily_quote_admin_service),
) -> DailyQuoteListResponse:
    return svc.list_quotes(page=page, size=size)


@router.post("", response_model=DailyQuoteOut, status_code=status.HTTP_201_CREATED)
def create_daily_quote(
    data: DailyQuoteCreate,
    svc: DailyQuoteAdminService = Depends(get_daily_quote_admin_service),
) -> DailyQuoteOut:
    return svc.create_quote(data)


@router.put("/{quote_id}", response_model=DailyQuoteOut)
def update_daily_quote(
    quote_id: int,
    data: DailyQuoteUpdate,
    svc: DailyQuoteAdminService = Depends(get_daily_quote_admin_service),
) -> DailyQuoteOut:
    return svc.update_quote(quote_id=quote_id, data=data)


@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_quote(
    quote_id: int,
    svc: DailyQuoteAdminService = Depends(get_daily_quote_admin_service),
) -> Response:
    svc.delete_quote(quote_id=quote_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
