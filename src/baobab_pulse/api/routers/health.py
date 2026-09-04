"""Liveness/readiness (item 117).

Readiness distinguishes whether mandatory dependencies are usable — a
process that is alive but cannot reach PostgreSQL is not ready to serve
traffic that needs it.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from baobab_pulse.api.dependencies import get_database
from baobab_pulse.infrastructure.persistence.connection import Database

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/readyz")
async def readiness(database: Database = Depends(get_database)) -> JSONResponse:
    database_ready = await database.is_ready()
    body = {"status": "ready" if database_ready else "not_ready", "dependencies": {"database": database_ready}}
    return JSONResponse(status_code=200 if database_ready else 503, content=body)
