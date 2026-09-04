"""Signal — a detected phenomenon (ARCH-PULSE-CIM-001 §38-43).

ADR-PULSE-002 §2.8: "Signal ≠ Insight subtype... Signal = detected
phenomenon; Insight = interpreted significance." ``Trend`` and ``Anomaly``
are Signal *specialisations* via ``signal_type``, not separate classes
(ADR-PULSE-002 §2.2: "implementation SHOULD favour Signal + signal_type +
specialised attributes over ORM inheritance").
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity
from baobab_pulse.domain.shared.value_objects import Confidence, Reference


class SignalType(StrEnum):
    """ARCH-PULSE-CIM-001 §40."""

    THRESHOLD = "THRESHOLD"
    CHANGE = "CHANGE"
    TREND = "TREND"
    ANOMALY = "ANOMALY"
    CORRELATION = "CORRELATION"
    EVENT = "EVENT"
    DIVERGENCE = "DIVERGENCE"
    CONVERGENCE = "CONVERGENCE"
    RISK_INDICATOR = "RISK_INDICATOR"
    OPPORTUNITY_INDICATOR = "OPPORTUNITY_INDICATOR"


class TrendDirection(StrEnum):
    """ARCH-PULSE-CIM-001 §41 (only meaningful when ``signal_type ==
    SignalType.TREND``)."""

    UPWARD = "UPWARD"
    DOWNWARD = "DOWNWARD"
    STABLE = "STABLE"
    ACCELERATING = "ACCELERATING"
    DECELERATING = "DECELERATING"
    CYCLICAL = "CYCLICAL"


class SignalStatus(StrEnum):
    """ARCH-PULSE-CIM-001 §43."""

    DETECTED = "DETECTED"
    ACTIVE = "ACTIVE"
    CONFIRMED = "CONFIRMED"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"


class Signal(GovernedEntity):
    """Aggregate root."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["signal"] = "signal"
    signal_type: SignalType
    subject_reference: Reference
    evidence_set_id: str
    detection_method: str
    detection_version: str
    severity: str | None = None
    confidence: Confidence
    trend_direction: TrendDirection | None = None
    """Populated only when ``signal_type == SignalType.TREND``; an Anomaly
    (``signal_type == SignalType.ANOMALY``) is "not automatically a risk"
    (CIM §42) and carries no direction of its own."""
    first_detected_at: datetime
    last_detected_at: datetime
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    status: SignalStatus = SignalStatus.DETECTED
    metadata: dict[str, str] = {}
