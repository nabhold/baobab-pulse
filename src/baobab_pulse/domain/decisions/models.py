"""Decision, Action, Outcome and Feedback — the human decision loop.

ARCH-PULSE-CIM-001 §68-77. INV-PULSE-009: Pulse distinguishes decision from
operational action — ``Action`` here only records Pulse's *knowledge* that
an external engine (MedusaJS, iDempiere, Payload CMS) or human process
executed something; Pulse never performs the mutation itself
(ADR-PULSE-001 §"Intelligence-to-Action Boundary").
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import CanonicalEntity, GovernedEntity


class DecisionType(StrEnum):
    """ARCH-PULSE-CIM-001 §70."""

    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    DEFER = "DEFER"
    REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
    CANCEL = "CANCEL"


class Decision(GovernedEntity):
    """Aggregate root. ``Recommendation 1 ─── * Decision``."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["decision"] = "decision"
    recommendation_id: str
    decision_type: DecisionType
    rationale: str | None = None
    decided_by: str
    decided_at: datetime
    authority_reference: str | None = None
    status: str = "RECORDED"
    metadata: dict[str, str] = {}


class Action(CanonicalEntity):
    """Subordinate to :class:`Decision`. Records intent and an external
    execution reference/status only — Pulse never performs the mutation."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["action"] = "action"
    decision_id: str
    intent: str
    external_engine: str | None = None
    """e.g. ``"medusajs"``, ``"idempiere"``, ``"payload_cms"``, ``"human"``."""
    external_execution_reference: str | None = None
    execution_status: str = "PENDING"


class Outcome(CanonicalEntity):
    """Subordinate to :class:`Decision` (``Decision 1 ─── * Outcome``)."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["outcome"] = "outcome"
    decision_id: str
    action_reference: str | None = None
    outcome_type: str | None = None
    description: str | None = None
    measured_value: float | None = None
    unit: str | None = None
    observed_at: datetime
    evidence_set_id: str | None = None
    metadata: dict[str, str] = {}


class FeedbackType(StrEnum):
    """ARCH-PULSE-CIM-001 §77."""

    ACCURACY = "ACCURACY"
    RELEVANCE = "RELEVANCE"
    TIMELINESS = "TIMELINESS"
    USEFULNESS = "USEFULNESS"
    CONFIDENCE_CALIBRATION = "CONFIDENCE_CALIBRATION"
    OUTCOME_SUCCESS = "OUTCOME_SUCCESS"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    FALSE_NEGATIVE = "FALSE_NEGATIVE"
    OTHER = "OTHER"


class Feedback(CanonicalEntity):
    """Append-only subordinate entity. Attaches to an Outcome, Recommendation,
    Insight, Signal, Forecast or ModelRun via ``target_reference``."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["feedback"] = "feedback"
    target_reference: str
    feedback_type: FeedbackType
    rating: float | None = None
    comment: str | None = None
    evidence_set_id: str | None = None
    submitted_by: str
    submitted_at: datetime
