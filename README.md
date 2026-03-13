# sleep_app_backend

FastAPI backend for the Sleep Device IoT + content distribution platform.

## Features (MVP)

- 5-layer architecture: Router / Schemas / Services / CRUD / Models
- Admin authentication: JWT login for `sys_user`
- Fine-grained RBAC permissions checked in Service layer
- Admin audio resource CRUD: `/api/v1/admin/audios`

## Quickstart (Windows PowerShell)

1. Create venv and install deps:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure env:

```bash
copy .env.example .env
```

3. Run API:

```bash
uvicorn main:app --reload
```

Open docs at `http://127.0.0.1:8000/docs`.

## Database

This project uses MySQL. Create the database specified by `MYSQL_DB`.

To create tables (simple dev bootstrap):

```bash
python -m app.scripts.init_db
```

## Default RBAC bootstrap

The init script creates:

- An admin user: `admin / admin123`
- Permissions: `audio:read`, `audio:create`, `audio:update`, `audio:delete`
- Role: `SUPER_ADMIN` with all permissions

