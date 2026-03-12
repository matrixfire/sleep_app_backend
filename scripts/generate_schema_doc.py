r"""
Regenerate the database schema section of BACKEND_STATUS.md from SQLAlchemy models.
Run from project root:
  .\.venv\Scripts\python.exe scripts\generate_schema_doc.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Project root on path so "app" resolves
_repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_repo_root))
repo_root = _repo_root

# Ensure all models are registered with Base.metadata
from app.models import Base  # noqa: F401
from app.models import (
    app_user,
    audio,
    rbac,
    user_audio_playback,
    user_sleep_record,
)
# Keep modules so tables are registered
_ = (app_user, audio, rbac, user_audio_playback, user_sleep_record)

# Short purpose per table (edit here when adding tables)
TABLE_PURPOSES: dict[str, str] = {
    "sys_user": "Admin/operator accounts (login with username + password).",
    "sys_role": "Roles (e.g. SUPER_ADMIN, CONTENT_OP).",
    "sys_permission": "Permission codes (e.g. audio:read, rbac:manage).",
    "sys_user_role": "Many-to-many: which users have which roles.",
    "sys_role_perm": "Many-to-many: which roles have which permissions.",
    "audio_resource": "Audio metadata (title, cover_url, audio_url) for Tide content.",
    "app_user": "App-side users (Tide end-users); minimal fields for now.",
    "user_sleep_record": "One record per sleep session; raw data stored at URL, not in DB.",
    "user_audio_playback": "Playback events (what was played, when, for how long).",
}


def _col_type_str(col) -> str:
    t = type(col.type).__name__
    if "Int" in t or "BigInteger" in t:
        return "int" if "Big" not in t else "bigint"
    if "String" in t or "Varchar" in t:
        return "string"
    if "Text" in t:
        return "text"
    if "DateTime" in t or "Date" in t:
        return "datetime"
    if "Boolean" in t:
        return "bool"
    return t.lower()


def _mermaid_attr(col) -> str:
    parts = [_col_type_str(col), col.name]
    for fk in col.foreign_keys:
        parts.append("FK")
        break
    if col.primary_key:
        parts.append("PK")
    if col.unique:
        parts.append("UK")
    return " ".join(parts)


def _constraint_str(col) -> str:
    out = []
    if col.primary_key:
        out.append("PK, autoincrement" if col.autoincrement else "PK")
    for fk in col.foreign_keys:
        out.append(f"FK → {fk.column.table.name}.{fk.column.name}")
    if col.unique:
        out.append("unique")
    if not col.nullable and not col.primary_key:
        out.append("not null")
    if getattr(col.type, "default", None) is not None:
        out.append("default")
    return ", ".join(out) if out else "—"


def build_mermaid() -> str:
    lines = ["erDiagram"]
    # Relationships: ref_table (one) ||--o{ table_with_fk (many)
    for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
        for col in table.c:
            for fk in col.foreign_keys:
                ref_table = fk.column.table.name
                lines.append(f'    {ref_table} ||--o{{ {table.name} : "{col.name}"')
    # Entity blocks
    for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
        lines.append(f"    {table.name} {{")
        for col in table.c:
            lines.append(f"        {_mermaid_attr(col)}")
        lines.append("    }")
    return "\n".join(lines)


def build_tables_summary() -> str:
    lines = [
        "| Table | Purpose |",
        "|-------|--------|",
    ]
    for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
        purpose = TABLE_PURPOSES.get(table.name, "—")
        lines.append(f"| **{table.name}** | {purpose} |")
    return "\n".join(lines)


def build_column_details() -> str:
    out = []
    for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
        out.append(f"**{table.name}**  ")
        out.append("| Column | Type | Constraints |")
        out.append("|--------|------|-------------|")
        for col in table.c:
            typ = type(col.type).__name__
            const = _constraint_str(col)
            out.append(f"| {col.name} | {typ} | {const} |")
        out.append("")
    return "\n".join(out)


def main() -> None:
    md_path = repo_root / "BACKEND_STATUS.md"

    mermaid = build_mermaid()
    summary = build_tables_summary()
    columns = build_column_details()

    # Windows path with single backslashes for the generated doc
    bash_cmd = ".\\" + r".venv\Scripts\python.exe scripts\generate_schema_doc.py"

    gen_block = f"""<!-- SCHEMA_GEN_START -->
### 1.1 Entity–relationship diagram

The diagram below is generated from the SQLAlchemy models. To refresh it after schema changes, run:

```bash
{bash_cmd}
```

```mermaid
{mermaid}
```

### 1.2 Tables summary

{summary}

### 1.3 Column details

{columns}
<!-- SCHEMA_GEN_END -->"""

    text = md_path.read_text(encoding="utf-8")
    if "<!-- SCHEMA_GEN_START -->" not in text or "<!-- SCHEMA_GEN_END -->" not in text:
        print("BACKEND_STATUS.md does not contain SCHEMA_GEN_START/END markers. Add them around the schema section.")
        return
    def repl(_m):
        return gen_block

    new_text = re.sub(
        r"<!-- SCHEMA_GEN_START -->.*?<!-- SCHEMA_GEN_END -->",
        repl,
        text,
        flags=re.DOTALL,
    )
    md_path.write_text(new_text, encoding="utf-8")
    print("Updated BACKEND_STATUS.md schema section.")


if __name__ == "__main__":
    main()
