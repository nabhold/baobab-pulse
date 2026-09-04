"""Risk (ARCH-PULSE-CIM-001 §57-60).

AGG-PULSE-009: kept separate from Opportunity. Invariant (ADR-PULSE-002
§2.2): ``likelihood``, ``impact`` and ``confidence`` MUST NOT collapse into
one unexplained numeric score.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.enums import ConfidenceBand
from baobab_pulse.domain.shared.value_objects import Confidence


class RiskType(StrEnum):
    """ARCH-PULSE-CIM-001 §59."""

    MARKET = "MARKET"
    FX = "FX"
    COUNTRY = "COUNTRY"
    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"
    WEATHER = "WEATHER"
    LOGISTICS = "LOGISTICS"
    REGULATORY = "REGULATORY"
    FINANCIAL = "FINANCIAL"
    OPERATIONAL = "OPERATIONAL"
    CYBER = "CYBER"
    REPUTATIONAL = "REPUTATIONAL"
    STRATEGIC = "STRATEGIC"
    OTHER = "OTHER"


class RiskStatus(StrEnum):
    """ARCH-PULSE-CIM-001 §60."""

    IDENTIFIED = "IDENTIFIED"
    ASSESSED = "ASSESSED"
    MONITORED = "MONITORED"
    MITIGATED = "MITIGATED"
    ACCEPTED = "ACCEPTED"
    MATERIALISED = "MATERIALISED"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"


class Risk(GovernedEntity):
    """Aggregate root, independent of :class:`~baobab_pulse.domain.opportunities.models.Opportunity`.

    ``likelihood``, ``impact`` and ``confidence`` are kept as three distinct
    ordinal dimensions rather than folded into a single ``severity`` number
    — a caller wanting one summary figure derives it explicitly and
    documents the method, it is never implicit here.
    """

    model_config = ConfigDict(extra="forbid")

    type: Literal["risk"] = "risk"
    title: str
    description: str | None = None
    risk_type: RiskType
    insight_references: tuple[str, ...] = ()
    evidence_set_id: str | None = None
    likelihood: ConfidenceBand = ConfidenceBand.UNKNOWN
    impact: ConfidenceBand = ConfidenceBand.UNKNOWN
    exposure: str | None = None
    time_horizon: str | None = None
    confidence: Confidence
    status: RiskStatus = RiskStatus.IDENTIFIED
    metadata: dict[str, str] = {}
