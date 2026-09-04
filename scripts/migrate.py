"""Apply pending SQL migrations from migrations/*.sql, in filename order.

Deliberately not Alembic/a full migration framework (item 63: "create only
foundational migrations necessary for proving the scaffold") — a
lockfile-tracked table of applied filenames plus plain SQL files is enough
to prove the mechanism and is trivial to replace once the physical model
(ADR-PULSE-011) grows large enough to need one.

Usage: `uv run python scripts/migrate.py` (or `make migrate`).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import asyncpg

from baobab_pulse.configuration.settings import Settings

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


async def main() -> None:
    settings = Settings()
    connection = await asyncpg.connect(settings.database_url)
    try:
        await connection.execute(
            "CREATE TABLE IF NOT EXISTS public.schema_migrations "
            "(filename TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        )
        applied = {row["filename"] for row in await connection.fetch("SELECT filename FROM public.schema_migrations")}

        for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if migration_file.name in applied:
                continue
            print(f"Applying {migration_file.name}...")
            async with connection.transaction():
                await connection.execute(migration_file.read_text(encoding="utf-8"))
                await connection.execute(
                    "INSERT INTO public.schema_migrations (filename) VALUES ($1)", migration_file.name
                )
        print("Migrations up to date.")
    finally:
        await connection.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (OSError, asyncpg.PostgresError) as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        sys.exit(1)
