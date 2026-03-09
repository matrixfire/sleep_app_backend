from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class LoginRequest(BaseModel):
    username: str
    password: str


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

