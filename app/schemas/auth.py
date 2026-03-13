from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    user_type: str | None = None  # "app" for app-user JWT, absent for admin JWT


class LoginRequest(BaseModel):
    username: str
    password: str


# App-user login: phone or wechat_openid
class AppLoginRequest(BaseModel):
    phone: str | None = None
    wechat_openid: str | None = None


class UserBase(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True


class UserWithPerms(UserBase):
    permissions: list[str]


class Message(BaseModel):
    message: str

