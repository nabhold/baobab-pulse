"""A deterministic, in-memory ``SourceAdapter`` — no network calls.

Used by contract tests to prove the ``SourceAdapter`` port and the
acquisition -> RawRecord flow work end-to-end without any external
dependency or credential (item 95-96). Not a template for a real provider
adapter's error handling/pagination — those are provider-specific concerns
a real adapter owns per ADR-PULSE-003 §25.
"""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from baobab_pulse.domain.ingestion import RawRecord
from baobab_pulse.domain.shared.identifiers import new_id


class ReferenceSourceAdapter:
    """Serves whatever records it was constructed with, as if they had been
    fetched from a real provider."""

    def __init__(self, dataset_records: dict[str, list[dict[str, Any]]]) -> None:
        self._dataset_records = dataset_records
        self._acquisition_id = new_id("acq")

    def describe(self) -> dict[str, Any]:
        return {"name": "reference-adapter", "version": "1", "modes": ["MANUAL"]}

    async def discover_datasets(self) -> list[str]:
        return list(self._dataset_records.keys())

    def validate_configuration(self, configuration: dict[str, Any]) -> None:
        return None

    async def validate_credentials(self) -> bool:
        return True

    async def plan_acquisition(self, dataset_id: str, *, cursor: str | None = None) -> dict[str, Any]:
        return {"dataset_id": dataset_id, "batch_size": len(self._dataset_records.get(dataset_id, []))}

    async def acquire(self, dataset_id: str, *, cursor: str | None = None) -> list[RawRecord]:
        records = self._dataset_records.get(dataset_id, [])
        retrieved_at = datetime.now(UTC)
        raw_records = []
        for record in records:
            payload = str(record).encode("utf-8")
            raw_records.append(
                RawRecord(
                    id=new_id("raw"),
                    acquisition_id=self._acquisition_id,
                    external_record_id=str(record.get("id")),
                    raw_location=f"reference://{dataset_id}",
                    media_type="application/json",
                    content_hash=sha256(payload).hexdigest(),
                    retrieved_at=retrieved_at,
                    metadata={k: str(v) for k, v in record.items()},
                )
            )
        return raw_records

    async def checkpoint(self, dataset_id: str) -> str:
        return "end"

    async def resume(self, dataset_id: str, cursor: str) -> list[RawRecord]:
        return []

    def report_rate_limit(self) -> dict[str, Any] | None:
        return None

    async def report_source_health(self) -> bool:
        return True

    async def close(self) -> None:
        return None
