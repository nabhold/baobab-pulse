"""ResearchMissionService — the reference application service.

This is the concrete implementation of the platform brief's central pipeline
diagram::

    ResearchMission
          |
          v
    Baobab Application Service      <- this class
          |
          v
    Pipeline Port
          |
          v
    HaystackPipelineAdapter
          |
          v
    Haystack Pipeline
          |
          v
    Baobab Validation Boundary       <- _ground_candidate() below
          |
          v
    Canonical Domain Objects (Claim)

It exists to prove the architecture end-to-end (item 112: "the purpose is
architectural verification. It is NOT the first production research
product") — real research missions will need source planning, multi-round
evidence acquisition, and editorial review (ADR-PULSE-003) that this
reference implementation deliberately does not attempt.

The validation boundary is not a formality: QUAL-PULSE-022 ("citation
presence SHALL not substitute for citation support") means a
``ClaimCandidate`` is only promoted to a domain ``Claim`` if every evidence
id it cites is structurally present in the ``EvidenceSet`` it was given —
never because the model asserted it was grounded.
"""

from __future__ import annotations

from baobab_pulse.application.ports.pipeline_port import (
    ClaimCandidate,
    PipelineExecutionRequest,
    PipelinePort,
)
from baobab_pulse.application.services.confidence_service import ConfidenceService
from baobab_pulse.domain.evidence import EvidenceSet
from baobab_pulse.domain.research import Claim, ClaimStatus, ClaimType, ResearchMission
from baobab_pulse.domain.shared.enums import ConfidenceBand
from baobab_pulse.domain.shared.identifiers import new_id
from baobab_pulse.domain.shared.value_objects import QualityProfile, TenantContext

_BAND_ORDER = (
    ConfidenceBand.UNKNOWN,
    ConfidenceBand.VERY_LOW,
    ConfidenceBand.LOW,
    ConfidenceBand.MODERATE,
    ConfidenceBand.HIGH,
    ConfidenceBand.VERY_HIGH,
)

_CLAIM_TYPE_MAP = {
    "FACTUAL": ClaimType.FACTUAL,
    "ESTIMATED": ClaimType.ESTIMATED,
    "INFERRED": ClaimType.INFERRED,
    "FORECAST": ClaimType.FORECAST,
    "HYPOTHESIS": ClaimType.HYPOTHESIS,
}


class ResearchMissionService:
    def __init__(self, pipeline_port: PipelinePort, confidence_service: ConfidenceService | None = None) -> None:
        self._pipeline = pipeline_port
        self._confidence = confidence_service or ConfidenceService()

    async def run_research_pipeline(
        self,
        mission: ResearchMission,
        evidence_set: EvidenceSet,
        evidence_text: dict[str, str],
        *,
        pipeline_name: str,
        pipeline_version: str,
    ) -> list[Claim]:
        """Run one pipeline pass over ``evidence_set`` and return the
        resulting, *validated* domain Claims. Ungrounded candidates are
        dropped, not silently promoted — see :meth:`_ground_candidate`."""
        mission.check_tenant_context()
        request = PipelineExecutionRequest(
            pipeline_name=pipeline_name,
            pipeline_version=pipeline_version,
            research_question=mission.research_question,
            evidence_set=evidence_set,
            evidence_text=evidence_text,
            tenant_context=mission.tenant_context or TenantContext(tenant_id="tn_platform"),
        )
        result = await self._pipeline.run(request)

        claims: list[Claim] = []
        for candidate in result.claim_candidates:
            claim = self._ground_candidate(candidate, mission=mission, evidence_set=evidence_set)
            if claim is not None:
                claims.append(claim)
        return claims

    def _ground_candidate(
        self, candidate: ClaimCandidate, *, mission: ResearchMission, evidence_set: EvidenceSet
    ) -> Claim | None:
        known_evidence_ids = {entry.id for entry in evidence_set.entries}
        cited_ids = set(candidate.supporting_evidence_ids)
        if not cited_ids or not cited_ids.issubset(known_evidence_ids):
            # Not an exception in the batch path: one ungrounded candidate
            # should not fail an entire pipeline run. Callers that need to
            # know *why* a candidate was dropped should inspect the pipeline
            # trace (result.trace_reference), not this return value.
            return None

        matched = [e for e in evidence_set.entries if e.id in cited_ids]
        quality = QualityProfile(
            corroboration=self._corroboration_band(len(cited_ids)),
            consistency=min((e.quality for e in matched), key=_BAND_ORDER.index),
        )
        confidence = self._confidence.compose(
            quality,
            independent_corroborating_sources=len(cited_ids),
            has_unresolved_contradiction=False,
        )

        return Claim(
            id=new_id("clm"),
            research_mission_id=mission.id,
            statement=candidate.statement,
            claim_type=_CLAIM_TYPE_MAP.get(candidate.claim_type.upper(), ClaimType.INFERRED),
            evidence_set_id=evidence_set.id,
            confidence=confidence,
            limitations=candidate.limitations,
            status=ClaimStatus.EVIDENCED,
            tenant_scope=mission.tenant_scope,
            classification=mission.classification,
        )

    @staticmethod
    def _corroboration_band(source_count: int) -> ConfidenceBand:
        if source_count >= 3:
            return ConfidenceBand.HIGH
        if source_count == 2:
            return ConfidenceBand.MODERATE
        return ConfidenceBand.LOW
