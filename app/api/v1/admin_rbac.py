from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.schemas import (
    MessageOut,
    SysPermissionCreate,
    SysPermissionListResponse,
    SysPermissionOut,
    SysRoleCreate,
    SysRoleListResponse,
    SysRoleOut,
    SysUserCreate,
    SysUserListResponse,
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


@router.get("/users", response_model=SysUserListResponse)
def list_users(
    page: int = 1,
    size: int = 20,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysUserListResponse:
    return svc.list_users(page=page, size=size)


@router.post("/roles", response_model=SysRoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    data: SysRoleCreate,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysRoleOut:
    return svc.create_role(data)


@router.get("/roles", response_model=SysRoleListResponse)
def list_roles(
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysRoleListResponse:
    return svc.list_roles()


@router.post("/permissions", response_model=SysPermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(
    data: SysPermissionCreate,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysPermissionOut:
    return svc.create_permission(data)


@router.get("/permissions", response_model=SysPermissionListResponse)
def list_permissions(
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> SysPermissionListResponse:
    return svc.list_permissions()


@router.post("/users/{user_id}/roles/{role_code}", response_model=MessageOut)
def assign_role(
    user_id: int,
    role_code: str,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> MessageOut:
    return svc.assign_role_to_user(user_id=user_id, role_code=role_code)


@router.delete("/users/{user_id}/roles/{role_code}", response_model=MessageOut)
def revoke_role(
    user_id: int,
    role_code: str,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> MessageOut:
    return svc.revoke_role_from_user(user_id=user_id, role_code=role_code)


@router.post("/roles/{role_code}/permissions/{perm_code}", response_model=MessageOut)
def assign_permission(
    role_code: str,
    perm_code: str,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> MessageOut:
    return svc.assign_permission_to_role(role_code=role_code, perm_code=perm_code)


@router.delete("/roles/{role_code}/permissions/{perm_code}", response_model=MessageOut)
def revoke_permission(
    role_code: str,
    perm_code: str,
    svc: RbacAdminService = Depends(get_rbac_admin_service),
) -> MessageOut:
    return svc.revoke_permission_from_role(role_code=role_code, perm_code=perm_code)

