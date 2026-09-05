"""``/evidence/search`` — the semantic-retrieval slice of the API boundary
(Qdrant refactor item 42, 105).

Requires a bound tenant context (``api.middleware.TenancyMiddleware`` binds
one from the ``X-Baobab-Tenant-Id`` header) — a request with no tenant
context fails closed with 400 ``TENANT_CONTEXT_MISSING``, never an
unrestricted Qdrant query (item 44).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from baobab_pulse.api.dependencies import get_evidence_retrieval_service
from baobab_pulse.application.services.evidence_retrieval_service import EvidenceRetrievalService
from baobab_pulse.contracts.api.evidence import (
    EvidenceCandidateResponse,
    EvidenceSearchRequest,
    EvidenceSearchResponse,
)

router = APIRouter(prefix="/evidence", tags=["evidence"])


@router.post("/search")
async def search_evidence(
    request: EvidenceSearchRequest,
    service: EvidenceRetrievalService = Depends(get_evidence_retrieval_service),
) -> EvidenceSearchResponse:
    candidates = await service.search(
        request.query_text,
        requester_clearance=request.requester_clearance,
        evidence_set_id=request.evidence_set_id,
        top_k=request.top_k,
    )
    return EvidenceSearchResponse(
        candidates=tuple(EvidenceCandidateResponse(**candidate.model_dump()) for candidate in candidates)
    )
