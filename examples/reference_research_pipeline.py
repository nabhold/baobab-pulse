"""Runnable demonstration of the reference research pipeline (item 112).

    Research Question -> Synthetic Evidence -> Haystack Pipeline
        -> Deterministic/Test Generator -> Structured Candidate
        -> Baobab Validation Adapter -> Result

This script proves the architecture end-to-end using synthetic, non-
sensitive evidence (item 111) and a deterministic ``MockChatGenerator`` —
it requires no database, no object storage, and no model-provider API key.
It is architectural verification, not a production research product
(item 112): a real research mission would plan sources, acquire evidence
through governed ``SourceAdapter``\\ s, and route through editorial review
before publication (ADR-PULSE-003).

Run with: `uv run python examples/reference_research_pipeline.py`
"""

from __future__ import annotations

import asyncio
import json

from haystack.components.generators.chat import MockChatGenerator

from baobab_pulse.application.services.research_mission_service import ResearchMissionService
from baobab_pulse.domain.evidence import Evidence, EvidenceSet
from baobab_pulse.domain.research import ResearchMission
from baobab_pulse.domain.shared.enums import Classification, ConfidenceBand, EvidenceDirection, TenantScope
from baobab_pulse.domain.shared.identifiers import new_id
from baobab_pulse.domain.shared.value_objects import Reference, TenantContext
from baobab_pulse.infrastructure.haystack.pipeline_adapter import HaystackPipelineAdapter
from baobab_pulse.infrastructure.haystack.pipelines.research_pipeline import PIPELINE_NAME, PIPELINE_VERSION


async def main() -> None:
    tenant_context = TenantContext(tenant_id="tn_example01")

    evidence_export_growth = new_id("evd")
    evidence_supply_shortage = new_id("evd")

    evidence_set = EvidenceSet(
        id=new_id("evs"),
        purpose="Uganda-South Africa coffee corridor opportunity screening",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
        entries=(
            Evidence(
                id=evidence_export_growth,
                referenced_object=Reference(object_type="observation", object_id="obs_uganda_exports_q2"),
                direction=EvidenceDirection.SUPPORTS,
                quality=ConfidenceBand.HIGH,
            ),
            Evidence(
                id=evidence_supply_shortage,
                referenced_object=Reference(object_type="observation", object_id="obs_za_import_shortage"),
                direction=EvidenceDirection.SUPPORTS,
                quality=ConfidenceBand.MODERATE,
            ),
        ),
    )
    evidence_text = {
        evidence_export_growth: "Ugandan coffee exports to South Africa rose 18% year-on-year in Q2 2026 (synthetic).",
        evidence_supply_shortage: "South African specialty coffee importers report supply shortages (synthetic).",
    }

    mission = ResearchMission(
        id=new_id("rms"),
        title="Uganda-South Africa coffee corridor",
        research_question="Is there a growing supply opportunity for Ugandan coffee into South Africa?",
        tenant_scope=TenantScope.TENANT,
        tenant_context=tenant_context,
        classification=Classification.TENANT,
    )

    # A deterministic, fixed model reply — no API key, no network call. A
    # production deployment would pass a real ChatGenerator here instead,
    # bound to a registered ModelVersion via
    # infrastructure.haystack.generators.model_execution_adapter.
    fixed_reply = json.dumps(
        [
            {
                "statement": "Rising Ugandan coffee exports align with reported South African supply "
                "shortages, suggesting a growing sourcing opportunity.",
                "claim_type": "INFERRED",
                "evidence_ids": [evidence_export_growth, evidence_supply_shortage],
                "limitations": ["Synthetic single-quarter data; not yet corroborated by trade statistics."],
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

    print(f"Research question: {mission.research_question}\n")
    print(f"Pipeline: {PIPELINE_NAME} v{PIPELINE_VERSION}\n")
    for claim in claims:
        print(f"Claim [{claim.status.value}]: {claim.statement}")
        print(f"  confidence: {claim.confidence.confidence_band.value} ({claim.confidence.confidence_method.value})")
        print(f"  limitations: {list(claim.limitations)}")


if __name__ == "__main__":
    asyncio.run(main())
