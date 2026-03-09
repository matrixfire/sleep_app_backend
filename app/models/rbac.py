from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SysUser(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    roles: Mapped[list["SysRole"]] = relationship(
        "SysRole",
        secondary="sys_user_role",
        back_populates="users",
        lazy="selectin",
    )


class SysRole(Base):
    __tablename__ = "sys_role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False)
    role_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[list[SysUser]] = relationship(
        "SysUser",
        secondary="sys_user_role",
        back_populates="roles",
        lazy="selectin",
    )
    permissions: Mapped[list["SysPermission"]] = relationship(
        "SysPermission",
        secondary="sys_role_perm",
        back_populates="roles",
        lazy="selectin",
    )


class SysPermission(Base):
    __tablename__ = "sys_permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    perm_name: Mapped[str] = mapped_column(String(50), nullable=False)
    perm_code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    roles: Mapped[list[SysRole]] = relationship(
        "SysRole",
        secondary="sys_role_perm",
        back_populates="permissions",
        lazy="selectin",
    )


class SysUserRole(Base):
    __tablename__ = "sys_user_role"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_sys_user_role"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("sys_user.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("sys_role.id"), primary_key=True)


class SysRolePerm(Base):
    __tablename__ = "sys_role_perm"
    __table_args__ = (UniqueConstraint("role_id", "perm_id", name="uq_sys_role_perm"),)

    role_id: Mapped[int] = mapped_column(ForeignKey("sys_role.id"), primary_key=True)
    perm_id: Mapped[int] = mapped_column(ForeignKey("sys_permission.id"), primary_key=True)

