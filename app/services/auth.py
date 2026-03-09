from __future__ import annotations

from sqlalchemy.orm import Session

from app import crud
from app.core.security import create_access_token, verify_password
from app.models import SysUser
from app.schemas import Token, UserWithPerms


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate(self, username: str, password: str) -> Token | None:
        user = crud.get_user_by_username(self.db, username=username)
        if not user or not user.status:
            return None
        if not verify_password(password, user.password_hash):
            return None
        token = create_access_token(subject=str(user.id))
        return Token(access_token=token)

    def load_current_user(self, user_id: int) -> UserWithPerms | None:
        user = self.db.get(SysUser, user_id)
        if not user or not user.status:
            return None
        perm_codes = crud.get_user_permissions(self.db, user_id=user.id)
        return UserWithPerms(
            id=user.id,
            username=user.username,
            is_active=bool(user.status),
            permissions=perm_codes,
        )

