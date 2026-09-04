"""Model, ModelVersion and ModelRun — the Pulse model registry.

ARCH-PULSE-CIM-001 §109-113. PULSE-018: material models SHALL be registered
and versioned. AGG-PULSE-011: ModelVersion and method identity SHALL be
immutable for historical analyses. A Haystack ``Generator``/``ChatGenerator``
instance is an *infrastructure* detail bound to a ModelVersion through
``infrastructure.haystack.generators`` — it never replaces this registry
(item 39 of the platform brief).
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import CanonicalEntity


class ModelLifecycle(StrEnum):
    """ARCH-PULSE-CIM-001 §112."""

    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


class Model(CanonicalEntity):
    """Aggregate root."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["model"] = "model"
    name: str
    purpose: str
    governance_state: ModelLifecycle = ModelLifecycle.DRAFT
    metadata: dict[str, str] = {}


class ModelVersion(CanonicalEntity):
    """Belongs to exactly one :class:`Model`; immutable once approved or
    used in a consequential analysis (AGG-PULSE-011)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["model_version"] = "model_version"
    model_id: str
    version: str
    provider: str
    """Provider-neutral label, e.g. ``"openai"``, ``"anthropic"``, ``"local"``
    — never a Haystack class name (item 37/38 of the platform brief)."""
    algorithm: str | None = None
    configuration: dict[str, Any] = {}
    training_reference: str | None = None
    release_date: datetime | None = None
    status: ModelLifecycle = ModelLifecycle.DRAFT


class ModelRun(CanonicalEntity):
    """Independently persisted/scalable; associated with exactly one
    :class:`ModelVersion`."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["model_run"] = "model_run"
    model_version_id: str
    input_reference: str | None = None
    parameters: dict[str, Any] = {}
    started_at: datetime
    completed_at: datetime | None = None
    result_reference: str | None = None
    status: str = "PENDING"
    cost: float | None = None
    usage: dict[str, int] = {}
