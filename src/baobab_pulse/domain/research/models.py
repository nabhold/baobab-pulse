"""ResearchMission and Claim — the structured research workflow.

These two are not among ADR-PULSE-002 §2.1's fifteen canonical aggregate
roots (that ADR governs the evidence-to-decision chain); they belong to the
research/acquisition bounded context defined by ADR-PULSE-003 (§8-12,
§71-72) and are included here because item 71 of the governing platform
brief requires ``ResearchMission`` to be "a first-class Baobab concept... not
represented merely as a Haystack prompt or an Agent message." A future ADR
splitting research/evidence bounded-context ownership more formally should
treat this file, not ADR-PULSE-002, as authoritative for these two shapes.

PULSE-010 / req. 43: AI-generated output is not evidence merely because an
AI generated it, and SHALL initially carry ``ClaimStatus.CANDIDATE`` until an
explicit Pulse validation step accepts it — see
``application.services.research_mission_service`` and
``infrastructure.haystack.components.claim_grounding_component``, which is
the only place a Claim is allowed to leave ``CANDIDATE``.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.enums import ConfidenceBand
from baobab_pulse.domain.shared.value_objects import Confidence, ValueObject


class ResearchMissionStatus(StrEnum):
    """ADR-PULSE-003 §10."""

    PROPOSED = "PROPOSED"
    SCOPED = "SCOPED"
    SOURCE_PLANNED = "SOURCE_PLANNED"
    ACQUIRING = "ACQUIRING"
    ANALYSING = "ANALYSING"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    SUPERSEDED = "SUPERSEDED"


class EvidencePlan(ValueObject):
    """ADR-PULSE-003 §12."""

    mandatory_domains: tuple[str, ...] = ()
    desirable_domains: tuple[str, ...] = ()
    minimum_independent_sources: int = 1
    required_time_coverage: str | None = None
    geography_coverage: tuple[str, ...] = ()
    freshness_requirement: str | None = None
    source_authority_requirement: str | None = None
    contradiction_policy: str | None = None
    missing_evidence_policy: str | None = None


class ResearchMission(GovernedEntity):
    """Aggregate root of the research bounded context. Mutable while
    in-flight (status advances through its lifecycle in place); frozen once
    ``status == PUBLISHED`` — enforced by
    ``application.services.research_mission_service``, not by the model
    itself, since the service is what owns the state transition.
    """

    model_config = ConfigDict(extra="forbid")

    type: Literal["research_mission"] = "research_mission"
    title: str
    research_question: str
    client_scope: str | None = None
    geography_scope: tuple[str, ...] = ()
    market_scope: tuple[str, ...] = ()
    sector_scope: tuple[str, ...] = ()
    commodity_scope: tuple[str, ...] = ()
    time_horizon: str | None = None
    decision_context: str | None = None
    evidence_requirements: EvidencePlan = EvidencePlan()
    confidence_requirement: ConfidenceBand = ConfidenceBand.MODERATE
    deadline: datetime | None = None
    publication_profile: str | None = None
    status: ResearchMissionStatus = ResearchMissionStatus.PROPOSED


class ClaimType(StrEnum):
    """Pulse's own derivation from ADR-PULSE-009 §163's claim-strength
    vocabulary, narrowed to the subset relevant to a single Claim's nature
    rather than its evidentiary strength (which lives on ``confidence``)."""

    FACTUAL = "FACTUAL"
    ESTIMATED = "ESTIMATED"
    INFERRED = "INFERRED"
    FORECAST = "FORECAST"
    HYPOTHESIS = "HYPOTHESIS"


class ClaimStatus(StrEnum):
    """ADR-PULSE-003 §72, prefixed with ``CANDIDATE`` per req. 43 (PULSE-010):
    every AI-generated Claim starts here and is never treated as evidence
    until it has passed grounding validation into ``DRAFT`` or later."""

    CANDIDATE = "CANDIDATE"
    DRAFT = "DRAFT"
    EVIDENCED = "EVIDENCED"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    RETRACTED = "RETRACTED"
    SUPERSEDED = "SUPERSEDED"


class Claim(GovernedEntity):
    """ADR-PULSE-003 §71. A structured, evidence-attributable statement —
    the canonical shape any Haystack-generated research output is validated
    against before it may become Pulse intelligence (Insight/Analysis)."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["claim"] = "claim"
    research_mission_id: str | None = None
    statement: str
    claim_type: ClaimType
    evidence_set_id: str | None = None
    analysis_reference: str | None = None
    confidence: Confidence | None = None
    temporal_scope: str | None = None
    geographic_scope: str | None = None
    limitations: tuple[str, ...] = ()
    status: ClaimStatus = ClaimStatus.CANDIDATE
    publication_reference: str | None = None
