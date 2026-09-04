"""Opportunity (ARCH-PULSE-CIM-001 §53-56).

AGG-PULSE-009: Opportunity and Risk SHALL remain separate aggregates — never
a generic "Finding" (ADR-PULSE-002, rejected alternative). Invariant: SHALL
reference >= 1 supporting Insight or Analysis unless manually originated.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.enums import ConfidenceBand
from baobab_pulse.domain.shared.errors import InvariantViolation
from baobab_pulse.domain.shared.value_objects import Confidence, GeographicContext, MarketContext, Money


class OpportunityType(StrEnum):
    """ARCH-PULSE-CIM-001 §55."""

    MARKET_ENTRY = "MARKET_ENTRY"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    PRODUCT = "PRODUCT"
    PRICING = "PRICING"
    SUPPLY = "SUPPLY"
    PROCUREMENT = "PROCUREMENT"
    PARTNERSHIP = "PARTNERSHIP"
    INVESTMENT = "INVESTMENT"
    COST_REDUCTION = "COST_REDUCTION"
    CAPACITY = "CAPACITY"
    REGULATORY = "REGULATORY"
    STRATEGIC = "STRATEGIC"
    OTHER = "OTHER"


class OpportunityStatus(StrEnum):
    """ARCH-PULSE-CIM-001 §56."""

    DETECTED = "DETECTED"
    QUALIFIED = "QUALIFIED"
    ASSESSED = "ASSESSED"
    PROPOSED = "PROPOSED"
    ACTIONED = "ACTIONED"
    DISMISSED = "DISMISSED"
    EXPIRED = "EXPIRED"
    LOST = "LOST"
    SUPERSEDED = "SUPERSEDED"


class Opportunity(GovernedEntity):
    """Aggregate root, independent of :class:`~baobab_pulse.domain.risks.models.Risk`."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["opportunity"] = "opportunity"
    title: str
    description: str | None = None
    opportunity_type: OpportunityType
    insight_references: tuple[str, ...] = ()
    evidence_set_id: str | None = None
    market: MarketContext = MarketContext()
    geography: GeographicContext = GeographicContext()
    estimated_value: Money | None = None
    time_horizon: str | None = None
    confidence: Confidence
    urgency: ConfidenceBand = ConfidenceBand.UNKNOWN
    feasibility: ConfidenceBand = ConfidenceBand.UNKNOWN
    status: OpportunityStatus = OpportunityStatus.DETECTED
    manually_originated: bool = False
    metadata: dict[str, str] = {}

    def check_invariants(self) -> None:
        if not self.manually_originated and not self.insight_references:
            raise InvariantViolation(
                "a non-manually-originated Opportunity must reference at least one Insight"
            )
        # QUAL-PULSE-024 (ADR-PULSE-009 §191): an Opportunity SHALL NOT become
        # QUALIFIED merely because a narrative is persuasive — it requires a
        # methodology-defined evidence profile, i.e. an actual EvidenceSet.
        if self.status == OpportunityStatus.QUALIFIED and self.evidence_set_id is None:
            raise InvariantViolation(
                "an Opportunity cannot be QUALIFIED without a methodology-backed EvidenceSet"
            )
