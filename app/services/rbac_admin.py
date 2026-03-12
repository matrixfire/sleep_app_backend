from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.core.security import get_password_hash
from app.models import SysPermission, SysRole, SysUser
from app.schemas import (
    MessageOut,
    SysPermissionCreate,
    SysPermissionOut,
    SysRoleCreate,
    SysRoleOut,
    SysUserCreate,
    SysUserOut,
    UserWithPerms,
)

PERM_RBAC_MANAGE = "rbac:manage"


def _ensure_permission(user: UserWithPerms, perm_code: str) -> None:
    if perm_code not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {perm_code}",
        )


class RbacAdminService:
    """
    A service for admins to manage the permission system itself.

    Allows creating users, roles, and permissions, and linking them together.
    Requires the 'rbac:manage' permission for all actions.
    """

    def __init__(self, db: Session, current_user: UserWithPerms):
        self.db = db
        self.current_user = current_user

    def create_user(self, data: SysUserCreate) -> SysUserOut:
        _ensure_permission(self.current_user, PERM_RBAC_MANAGE)
        existing = crud.get_user_by_username(self.db, username=data.username)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        obj = SysUser(
            username=data.username,
            password_hash=get_password_hash(data.password),
            status=int(data.status),
        )
        obj = crud.create_user(self.db, obj)
        return SysUserOut(
            id=obj.id,
            username=obj.username,
            status=obj.status,
            roles=[r.role_code for r in obj.roles],
        )

    def create_role(self, data: SysRoleCreate) -> SysRoleOut:
        _ensure_permission(self.current_user, PERM_RBAC_MANAGE)
        existing = crud.get_role_by_code(self.db, role_code=data.role_code)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role code already exists")
        obj = SysRole(role_name=data.role_name, role_code=data.role_code)
        obj = crud.create_role(self.db, obj)
        return SysRoleOut.model_validate(obj)

    def create_permission(self, data: SysPermissionCreate) -> SysPermissionOut:
        _ensure_permission(self.current_user, PERM_RBAC_MANAGE)
        existing = crud.get_permission_by_code(self.db, perm_code=data.perm_code)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Permission code already exists")
        obj = SysPermission(perm_name=data.perm_name, perm_code=data.perm_code)
        obj = crud.create_permission(self.db, obj)
        return SysPermissionOut.model_validate(obj)

    def assign_role_to_user(self, user_id: int, role_code: str) -> MessageOut:
        _ensure_permission(self.current_user, PERM_RBAC_MANAGE)
        user = crud.get_user(self.db, user_id=user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        role = crud.get_role_by_code(self.db, role_code=role_code)
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        crud.ensure_user_role(self.db, user=user, role=role)
        return MessageOut(message=f"Role '{role_code}' assigned to user_id={user_id}")

    def assign_permission_to_role(self, role_code: str, perm_code: str) -> MessageOut:
        _ensure_permission(self.current_user, PERM_RBAC_MANAGE)
        role = crud.get_role_by_code(self.db, role_code=role_code)
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        perm = crud.get_permission_by_code(self.db, perm_code=perm_code)
        if perm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        crud.ensure_role_permission(self.db, role=role, perm=perm)
        return MessageOut(message=f"Permission '{perm_code}' assigned to role '{role_code}'")

