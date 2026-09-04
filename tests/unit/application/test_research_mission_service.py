"""Unit tests for the validation boundary itself — no Haystack involved.

Uses a fake ``PipelinePort`` so this test is pure application-layer logic:
it proves ``ResearchMissionService`` drops ungrounded ``ClaimCandidate``s
and promotes grounded ones, independent of whatever produced the
candidates.
"""

from __future__ import annotations

from baobab_pulse.application.ports.pipeline_port import (
    ClaimCandidate,
    PipelineExecutionRequest,
    PipelineExecutionResult,
)
from baobab_pulse.application.services.research_mission_service import ResearchMissionService
from baobab_pulse.domain.evidence import Evidence, EvidenceSet
from baobab_pulse.domain.research import ClaimStatus, ResearchMission
from baobab_pulse.domain.shared.enums import Classification, EvidenceDirection, TenantScope
from baobab_pulse.domain.shared.value_objects import Reference, TenantContext


class FakePipelinePort:
    def __init__(self, candidates: tuple[ClaimCandidate, ...]) -> None:
        self._candidates = candidates

    async def run(self, request: PipelineExecutionRequest) -> PipelineExecutionResult:
        return PipelineExecutionResult(
            pipeline_name=request.pipeline_name,
            pipeline_version=request.pipeline_version,
            claim_candidates=self._candidates,
        )


def _mission_and_evidence() -> tuple[ResearchMission, EvidenceSet]:
    tenant_context = TenantContext(tenant_id="tn_test01")
    evidence_set = EvidenceSet(
        id="evs_1",
        purpose="test",
        entries=(
            Evidence(
                id="evd_known",
                referenced_object=Reference(object_type="observation", object_id="obs_1"),
                direction=EvidenceDirection.SUPPORTS,
            ),
        ),
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
    )
    mission = ResearchMission(
        id="rms_1",
        title="test mission",
        research_question="does the evidence support anything?",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
    )
    return mission, evidence_set


async def test_ungrounded_candidate_is_dropped() -> None:
    mission, evidence_set = _mission_and_evidence()
    candidate = ClaimCandidate(
        statement="an unsupported assertion",
        claim_type="INFERRED",
        supporting_evidence_ids=("evd_does_not_exist",),
    )
    service = ResearchMissionService(pipeline_port=FakePipelinePort((candidate,)))

    claims = await service.run_research_pipeline(
        mission, evidence_set, {}, pipeline_name="test", pipeline_version="1"
    )

    assert claims == []


async def test_grounded_candidate_is_promoted_to_a_claim() -> None:
    mission, evidence_set = _mission_and_evidence()
    candidate = ClaimCandidate(
        statement="a properly grounded assertion",
        claim_type="INFERRED",
        supporting_evidence_ids=("evd_known",),
    )
    service = ResearchMissionService(pipeline_port=FakePipelinePort((candidate,)))

    claims = await service.run_research_pipeline(
        mission, evidence_set, {}, pipeline_name="test", pipeline_version="1"
    )

    assert len(claims) == 1
    assert claims[0].status == ClaimStatus.EVIDENCED
    assert claims[0].statement == candidate.statement


async def test_candidate_with_no_cited_evidence_is_dropped() -> None:
    mission, evidence_set = _mission_and_evidence()
    candidate = ClaimCandidate(statement="an unattributed assertion", claim_type="INFERRED")
    service = ResearchMissionService(pipeline_port=FakePipelinePort((candidate,)))

    claims = await service.run_research_pipeline(
        mission, evidence_set, {}, pipeline_name="test", pipeline_version="1"
    )

    assert claims == []
