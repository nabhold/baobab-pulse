"""In-memory ``ObjectStoragePort`` — tests and local development only.

A real deployment binds an S3-compatible client here once actual raw-artefact
volume exists (item 116: avoid unnecessary services until justified). The
storage reference format (``mem://<key>``) is deliberately opaque — callers
must never construct or parse it themselves (ADR-PULSE-004 §8: identity
stays independent of bucket/key structure).
"""

from __future__ import annotations

from baobab_pulse.domain.shared.identifiers import new_id


class InMemoryObjectStorage:
    def __init__(self) -> None:
        self._objects: dict[str, bytes] = {}

    async def put(self, key: str, data: bytes, *, content_type: str) -> str:
        reference = f"mem://{new_id('obj')}"
        self._objects[reference] = data
        return reference

    async def get(self, storage_reference: str) -> bytes:
        return self._objects[storage_reference]

    async def exists(self, storage_reference: str) -> bool:
        return storage_reference in self._objects
