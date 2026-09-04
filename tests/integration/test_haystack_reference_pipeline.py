"""End-to-end proof of the reference research pipeline (item 95, 112).

Deterministic and credential-free: ``MockChatGenerator`` returns a fixed
reply, so this test never calls a real model provider (item 96) — it
exercises the real ``haystack.Pipeline``, the real
``EvidenceContextComponent``/``ClaimGroundingComponent``, and the real
``HaystackPipelineAdapter``, proving:

* a Haystack pipeline actually executes (architecture test #9);
* its structured result crosses the anti-corruption boundary as a plain
  ``ClaimCandidate``, never a ``haystack.*`` type (architecture test #4);
* the Baobab validation boundary (``ResearchMissionService``) turns a
  grounded candidate into a canonical domain ``Claim`` (architecture
  test #10's "reproducibly from documented inputs" companion: the same
  fixed input always produces the same claim).
"""

from __future__ import annotations

import json

from haystack.components.generators.chat import MockChatGenerator

from baobab_pulse.application.services.research_mission_service import ResearchMissionService
from baobab_pulse.domain.evidence import Evidence, EvidenceSet
from baobab_pulse.domain.research import ClaimStatus, ResearchMission
from baobab_pulse.domain.shared.enums import Classification, ConfidenceBand, EvidenceDirection, TenantScope
from baobab_pulse.domain.shared.identifiers import new_id
from baobab_pulse.domain.shared.value_objects import Reference, TenantContext
from baobab_pulse.infrastructure.haystack.pipeline_adapter import HaystackPipelineAdapter
from baobab_pulse.infrastructure.haystack.pipelines.research_pipeline import PIPELINE_NAME, PIPELINE_VERSION


async def test_reference_pipeline_produces_a_grounded_claim() -> None:
    tenant_context = TenantContext(tenant_id="tn_test01")
    evidence_a, evidence_b = new_id("evd"), new_id("evd")

    evidence_set = EvidenceSet(
        id=new_id("evs"),
        purpose="opportunity research",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
        entries=(
            Evidence(
                id=evidence_a,
                referenced_object=Reference(object_type="observation", object_id="obs_exports"),
                direction=EvidenceDirection.SUPPORTS,
                quality=ConfidenceBand.HIGH,
            ),
            Evidence(
                id=evidence_b,
                referenced_object=Reference(object_type="observation", object_id="obs_shortage"),
                direction=EvidenceDirection.SUPPORTS,
                quality=ConfidenceBand.MODERATE,
            ),
        ),
    )
    evidence_text = {
        evidence_a: "Ugandan coffee exports to South Africa rose 18% year-on-year in Q2.",
        evidence_b: "South African specialty coffee importers report supply shortages.",
    }
    mission = ResearchMission(
        id=new_id("rms"),
        title="Uganda-South Africa coffee corridor",
        research_question="Is there a growing supply opportunity for Ugandan coffee into South Africa?",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
    )

    fixed_reply = json.dumps(
        [
            {
                "statement": "Rising Ugandan coffee exports align with South African supply shortages.",
                "claim_type": "INFERRED",
                "evidence_ids": [evidence_a, evidence_b],
                "limitations": ["Single-quarter data; not yet corroborated by trade statistics."],
            }
        ]
    )
    adapter = HaystackPipelineAdapter(chat_generator=MockChatGenerator(responses=fixed_reply))
    service = ResearchMissionService(pipeline_port=adapter)

    claims = await service.run_research_pipeline(
        mission,
        evidence_set,
        evidence_text,
        pipeline_name=PIPELINE_NAME,
        pipeline_version=PIPELINE_VERSION,
    )

    assert len(claims) == 1
    claim = claims[0]
    assert claim.status == ClaimStatus.EVIDENCED
    assert claim.research_mission_id == mission.id
    assert claim.evidence_set_id == evidence_set.id
    assert "South African supply shortages" in claim.statement


async def test_reference_pipeline_drops_an_ungrounded_reply() -> None:
    tenant_context = TenantContext(tenant_id="tn_test01")
    evidence_set = EvidenceSet(
        id=new_id("evs"),
        purpose="opportunity research",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
        entries=(
            Evidence(
                id=new_id("evd"),
                referenced_object=Reference(object_type="observation", object_id="obs_1"),
                direction=EvidenceDirection.SUPPORTS,
            ),
        ),
    )
    mission = ResearchMission(
        id=new_id("rms"),
        title="test",
        research_question="anything interesting here?",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
    )
    # The model hallucinates a citation to evidence that was never provided.
    fixed_reply = json.dumps(
        [{"statement": "an ungrounded claim", "claim_type": "INFERRED", "evidence_ids": ["evd_made_up"]}]
    )
    adapter = HaystackPipelineAdapter(chat_generator=MockChatGenerator(responses=fixed_reply))
    service = ResearchMissionService(pipeline_port=adapter)

    claims = await service.run_research_pipeline(
        mission, evidence_set, {}, pipeline_name=PIPELINE_NAME, pipeline_version=PIPELINE_VERSION
    )

    assert claims == []
