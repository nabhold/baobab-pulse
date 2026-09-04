"""Insight — an interpreted statement supported by evidence.

ARCH-PULSE-CIM-001 §48-52. Invariant (ADR-PULSE-002 §2.2): a published
Insight SHOULD have at least one Analysis and SHALL have at least one
EvidenceSet, except when explicitly classified as human-authored
opinion/hypothesis.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.enums import ConfidenceBand
from baobab_pulse.domain.shared.errors import InvariantViolation
from baobab_pulse.domain.shared.value_objects import Confidence, Reference


class InsightType(StrEnum):
    """ARCH-PULSE-CIM-001 §50."""

    MARKET = "MARKET"
    TRADE = "TRADE"
    FINANCIAL = "FINANCIAL"
    OPERATIONAL = "OPERATIONAL"
    REGULATORY = "REGULATORY"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    CUSTOMER = "CUSTOMER"
    COMPETITIVE = "COMPETITIVE"
    MACROECONOMIC = "MACROECONOMIC"
    GEOSPATIAL = "GEOSPATIAL"
    WEATHER = "WEATHER"
    STRATEGIC = "STRATEGIC"
    OTHER = "OTHER"


class InsightStatus(StrEnum):
    """ARCH-PULSE-CIM-001 §51."""

    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    PUBLISHED = "PUBLISHED"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"
    WITHDRAWN = "WITHDRAWN"
    REJECTED = "REJECTED"


class Insight(GovernedEntity):
    """Aggregate root. Frozen — a versioned aggregate (AGG-PULSE-005/CIM §63)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["insight"] = "insight"
    title: str
    statement: str
    insight_type: InsightType
    subject_reference: Reference
    evidence_set_id: str | None = None
    analysis_references: tuple[str, ...] = ()
    confidence: Confidence
    significance: ConfidenceBand = ConfidenceBand.UNKNOWN
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    status: InsightStatus = InsightStatus.DRAFT
    is_human_authored_opinion: bool = False
    metadata: dict[str, str] = {}

    def check_invariants(self) -> None:
        if (
            self.status == InsightStatus.PUBLISHED
            and not self.is_human_authored_opinion
            and self.evidence_set_id is None
        ):
            raise InvariantViolation(
                "a published, non-opinion Insight must reference at least one EvidenceSet"
            )
