from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import DailyQuote
from app.schemas import DailyQuoteCreate, DailyQuoteListResponse, DailyQuoteOut, DailyQuoteUpdate, UserWithPerms

PERM_CONTENT_MANAGE = "content:manage"


def _ensure_permission(user: UserWithPerms, perm_code: str) -> None:
    if perm_code not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {perm_code}",
        )


class DailyQuoteAdminService:
    def __init__(self, db: Session, current_user: UserWithPerms):
        self.db = db
        self.current_user = current_user

    def list_quotes(self, page: int, size: int) -> DailyQuoteListResponse:
        _ensure_permission(self.current_user, PERM_CONTENT_MANAGE)
        total, items = crud.list_daily_quotes(self.db, page=page, size=size)
        return DailyQuoteListResponse(
            total=total,
            items=[DailyQuoteOut.model_validate(x) for x in items],
        )

    def create_quote(self, data: DailyQuoteCreate) -> DailyQuoteOut:
        _ensure_permission(self.current_user, PERM_CONTENT_MANAGE)
        obj = DailyQuote(
            show_date=data.show_date,
            content=data.content,
            author=data.author,
            bg_image_url=data.bg_image_url,
        )
        obj = crud.create_daily_quote(self.db, obj)
        return DailyQuoteOut.model_validate(obj)

    def update_quote(self, quote_id: int, data: DailyQuoteUpdate) -> DailyQuoteOut:
        _ensure_permission(self.current_user, PERM_CONTENT_MANAGE)
        obj = crud.get_daily_quote(self.db, quote_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily quote not found")
        if data.show_date is not None:
            obj.show_date = data.show_date
        if data.content is not None:
            obj.content = data.content
        if data.author is not None:
            obj.author = data.author
        if data.bg_image_url is not None:
            obj.bg_image_url = data.bg_image_url
        obj = crud.update_daily_quote(self.db, obj)
        return DailyQuoteOut.model_validate(obj)

    def delete_quote(self, quote_id: int) -> None:
        _ensure_permission(self.current_user, PERM_CONTENT_MANAGE)
        obj = crud.get_daily_quote(self.db, quote_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily quote not found")
        crud.delete_daily_quote(self.db, obj)
