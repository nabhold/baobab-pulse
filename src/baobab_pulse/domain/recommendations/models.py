"""Recommendation (ARCH-PULSE-CIM-001 §64-67).

INV-PULSE-008 / ADR-PULSE-002 §2.8: Recommendation and Decision are
mandatorily separate — "No ORM convenience shall merge the two." A
Recommendation SHALL NOT automatically become a Decision (that requires a
:class:`~baobab_pulse.domain.decisions.models.Decision` recorded by the
authorised decision authority). "Recommendation isolation" (ADR-PULSE-002):
it must not embed mutable copies of upstream intelligence — hence every
upstream link here is a :class:`Reference`, not an inline copy.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.value_objects import Confidence, Money


class AuthorityRequirement(StrEnum):
    """ARCH-PULSE-CIM-001 §67. Default for consequential actions is
    ``HUMAN_APPROVAL_REQUIRED`` — this mirrors ADR-PULSE-001's Automation
    Authority Levels ladder (OBSERVE -> ... -> APPROVE_BY_POLICY -> EXECUTE):
    a Recommendation never carries ``AUTOMATED`` authority on its own say-so."""

    INFORMATIONAL = "INFORMATIONAL"
    ADVISORY = "ADVISORY"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    POLICY_AUTOMATABLE = "POLICY_AUTOMATABLE"
    AUTOMATED = "AUTOMATED"


class RecommendationStatus(StrEnum):
    """ARCH-PULSE-CIM-001 §66."""

    DRAFT = "DRAFT"
    READY = "READY"
    PRESENTED = "PRESENTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    MODIFIED = "MODIFIED"
    DEFERRED = "DEFERRED"
    EXPIRED = "EXPIRED"
    WITHDRAWN = "WITHDRAWN"


class Recommendation(GovernedEntity):
    """Aggregate root. Frozen — a versioned aggregate (CIM §63)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["recommendation"] = "recommendation"
    title: str
    action: str
    rationale: str
    opportunity_references: tuple[str, ...] = ()
    risk_references: tuple[str, ...] = ()
    insight_references: tuple[str, ...] = ()
    evidence_set_id: str
    expected_benefit: Money | None = None
    expected_cost: Money | None = None
    urgency: str | None = None
    confidence: Confidence
    authority_requirement: AuthorityRequirement = AuthorityRequirement.HUMAN_APPROVAL_REQUIRED
    status: RecommendationStatus = RecommendationStatus.DRAFT
    metadata: dict[str, str] = {}
