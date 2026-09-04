"""The Intelligence Execution Port — Pulse's one seam onto Haystack.

This is the concrete shape of the "Haystack Integration Boundary" in the
platform brief's final diagram::

    ResearchMission -> Application Service -> PipelinePort
        -> HaystackPipelineAdapter -> Haystack Pipeline

Nothing in ``baobab_pulse.application`` or ``baobab_pulse.domain`` imports
Haystack. ``PipelinePort`` is the only thing an application service knows
about "running a pipeline" — the adapter in
``baobab_pulse.infrastructure.haystack.pipeline_adapter`` is the only class
in the whole codebase allowed to import ``haystack``.

Everything crossing this port is a plain, framework-agnostic type. In
particular, ``ClaimCandidate`` is *not* the domain ``Claim`` — it is
unvalidated model output and always carries ``status="CANDIDATE"``
(PULSE-010, req. 43). It only becomes a domain ``Claim`` after
``application.services.research_mission_service`` runs it through grounding
validation.
"""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict

from baobab_pulse.domain.evidence import EvidenceSet
from baobab_pulse.domain.shared.value_objects import TenantContext


class ClaimCandidate(BaseModel):
    """Unvalidated, structured output of a research pipeline run. Never
    treated as evidence (PULSE-010) and never exposed to a caller under the
    name ``Claim`` until grounding validation promotes it."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    statement: str
    claim_type: str
    supporting_evidence_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    status: str = "CANDIDATE"


class PipelineExecutionRequest(BaseModel):
    """Everything a research pipeline run needs, expressed in Pulse's own
    vocabulary — never a Haystack type."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    pipeline_name: str
    pipeline_version: str
    research_question: str
    evidence_set: EvidenceSet
    evidence_text: dict[str, str] = {}
    """Resolved snippet text keyed by ``Evidence.id``. Evidence itself only
    references other canonical objects (item 27), so the caller resolves the
    actual text (from an Observation, SourceDocument, etc.) before crossing
    this port. A future ADR may replace this inline map with a dedicated
    text-resolution port once evidence volume makes eager resolution
    impractical — out of scope for this reference implementation."""
    tenant_context: TenantContext
    parameters: dict[str, Any] = {}


class PipelineExecutionResult(BaseModel):
    """Everything a caller needs to record provenance for a pipeline run,
    without knowing anything about how it was produced."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    pipeline_name: str
    pipeline_version: str
    model_run_reference: str | None = None
    claim_candidates: tuple[ClaimCandidate, ...] = ()
    trace_reference: str | None = None


class PipelinePort(Protocol):
    """Implemented by exactly one class in this codebase:
    ``infrastructure.haystack.pipeline_adapter.HaystackPipelineAdapter``."""

    async def run(self, request: PipelineExecutionRequest) -> PipelineExecutionResult: ...
