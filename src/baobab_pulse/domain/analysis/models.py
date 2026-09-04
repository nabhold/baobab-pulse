"""Analysis — a domain analytical act (ARCH-PULSE-CIM-001 §44-47).

ADR-PULSE-002 §2.2: "``Analysis`` and ``IntelligenceJob`` are NOT
synonymous (Job = orchestration; Analysis = domain analytical act)." An
Analysis MAY be produced by a deterministic rule, a statistical method, or a
Haystack-orchestrated LLM pipeline (``analysis_type == LLM_ASSISTED``) — the
domain object itself never knows or cares which.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import GovernedEntity


class AnalysisType(StrEnum):
    """ARCH-PULSE-CIM-001 §46."""

    DESCRIPTIVE = "DESCRIPTIVE"
    DIAGNOSTIC = "DIAGNOSTIC"
    COMPARATIVE = "COMPARATIVE"
    STATISTICAL = "STATISTICAL"
    FORECAST = "FORECAST"
    SCENARIO = "SCENARIO"
    GEOSPATIAL = "GEOSPATIAL"
    SEMANTIC = "SEMANTIC"
    RULE_BASED = "RULE_BASED"
    ML = "ML"
    LLM_ASSISTED = "LLM_ASSISTED"
    HYBRID = "HYBRID"


class AnalysisStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class Analysis(GovernedEntity):
    """Aggregate root."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["analysis"] = "analysis"
    analysis_type: AnalysisType
    method: str
    method_version: str
    evidence_set_id: str
    parameters: dict[str, Any] = {}
    model_version_id: str | None = None
    started_at: datetime
    completed_at: datetime | None = None
    status: AnalysisStatus = AnalysisStatus.PENDING
    result_reference: str | None = None
    reproducibility_profile: dict[str, str] = {}
    metadata: dict[str, str] = {}
