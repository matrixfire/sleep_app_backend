from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app import crud
from app.core.security import create_access_token
from app.models import AppUser
from app.schemas import AppUserOut, Token


class AppAuthService:
    """Authentication for app end-users (phone or WeChat)."""

    def __init__(self, db: Session):
        self.db = db

    def login(self, phone: str | None = None, wechat_openid: str | None = None) -> Token | None:
        """Find or create app user by phone or wechat_openid; return JWT with user_type=app."""
        if not phone and not wechat_openid:
            return None
        user: AppUser | None = None
        if phone:
            user = crud.get_app_user_by_mobile(self.db, phone)
        if not user and wechat_openid:
            user = crud.get_app_user_by_wechat_openid(self.db, wechat_openid)
        if not user:
            nickname = "SleepUser_" + uuid.uuid4().hex[:8]
            user = AppUser(
                mobile=phone,
                wechat_openid=wechat_openid,
                nickname=nickname,
            )
            user = crud.create_app_user(self.db, user)
        token = create_access_token(
            subject=str(user.id),
            extra_claims={"user_type": "app"},
        )
        return Token(access_token=token)

    def get_me(self, user_id: int) -> AppUserOut | None:
        """Load app user by id for /auth/me."""
        user = crud.get_app_user(self.db, user_id)
        if not user:
            return None
        return AppUserOut.model_validate(user)
