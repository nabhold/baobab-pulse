"""Observation — the foundational semantic unit of Pulse intelligence.

"An Observation is a statement that a measurable, categorical or stateful
property of a subject had a particular value within a defined temporal and
contextual scope." (ARCH-PULSE-CIM-001 §23). Field list: CIM §23-25,
cross-checked against the canonical kernel in ADR-PULSE-005 §4.

AGG-PULSE-005/006: published intelligence is immutable or versioned. Once
published, an Observation's semantic content is immutable (ADR-PULSE-002
§2.2); a revision becomes a *new* Observation linked via
``supersedes_id``/``superseded_by_id`` — it never overwrites the original
(PULSE-008, EVD-PULSE governing the same rule for raw evidence).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.enums import Missingness
from baobab_pulse.domain.shared.value_objects import (
    Confidence,
    GeographicContext,
    MarketContext,
    QualityProfile,
    Reference,
    TemporalContext,
)


class ObservationValueType(StrEnum):
    """ADR-PULSE-005 §16."""

    DECIMAL = "DECIMAL"
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    CATEGORY = "CATEGORY"
    DATE = "DATE"
    DATETIME = "DATETIME"
    MONEY = "MONEY"
    QUANTITY = "QUANTITY"
    PERCENTAGE = "PERCENTAGE"
    RATE = "RATE"
    INDEX = "INDEX"
    REFERENCE = "REFERENCE"


class ObservationStatus(StrEnum):
    """Pulse's own derivation (ARCH-PULSE-CIM-001 §187 leaves lifecycle
    naming to the implementation) of the immutability/versioning rule in
    ADR-PULSE-002 §2.2."""

    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    SUPERSEDED = "SUPERSEDED"
    RETRACTED = "RETRACTED"


class Observation(GovernedEntity):
    """Aggregate root. Frozen: a published Observation's semantic content is
    immutable — see module docstring."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["observation"] = "observation"
    subject_reference: Reference
    metric: str
    value: float | str | bool | None
    value_type: ObservationValueType
    missingness: Missingness | None = None
    unit: str | None = None
    currency: str | None = None
    geography: GeographicContext = GeographicContext()
    market: MarketContext = MarketContext()
    temporal_context: TemporalContext
    source_id: str
    dataset_id: str | None = None
    quality_profile: QualityProfile = QualityProfile()
    confidence: Confidence | None = None
    status: ObservationStatus = ObservationStatus.PUBLISHED
    revision: int = 1
    supersedes_id: str | None = None
    superseded_by_id: str | None = None
    metadata: dict[str, str] = {}


class Measurement(Observation):
    """A specialised, strictly numeric Observation (ARCH-PULSE-CIM-001 §26:
    an IS-A relationship, not a separate aggregate)."""

    type: Literal["measurement"] = "measurement"  # type: ignore[assignment]
    value: float
    value_type: Literal[ObservationValueType.DECIMAL, ObservationValueType.INTEGER] = (
        ObservationValueType.DECIMAL
    )
