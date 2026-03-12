from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import (
    AudioResource,
    AppUser,
    Base,
    SysPermission,
    SysRole,
    SysRolePerm,
    SysUser,
    SysUserRole,
    UserAudioPlayback,
    UserSleepRecord,
)
from db.session import engine, SessionLocal


def init_db() -> None:
    """
    Initializes the database with required data for the first run.

    This script performs the following actions:
    1. Creates all database tables based on the defined models.
    2. Creates a default super-admin user (admin/admin123).
    3. Creates a 'SUPER_ADMIN' role.
    4. Creates a set of essential permissions for all features.
    5. Assigns the 'SUPER_ADMIN' role to the admin user.
    6. Assigns all created permissions to the 'SUPER_ADMIN' role.

    It is safe to run this script multiple times; it will only add data that doesn't already exist.
    """
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Check for existing admin
        admin = db.query(SysUser).filter(SysUser.username == "admin").first()
        if not admin:
            admin = SysUser(
                username="admin",
                password_hash=get_password_hash("admin123"),
                status=1,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        role = db.query(SysRole).filter(SysRole.role_code == "SUPER_ADMIN").first()
        if not role:
            role = SysRole(role_name="Super Admin", role_code="SUPER_ADMIN")
            db.add(role)
            db.commit()
            db.refresh(role)

        # Bind user-role
        if role not in admin.roles:
            admin.roles.append(role)
            db.add(admin)
            db.commit()
            db.refresh(admin)

        # Permissions
        perm_codes = {
            "audio:read": "Read audio resources",
            "audio:create": "Create audio resources",
            "audio:update": "Update audio resources",
            "audio:delete": "Delete audio resources",
            "rbac:manage": "Manage operator users/roles/permissions",
            "app_user:create": "Create app users",
            "app_user:read": "Read app users",
            "sleep_record:create": "Create user sleep records",
            "sleep_record:read": "Read user sleep records",
            "audio_playback:create": "Create user audio playbacks",
            "audio_playback:read": "Read user audio playbacks",
        }

        for code, name in perm_codes.items():
            perm = db.query(SysPermission).filter(SysPermission.perm_code == code).first()
            if not perm:
                perm = SysPermission(perm_name=name, perm_code=code)
                db.add(perm)
                db.commit()
                db.refresh(perm)
            if perm not in role.permissions:
                role.permissions.append(perm)
                db.add(role)
                db.commit()
                db.refresh(role)

        print("Database initialized. Admin user: admin / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

