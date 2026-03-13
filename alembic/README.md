# Alembic migrations

Migrations keep your database schema in sync with the SQLAlchemy models.

## First time (apply current changes)

1. Install deps: `pip install -r requirements.txt`
2. Ensure `.env` has correct `MYSQL_*` (or DB URL is set).
3. Run:
   ```bash
   alembic upgrade head
   ```
   This will:
   - Create tables `daily_quote` and `user_activity_record` if they don't exist.
   - Add columns to `app_user` (wechat_openid, register_time, device_mac) and to `audio_resource` (category, scene_tags, duration) if those tables exist and columns are missing.

## After you change models (new fields / new tables)

1. Generate a new migration:
   ```bash
   alembic revision --autogenerate -m "describe your change"
   ```
2. Review the new file under `alembic/versions/`.
3. Apply it:
   ```bash
   alembic upgrade head
   ```

## Other commands

- `alembic current` — show current revision.
- `alembic history` — list revisions.
- `alembic downgrade -1` — undo last migration (use with care).
