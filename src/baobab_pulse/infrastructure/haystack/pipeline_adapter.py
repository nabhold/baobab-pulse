"""HaystackPipelineAdapter — the one class implementing ``PipelinePort``.

    Baobab Application Service -> Pipeline Port -> HaystackPipelineAdapter -> Haystack Pipeline

Everything this class receives and returns is a plain
``application.ports.pipeline_port`` type. It is the translation point where
a canonical ``EvidenceSet`` becomes Haystack ``Document``\\ s and a Haystack
reply becomes ``ClaimCandidate``\\ s — see
``infrastructure.haystack.document_stores.in_memory_projection`` and
``infrastructure.haystack.components.claim_grounding_component`` for the two
halves of that translation.
"""

from __future__ import annotations

from typing import Any

from baobab_pulse.application.ports.pipeline_port import (
    PipelineExecutionRequest,
    PipelineExecutionResult,
)
from baobab_pulse.domain.shared.identifiers import new_id
from baobab_pulse.infrastructure.haystack.document_stores.in_memory_projection import build_documents
from baobab_pulse.infrastructure.haystack.errors import translate_exceptions
from baobab_pulse.infrastructure.haystack.pipelines.research_pipeline import (
    PIPELINE_NAME,
    PIPELINE_VERSION,
    build_research_pipeline,
)


class HaystackPipelineAdapter:
    """Implements ``application.ports.pipeline_port.PipelinePort``.

    ``chat_generator`` defaults to ``None``, which
    ``build_research_pipeline`` resolves to a deterministic
    ``MockChatGenerator`` — see that function's docstring for why that
    keeps this adapter usable in the core test suite without a model
    provider API key.
    """

    def __init__(self, chat_generator: Any | None = None) -> None:
        self._pipeline = build_research_pipeline(chat_generator)

    async def run(self, request: PipelineExecutionRequest) -> PipelineExecutionResult:
        return self._run(request)

    @translate_exceptions("Haystack research pipeline execution")
    def _run(self, request: PipelineExecutionRequest) -> PipelineExecutionResult:
        documents = build_documents(
            request.evidence_set,
            request.evidence_text,
        )
        outputs = self._pipeline.run(
            {"evidence_context": {"research_question": request.research_question, "documents": documents}}
        )
        candidates = outputs.get("claim_grounding", {}).get("claim_candidates", [])
        return PipelineExecutionResult(
            pipeline_name=request.pipeline_name or PIPELINE_NAME,
            pipeline_version=request.pipeline_version or PIPELINE_VERSION,
            model_run_reference=new_id("mrun"),
            claim_candidates=tuple(candidates),
        )
