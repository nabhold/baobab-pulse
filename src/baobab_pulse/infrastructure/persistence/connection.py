"""asyncpg connection pool management.

A thin wrapper, not an ORM (item 62 leaves the choice of persistence
technology to the org's physical ADR; asyncpg direct is this scaffold's
temporary implementation constraint since it needs no schema to prove
connectivity works). Readiness probing lives here because
``api.routers.health`` needs to answer "is PostgreSQL usable?" without
owning connection lifecycle itself.
"""

from __future__ import annotations

import asyncpg


class Database:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(self._dsn, min_size=1, max_size=10)

    async def disconnect(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def is_ready(self) -> bool:
        if self._pool is None:
            return False
        try:
            async with self._pool.acquire() as connection:
                await connection.execute("SELECT 1")
            return True
        except (OSError, asyncpg.PostgresError):
            return False

    @property
    def pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("Database.connect() must be called before use")
        return self._pool
