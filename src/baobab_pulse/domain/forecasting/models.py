"""Forecast and ForecastEvaluation (ARCH-PULSE-CIM-001 §61-63).

``ForecastEvaluation`` is subordinate: ``Forecast 1 ─── 0..* ForecastEvaluation``
(ADR-PULSE-002 §2.2), produced once an actual Observation for the target
becomes available, enabling ``error``/``bias``/``accuracy``/``calibration``.
A Forecast SHALL NOT be confused with a Scenario (ADR-PULSE-002).
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import CanonicalEntity, GovernedEntity
from baobab_pulse.domain.shared.value_objects import Confidence, Reference


class Forecast(GovernedEntity):
    """Aggregate root. Frozen — a versioned aggregate (CIM §63)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["forecast"] = "forecast"
    target_reference: Reference
    target_metric: str
    forecast_origin: datetime
    target_time: datetime
    horizon: str
    predicted_value: float
    lower_bound: float | None = None
    upper_bound: float | None = None
    confidence: Confidence
    model_version_id: str | None = None
    evidence_set_id: str | None = None
    generated_at: datetime
    metadata: dict[str, str] = {}


class ForecastEvaluation(CanonicalEntity):
    """Subordinate entity: compares a :class:`Forecast` against the actual
    Observation once it materialises."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["forecast_evaluation"] = "forecast_evaluation"
    forecast_id: str
    actual_observation_id: str
    error: float | None = None
    bias: float | None = None
    accuracy: float | None = None
    calibration: float | None = None
    evaluated_at: datetime
