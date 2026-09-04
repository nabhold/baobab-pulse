"""SourceAdapter — the port every external source integration implements.

ADR-PULSE-003 §24 gives this method list conceptually and explicitly defers
the exact Python signature to "a later implementation specification"; the
signatures below are Pulse's own derivation, kept intentionally narrow.
Adapters MUST remain isolated from canonical-domain processing
(ADR-PULSE-003 §26, the anti-corruption pipeline: Provider Model -> Provider
Adapter -> Source Record -> Canonical Normaliser -> Pulse Observation) — a
``SourceAdapter`` implementation returns :class:`RawRecord`\\ s, never a
domain ``Observation`` directly.
"""

from __future__ import annotations

from typing import Any, Protocol

from baobab_pulse.domain.ingestion import RawRecord


class SourceAdapter(Protocol):
    def describe(self) -> dict[str, Any]:
        """Static, provider-facing metadata (name, version, supported
        acquisition modes) — never anything tenant- or request-specific."""
        ...

    async def discover_datasets(self) -> list[str]: ...

    def validate_configuration(self, configuration: dict[str, Any]) -> None:
        """Raise on invalid configuration; never silently coerce it."""
        ...

    async def validate_credentials(self) -> bool: ...

    async def plan_acquisition(self, dataset_id: str, *, cursor: str | None = None) -> dict[str, Any]:
        """Return an acquisition plan (e.g. request batches, pagination
        strategy) without performing any network I/O yet."""
        ...

    async def acquire(self, dataset_id: str, *, cursor: str | None = None) -> list[RawRecord]: ...

    async def checkpoint(self, dataset_id: str) -> str:
        """Return an opaque cursor a later :meth:`acquire`/:meth:`resume`
        call can use to continue where this run left off."""
        ...

    async def resume(self, dataset_id: str, cursor: str) -> list[RawRecord]: ...

    def report_rate_limit(self) -> dict[str, Any] | None:
        """Return the provider's current rate-limit state if known, else
        ``None`` — never guessed."""
        ...

    async def report_source_health(self) -> bool: ...

    async def close(self) -> None: ...
