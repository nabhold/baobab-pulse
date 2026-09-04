"""IntelligenceProduct — a reusable, productised intelligence output.

ARCH-PULSE-CIM-001 §116-119. Examples (ARCH-PULSE-001 §60): Market Pulse,
Commodity Pulse, FX Pulse, Trade Corridor Pulse, Country Pulse, Supplier
Risk Pulse, Regulatory Pulse, Opportunity Radar, Executive Brief. The
platform is deliberately not hard-coded around any single product type
(item 73 of the platform brief) — ``product_type`` and ``configuration``
are how a new product is added without an engine redesign.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import CanonicalEntity, GovernedEntity


class IntelligenceProduct(GovernedEntity):
    """Aggregate root. Frozen — a versioned aggregate (CIM §63)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["intelligence_product"] = "intelligence_product"
    name: str
    product_type: str
    scope: str | None = None
    configuration: dict[str, Any] = {}
    schedule: str | None = None
    output_profile: dict[str, Any] = {}
    audience: str | None = None
    status: str = "DRAFT"


class IntelligenceProductRun(CanonicalEntity):
    """``IntelligenceProduct 1 ─── * IntelligenceProductRun``."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["intelligence_product_run"] = "intelligence_product_run"
    product_id: str
    product_version: str
    input_references: tuple[str, ...] = ()
    output_references: tuple[str, ...] = ()
    job_id: str | None = None
    run_at: datetime
    status: str = "PENDING"
