from __future__ import annotations

from pydantic import BaseModel, Field


class SysUserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    status: int = 1


class SysUserOut(BaseModel):
    id: int
    username: str
    status: int
    roles: list[str] = []

    class Config:
        from_attributes = True


class SysUserListResponse(BaseModel):
    total: int
    items: list[SysUserOut]


class SysRoleCreate(BaseModel):
    role_name: str = Field(min_length=1, max_length=50)
    role_code: str = Field(min_length=1, max_length=50)


class SysRoleOut(BaseModel):
    id: int
    role_name: str
    role_code: str

    class Config:
        from_attributes = True


class SysRoleListResponse(BaseModel):
    items: list[SysRoleOut]


class SysPermissionCreate(BaseModel):
    perm_name: str = Field(min_length=1, max_length=50)
    perm_code: str = Field(min_length=1, max_length=100)


class SysPermissionOut(BaseModel):
    id: int
    perm_name: str
    perm_code: str

    class Config:
        from_attributes = True


class SysPermissionListResponse(BaseModel):
    items: list[SysPermissionOut]


class MessageOut(BaseModel):
    message: str

