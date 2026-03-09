from __future__ import annotations

from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SysPermission, SysRole, SysRolePerm, SysUser, SysUserRole


def get_user_by_username(db: Session, username: str) -> SysUser | None:
    stmt = select(SysUser).where(SysUser.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_permissions(db: Session, user_id: int) -> list[str]:
    stmt = (
        select(SysPermission.perm_code)
        .join(SysRolePerm, SysRolePerm.perm_id == SysPermission.id)
        .join(SysRole, SysRole.id == SysRolePerm.role_id)
        .join(SysUserRole, SysUserRole.role_id == SysRole.id)
        .where(SysUserRole.user_id == user_id)
    )
    rows = db.execute(stmt).scalars().all()
    # ensure unique
    return sorted(set(rows))


def create_user(db: Session, user: SysUser) -> SysUser:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_role(db: Session, role: SysRole) -> SysRole:
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def create_permission(db: Session, perm: SysPermission) -> SysPermission:
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def ensure_user_role(db: Session, user: SysUser, role: SysRole) -> None:
    if role not in user.roles:
        user.roles.append(role)
        db.add(user)
        db.commit()
        db.refresh(user)


def ensure_role_permission(db: Session, role: SysRole, perm: SysPermission) -> None:
    if perm not in role.permissions:
        role.permissions.append(perm)
        db.add(role)
        db.commit()
        db.refresh(role)

