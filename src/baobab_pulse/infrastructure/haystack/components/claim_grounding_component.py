"""ClaimGroundingComponent — parses model output into structured candidates.

This is *not* the validation boundary itself (item 42-43): it only performs
the mechanical translation from a chat reply's text into
``ClaimCandidate`` DTOs, all carrying ``status="CANDIDATE"``. The actual
grounding check (do the cited evidence ids really exist in the EvidenceSet?)
happens in ``application.services.research_mission_service`` — a Haystack
component is never the place a claim is authorised to leave CANDIDATE
status, since a component has no view of the canonical EvidenceSet the
pipeline was authorised against.

Fails closed: a reply that is not valid, well-shaped JSON produces zero
candidates rather than a fabricated one (item 42: prefer structured output
that a schema failure can reject over unvalidated free-form prose).
"""

from __future__ import annotations

import json
import logging
from typing import Any

from haystack import component
from haystack.dataclasses import ChatMessage

from baobab_pulse.application.ports.pipeline_port import ClaimCandidate

logger = logging.getLogger(__name__)

_VALID_CLAIM_TYPES = {"FACTUAL", "ESTIMATED", "INFERRED", "FORECAST", "HYPOTHESIS"}


@component
class ClaimGroundingComponent:
    @component.output_types(claim_candidates=list[ClaimCandidate])
    def run(self, replies: list[ChatMessage]) -> dict[str, list[ClaimCandidate]]:
        if not replies or replies[0].text is None:
            return {"claim_candidates": []}

        try:
            parsed: Any = json.loads(replies[0].text)
        except json.JSONDecodeError:
            logger.warning("claim grounding: model reply was not valid JSON; producing zero candidates")
            return {"claim_candidates": []}

        if not isinstance(parsed, list):
            return {"claim_candidates": []}

        candidates: list[ClaimCandidate] = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            claim_type = str(item.get("claim_type", "")).upper()
            if claim_type not in _VALID_CLAIM_TYPES:
                claim_type = "INFERRED"
            statement = item.get("statement")
            if not statement:
                continue
            candidates.append(
                ClaimCandidate(
                    statement=str(statement),
                    claim_type=claim_type,
                    supporting_evidence_ids=tuple(str(e) for e in item.get("evidence_ids", [])),
                    limitations=tuple(str(x) for x in item.get("limitations", [])),
                )
            )
        return {"claim_candidates": candidates}
