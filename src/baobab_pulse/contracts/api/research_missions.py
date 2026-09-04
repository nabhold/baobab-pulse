"""``/research-missions`` request/response schemas (item 60, 71)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from baobab_pulse.domain.research import ResearchMission, ResearchMissionStatus
from baobab_pulse.domain.shared.enums import Classification, ConfidenceBand, TenantScope
from baobab_pulse.domain.shared.value_objects import TenantContext


class CreateResearchMissionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    research_question: str
    tenant_id: str | None = None
    """Control-Plane-minted tenant id (``tn_...``). Required unless
    ``tenant_scope`` is ``GLOBAL``/``PLATFORM``."""
    tenant_scope: TenantScope = TenantScope.TENANT
    classification: Classification = Classification.TENANT
    confidence_requirement: ConfidenceBand = ConfidenceBand.MODERATE

    def to_tenant_context(self) -> TenantContext | None:
        return TenantContext(tenant_id=self.tenant_id) if self.tenant_id else None


class ResearchMissionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    research_question: str
    status: ResearchMissionStatus
    tenant_scope: TenantScope
    classification: Classification

    @classmethod
    def from_domain(cls, mission: ResearchMission) -> ResearchMissionResponse:
        return cls(
            id=mission.id,
            title=mission.title,
            research_question=mission.research_question,
            status=mission.status,
            tenant_scope=mission.tenant_scope,
            classification=mission.classification,
        )
