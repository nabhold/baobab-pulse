"""ModelExecutionPort — provider-neutral model invocation (item 38).

    ModelExecutionPort -> HaystackGeneratorAdapter -> Provider Integration

Application/domain code asks for "run this ModelVersion against these
messages"; it never knows whether the eventual call is an
``OpenAIChatGenerator``, an ``AnthropicChatGenerator``, or a local model —
that choice is bound in ``infrastructure.haystack.generators`` from a
``baobab_pulse.domain.models.ModelVersion`` (PULSE-018: the domain model
registry is authoritative, a Haystack Generator instance never replaces it).
"""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, ConfigDict


class ModelMessage(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    role: str
    """``"system"``, ``"user"``, or ``"assistant"`` — provider-neutral."""
    content: str


class ModelExecutionRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    model_version_id: str
    messages: tuple[ModelMessage, ...]
    parameters: dict[str, float | int | str | bool] = {}


class ModelExecutionResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    text: str
    usage: dict[str, int] = {}
    model_run_reference: str | None = None
    finish_reason: str | None = None


class ModelExecutionPort(Protocol):
    async def generate(self, request: ModelExecutionRequest) -> ModelExecutionResult: ...
