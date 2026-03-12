from __future__ import annotations

from typing import Iterable, Optional, Sequence, Tuple

from sqlalchemy import func, select
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


def get_user(db: Session, user_id: int) -> SysUser | None:
    return db.get(SysUser, user_id)


def list_users(db: Session, page: int, size: int) -> Tuple[int, list[SysUser]]:
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    total = db.execute(select(func.count()).select_from(SysUser)).scalar_one()
    stmt = (
        select(SysUser)
        .order_by(SysUser.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()
    return total, items


def get_role_by_code(db: Session, role_code: str) -> SysRole | None:
    stmt = select(SysRole).where(SysRole.role_code == role_code)
    return db.execute(stmt).scalar_one_or_none()


def list_roles(db: Session) -> list[SysRole]:
    stmt = select(SysRole).order_by(SysRole.id.desc())
    return db.execute(stmt).scalars().all()


def get_permission_by_code(db: Session, perm_code: str) -> SysPermission | None:
    stmt = select(SysPermission).where(SysPermission.perm_code == perm_code)
    return db.execute(stmt).scalar_one_or_none()


def list_permissions(db: Session) -> list[SysPermission]:
    stmt = select(SysPermission).order_by(SysPermission.id.desc())
    return db.execute(stmt).scalars().all()


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


def remove_user_role(db: Session, user: SysUser, role: SysRole) -> bool:
    if role in user.roles:
        user.roles.remove(role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return True
    return False


def remove_role_permission(db: Session, role: SysRole, perm: SysPermission) -> bool:
    if perm in role.permissions:
        role.permissions.remove(perm)
        db.add(role)
        db.commit()
        db.refresh(role)
        return True
    return False

