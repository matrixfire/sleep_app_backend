from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
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
from app.services.rbac_admin import RbacAdminService
from db.session import get_db

router = APIRouter(prefix="/admin/rbac", tags=["admin-rbac"])


def get_rbac_admin_service(
    db: Session = Depends(get_db),
    current_user: UserWithPerms = Depends(get_current_user),
) -> RbacAdminService:
    return RbacAdminService(db=db, current_user=current_user)


@router.post("/users", response_model=SysUserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: SysUserCreate,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysUserOut:
    return svc.create_user(data)


@router.post("/roles", response_model=SysRoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    data: SysRoleCreate,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysRoleOut:
    return svc.create_role(data)


@router.post("/permissions", response_model=SysPermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(
    data: SysPermissionCreate,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysPermissionOut:
    return svc.create_permission(data)


@router.post("/users/{user_id}/roles/{role_code}", response_model=MessageOut)
def assign_role(
    user_id: int,
    role_code: str,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> MessageOut:
    return svc.assign_role_to_user(user_id=user_id, role_code=role_code)


@router.post("/roles/{role_code}/permissions/{perm_code}", response_model=MessageOut)
def assign_permission(
    role_code: str,
    perm_code: str,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> MessageOut:
    return svc.assign_permission_to_role(role_code=role_code, perm_code=perm_code)

