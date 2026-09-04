"""The reference research pipeline (item 112).

    Research Question
          |
          v
    Synthetic Evidence (Documents, built outside the pipeline from a
                         canonical EvidenceSet — see the pipeline adapter)
          |
          v
    Haystack Pipeline:  EvidenceContextComponent -> ChatGenerator -> ClaimGroundingComponent
          |
          v
    Deterministic/Test Generator (MockChatGenerator by default)
          |
          v
    Structured Candidate (ClaimCandidate, status=CANDIDATE)
          |
          v
    Baobab Validation Adapter (application.services.research_mission_service)
          |
          v
    Result (domain Claim)

Item 109: pipeline definitions are versioned. ``PIPELINE_VERSION`` is the
exact string a ``PipelineExecutionResult``/``ModelRun`` records — bump it
whenever this graph's structure or component configuration changes in a way
that could alter research behaviour, so a Haystack upgrade or a pipeline
edit is always traceable to a specific, reproducible definition (item 110).

This is architectural verification, not a production research product
(item 112) — it proves evidence flows through Haystack and back out as a
structured, grounded candidate without Haystack ever becoming the canonical
model.
"""

from __future__ import annotations

from typing import Any

from haystack import Pipeline
from haystack.components.generators.chat import MockChatGenerator

from baobab_pulse.infrastructure.haystack.components.claim_grounding_component import ClaimGroundingComponent
from baobab_pulse.infrastructure.haystack.components.evidence_context_component import (
    EvidenceContextComponent,
)

PIPELINE_NAME = "pulse.research.reference"
PIPELINE_VERSION = "1"


def build_research_pipeline(chat_generator: Any | None = None) -> Pipeline:
    """Build the reference research pipeline.

    ``chat_generator=None`` (the default) wires in a deterministic
    ``MockChatGenerator`` so this pipeline — and every test that exercises
    it — never requires a paid model-provider API key (item 96-97). A real
    deployment passes a Generator selected via
    ``infrastructure.haystack.generators.model_execution_adapter`` from a
    registered ``ModelVersion``.
    """
    generator = chat_generator if chat_generator is not None else MockChatGenerator()

    pipeline = Pipeline()
    pipeline.add_component("evidence_context", EvidenceContextComponent())
    pipeline.add_component("generator", generator)
    pipeline.add_component("claim_grounding", ClaimGroundingComponent())

    pipeline.connect("evidence_context.messages", "generator.messages")
    pipeline.connect("generator.replies", "claim_grounding.replies")
    return pipeline
