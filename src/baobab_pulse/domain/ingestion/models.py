"""Acquisition and RawRecord — L0/L1 of the evidence-layer stack.

Field lists: ARCH-PULSE-CIM-001 §18-21. Evidence layering: ADR-PULSE-004 §2
(``L0 SourceArtefact -> L1 RawRecord -> L2 NormalisedRecord ->
L3 Observation -> L4 DerivedEvidence``). ``SourceArtefact`` and
``NormalisedRecord`` are infrastructure/ingestion-pipeline concerns (raw
bytes in object storage, transient normalisation state) rather than
persisted domain aggregates, so only ``Acquisition`` and ``RawRecord`` are
modelled here; see ``infrastructure.object_storage`` and
``ingestion.pipelines`` for L0/L2.

EVD-PULSE-004: a RawRecord SHALL be immutable once successfully persisted —
hence ``frozen=True``. A later source revision produces a *new* RawRecord,
never an in-place edit.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import CanonicalEntity
from baobab_pulse.domain.shared.enums import Classification


class AcquisitionMode(StrEnum):
    """ARCH-PULSE-CIM-001 §19 / ADR-PULSE-003 §41 / ADR-PULSE-007 §24.

    The union of every acquisition-mode enumeration across the governing
    ADRs (ADR-PULSE-003's list additionally has ``MANUAL_RESEARCH`` and
    ``ON_DEMAND``; CIM's has ``MANUAL`` and ``EVENT_DRIVEN``) — kept as one
    superset rather than reconciled down, since the ADRs themselves were not
    reconciled with each other on this point.
    """

    LIVE = "LIVE"
    SCHEDULED = "SCHEDULED"
    EVENT_DRIVEN = "EVENT_DRIVEN"
    BACKFILL = "BACKFILL"
    REPROCESS = "REPROCESS"
    CORRECTION = "CORRECTION"
    MANUAL = "MANUAL"
    MANUAL_RESEARCH = "MANUAL_RESEARCH"
    ON_DEMAND = "ON_DEMAND"


class AcquisitionStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class Acquisition(CanonicalEntity):
    """Aggregate root. Invariants (ADR-PULSE-002 §2.2): ``started_at <=
    completed_at`` where both are set; ``accepted + rejected <= received``
    unless provider semantics differ; a completed Acquisition never reverts
    to running."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["acquisition"] = "acquisition"
    data_source_id: str
    dataset_id: str | None = None
    mode: AcquisitionMode
    started_at: datetime
    completed_at: datetime | None = None
    status: AcquisitionStatus = AcquisitionStatus.PENDING
    cursor: str | None = None
    records_received: int = 0
    records_accepted: int = 0
    records_rejected: int = 0
    checksum: str | None = None
    error_summary: str | None = None
    metadata: dict[str, str] = {}

    def check_invariants(self) -> None:
        from baobab_pulse.domain.shared.errors import InvariantViolation

        if self.completed_at is not None and self.completed_at < self.started_at:
            raise InvariantViolation("Acquisition.completed_at cannot precede started_at")
        if self.records_accepted + self.records_rejected > self.records_received:
            raise InvariantViolation("Acquisition accepted+rejected cannot exceed received")


class RawRecord(CanonicalEntity):
    """L1. Immutable once persisted (EVD-PULSE-004)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["raw_record"] = "raw_record"
    acquisition_id: str
    external_record_id: str | None = None
    raw_location: str
    media_type: str
    source_schema_version: str | None = None
    content_hash: str
    observed_at: datetime | None = None
    published_at: datetime | None = None
    retrieved_at: datetime
    classification: Classification = Classification.BAOBAB_INTERNAL
    metadata: dict[str, str] = {}
