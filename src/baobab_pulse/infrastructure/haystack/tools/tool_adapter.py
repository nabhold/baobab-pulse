"""BaobabToolContract and its adapter to ``haystack.tools.Tool``.

Every field required by item 20 (name, purpose, input/output contract,
required permissions, tenant scope, side-effect classification, audit
behaviour, timeout, failure semantics) is a real field on
:class:`BaobabToolContract` — nothing is left to convention.

Item 21-22: initial agents are READ_ONLY or ANALYSIS_ONLY, and SHALL NOT
directly mutate operational systems. ``to_haystack_tool`` enforces this
mechanically: a contract declaring ``ToolSideEffect.MUTATING`` is refused
outright — there is no "governed action contract" for autonomous mutation
yet (item 22), so this scaffold does not provide a code path to bypass the
refusal. Introducing one is a future ADR's decision, not a runtime flag.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from enum import StrEnum
from typing import Any

from haystack.tools import Tool
from pydantic import BaseModel, ConfigDict

from baobab_pulse.domain.shared.enums import AutomationAuthorityLevel
from baobab_pulse.domain.shared.errors import PulseError
from baobab_pulse.tenancy.context import require_tenant_context

logger = logging.getLogger(__name__)


class ToolSideEffect(StrEnum):
    NONE = "NONE"
    READ_ONLY = "READ_ONLY"
    MUTATING = "MUTATING"


class ToolAuthorityRefusedError(PulseError):
    """Raised by :func:`to_haystack_tool` for a contract this scaffold has
    no governed authority to expose as an agent-callable tool."""


class ToolTimeoutError(PulseError):
    """Raised when a tool call exceeds ``BaobabToolContract.timeout_seconds``
    (item 20's "failure semantics" requirement)."""


class BaobabToolContract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    purpose: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any] | None = None
    required_permissions: tuple[str, ...] = ()
    tenant_scoped: bool = True
    side_effect: ToolSideEffect = ToolSideEffect.READ_ONLY
    audit: bool = True
    timeout_seconds: float = 30.0
    authority_level: AutomationAuthorityLevel = AutomationAuthorityLevel.ANALYSE
    """Item 19-21: an agent's authority ladder position. Default is
    ``ANALYSE`` — never ``EXECUTE`` without an explicit future policy."""


def to_haystack_tool(contract: BaobabToolContract, function: Callable[..., Any]) -> Tool:
    if contract.side_effect == ToolSideEffect.MUTATING:
        raise ToolAuthorityRefusedError(
            f"tool {contract.name!r} declares side_effect=MUTATING; Pulse has no governed action "
            "contract authorising an agent to mutate an operational system (item 22)"
        )
    if contract.authority_level == AutomationAuthorityLevel.EXECUTE:
        raise ToolAuthorityRefusedError(
            f"tool {contract.name!r} declares authority_level=EXECUTE; initial Pulse agents are "
            "READ_ONLY/ANALYSIS_ONLY (item 21)"
        )

    def _governed(*args: Any, **kwargs: Any) -> Any:
        if contract.tenant_scoped:
            require_tenant_context()
        if contract.audit:
            logger.info(
                "tool_invocation",
                extra={
                    "tool_name": contract.name,
                    "authority_level": contract.authority_level.value,
                    "side_effect": contract.side_effect.value,
                },
            )
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(function, *args, **kwargs)
            try:
                return future.result(timeout=contract.timeout_seconds)
            except FutureTimeoutError as exc:
                raise ToolTimeoutError(
                    f"tool {contract.name!r} exceeded its {contract.timeout_seconds}s timeout"
                ) from exc

    return Tool(
        name=contract.name,
        description=contract.purpose,
        parameters=contract.input_schema,
        function=_governed,
    )
