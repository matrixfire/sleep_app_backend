"""Add new tables and columns (app_user, audio_resource, daily_quote, user_activity_record).

Revision ID: 001
Revises:
Create Date: 2025-03-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    # ----- New tables (create only if missing) -----
    if "daily_quote" not in tables:
        op.create_table(
            "daily_quote",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("show_date", sa.Date(), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("author", sa.String(50), nullable=True),
            sa.Column("bg_image_url", sa.String(255), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("show_date", name="uq_daily_quote_show_date"),
        )

    if "user_activity_record" not in tables:
        op.create_table(
            "user_activity_record",
            sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.BigInteger(), nullable=False),
            sa.Column("activity_type", sa.String(20), nullable=False),
            sa.Column("start_time", sa.DateTime(), nullable=False),
            sa.Column("end_time", sa.DateTime(), nullable=True),
            sa.Column("duration_min", sa.Integer(), nullable=True),
            sa.Column("status", sa.SmallInteger(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["app_user.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_user_activity_record_user_id", "user_activity_record", ["user_id"], unique=False)
        op.create_index("ix_user_activity_record_activity_type", "user_activity_record", ["activity_type"], unique=False)

    # ----- app_user: add new columns (only if table exists; skip if column exists) -----
    if "app_user" in tables:
        app_user_cols = [c["name"] for c in inspector.get_columns("app_user")]
        if "wechat_openid" not in app_user_cols:
            op.add_column("app_user", sa.Column("wechat_openid", sa.String(100), nullable=True))
            op.create_index("ix_app_user_wechat_openid", "app_user", ["wechat_openid"], unique=True)
        if "register_time" not in app_user_cols:
            op.add_column("app_user", sa.Column("register_time", sa.DateTime(), nullable=True, server_default=sa.text("CURRENT_TIMESTAMP")))
            op.execute(sa.text("UPDATE app_user SET register_time = CURRENT_TIMESTAMP WHERE register_time IS NULL"))
            op.alter_column("app_user", "register_time", existing_type=sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"))
        if "device_mac" not in app_user_cols:
            op.add_column("app_user", sa.Column("device_mac", sa.String(50), nullable=True))
        if "nickname" in app_user_cols:
            op.execute(sa.text("UPDATE app_user SET nickname = CONCAT('SleepUser_', id) WHERE nickname IS NULL OR nickname = ''"))
            op.alter_column("app_user", "nickname", existing_type=sa.String(50), nullable=False)

    # ----- audio_resource: add new columns -----
    if "audio_resource" in tables:
        audio_cols = [c["name"] for c in inspector.get_columns("audio_resource")]
        if "category" not in audio_cols:
            op.add_column("audio_resource", sa.Column("category", sa.String(20), nullable=True))
            op.create_index("ix_audio_resource_category", "audio_resource", ["category"], unique=False)
        if "scene_tags" not in audio_cols:
            op.add_column("audio_resource", sa.Column("scene_tags", sa.String(100), nullable=True))
        if "duration" not in audio_cols:
            op.add_column("audio_resource", sa.Column("duration", sa.Integer(), nullable=True))


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "audio_resource" in inspector.get_table_names():
        audio_cols = [c["name"] for c in inspector.get_columns("audio_resource")]
        if "duration" in audio_cols:
            op.drop_column("audio_resource", "duration")
        if "scene_tags" in audio_cols:
            op.drop_column("audio_resource", "scene_tags")
        if "category" in audio_cols:
            op.drop_index("ix_audio_resource_category", table_name="audio_resource")
            op.drop_column("audio_resource", "category")
    if "app_user" in inspector.get_table_names():
        app_user_cols = [c["name"] for c in inspector.get_columns("app_user")]
        if "device_mac" in app_user_cols:
            op.drop_column("app_user", "device_mac")
        if "register_time" in app_user_cols:
            op.drop_column("app_user", "register_time")
        if "wechat_openid" in app_user_cols:
            op.drop_index("ix_app_user_wechat_openid", table_name="app_user")
            op.drop_column("app_user", "wechat_openid")

    op.drop_index("ix_user_activity_record_activity_type", table_name="user_activity_record")
    op.drop_index("ix_user_activity_record_user_id", table_name="user_activity_record")
    op.drop_table("user_activity_record")
    op.drop_table("daily_quote")
