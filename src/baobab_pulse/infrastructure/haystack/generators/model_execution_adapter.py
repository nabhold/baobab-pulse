"""HaystackModelExecutionAdapter — implements ``ModelExecutionPort``.

    ModelExecutionPort -> HaystackModelExecutionAdapter -> Provider Integration

Used by application/domain-adjacent code that needs a single model call
without building a whole Haystack pipeline (e.g. a future
``ModelTool``). Pipeline-internal generation goes through
``infrastructure.haystack.pipelines.research_pipeline`` directly instead —
that is idiomatic Haystack usage entirely inside this anti-corruption layer,
not a bypass of this port.
"""

from __future__ import annotations

from typing import Any

from haystack.components.generators.chat import MockChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret

from baobab_pulse.application.ports.model_execution_port import (
    ModelExecutionRequest,
    ModelExecutionResult,
)
from baobab_pulse.infrastructure.haystack.errors import translate_exceptions

_ROLE_FACTORY = {
    "system": ChatMessage.from_system,
    "user": ChatMessage.from_user,
}


def build_chat_generator(provider: str, *, api_key: str | None = None, model: str | None = None) -> Any:
    """Provider-neutral factory (item 37-38). ``provider`` is a Pulse-owned
    label from ``ModelVersion.provider`` — never a Haystack class name."""
    if provider == "openai":
        from haystack.components.generators.chat import OpenAIChatGenerator

        kwargs: dict[str, Any] = {}
        if api_key is not None:
            kwargs["api_key"] = Secret.from_token(api_key)
        if model is not None:
            kwargs["model"] = model
        return OpenAIChatGenerator(**kwargs)
    if provider == "mock":
        return MockChatGenerator()
    raise ValueError(
        f"unknown model provider {provider!r} — register a new branch here when Pulse adds provider "
        "support; do not hard-wire a provider name anywhere outside this factory (item 37)"
    )


class HaystackModelExecutionAdapter:
    def __init__(self, chat_generator: Any) -> None:
        self._generator = chat_generator

    async def generate(self, request: ModelExecutionRequest) -> ModelExecutionResult:
        return self._generate(request)

    @translate_exceptions("Haystack model execution")
    def _generate(self, request: ModelExecutionRequest) -> ModelExecutionResult:
        messages = [_ROLE_FACTORY.get(m.role, ChatMessage.from_user)(m.content) for m in request.messages]
        result = self._generator.run(messages=messages)
        replies: list[ChatMessage] = result["replies"]
        reply = replies[0] if replies else ChatMessage.from_assistant("")
        meta = reply.meta or {}
        return ModelExecutionResult(
            text=reply.text or "",
            usage=meta.get("usage", {}),
            finish_reason=meta.get("finish_reason"),
        )
