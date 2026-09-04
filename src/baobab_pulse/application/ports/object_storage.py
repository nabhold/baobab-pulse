"""ObjectStoragePort — the Raw Evidence Vault's storage side.

ADR-PULSE-004 §7: PostgreSQL holds metadata/lineage/indexes; object storage
holds source artefacts. This port is intentionally minimal (put/get/exists)
— no bucket-naming or retention policy is encoded here, that is an
infrastructure-adapter and ``RetentionPolicy`` (domain-level) concern.
"""

from __future__ import annotations

from typing import Protocol


class ObjectStoragePort(Protocol):
    async def put(self, key: str, data: bytes, *, content_type: str) -> str:
        """Store ``data`` and return its storage reference (never the raw
        key alone — see ADR-PULSE-004 §8: identity must stay independent of
        bucket key)."""
        ...

    async def get(self, storage_reference: str) -> bytes: ...

    async def exists(self, storage_reference: str) -> bool: ...
