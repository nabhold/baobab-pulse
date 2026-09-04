"""In-memory ``Repository[T]`` implementation.

Satisfies ``application.ports.repositories.Repository`` for tests, examples,
and local development without requiring PostgreSQL — this is what makes the
core test suite runnable with no external services (item 96, architecture
test #6 is about credentials specifically, but the same principle extends to
not needing a live database for unit/contract tests).
"""

from __future__ import annotations

from typing import Protocol


class _HasId(Protocol):
    id: str


class InMemoryRepository[T: _HasId]:
    def __init__(self) -> None:
        self._store: dict[str, T] = {}

    async def get(self, entity_id: str) -> T | None:
        return self._store.get(entity_id)

    async def add(self, entity: T) -> None:
        self._store[entity.id] = entity
