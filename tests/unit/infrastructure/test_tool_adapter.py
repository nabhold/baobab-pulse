import pytest

from baobab_pulse.domain.shared.enums import AutomationAuthorityLevel
from baobab_pulse.domain.shared.value_objects import TenantContext
from baobab_pulse.infrastructure.haystack.tools.tool_adapter import (
    BaobabToolContract,
    ToolAuthorityRefusedError,
    ToolSideEffect,
    to_haystack_tool,
)
from baobab_pulse.tenancy.context import bind_tenant_context


def _contract(**overrides: object) -> BaobabToolContract:
    defaults: dict[str, object] = {
        "name": "search_evidence",
        "purpose": "Search Pulse evidence for a query.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
    }
    defaults.update(overrides)
    return BaobabToolContract(**defaults)  # type: ignore[arg-type]


def test_mutating_tool_is_refused() -> None:
    with pytest.raises(ToolAuthorityRefusedError):
        to_haystack_tool(_contract(side_effect=ToolSideEffect.MUTATING), function=lambda: None)


def test_execute_authority_is_refused() -> None:
    with pytest.raises(ToolAuthorityRefusedError):
        to_haystack_tool(
            _contract(authority_level=AutomationAuthorityLevel.EXECUTE), function=lambda: None
        )


def test_read_only_tool_requires_bound_tenant_context() -> None:
    from baobab_pulse.domain.shared.errors import TenantContextMissingError

    tool = to_haystack_tool(_contract(), function=lambda query: f"results for {query}")
    # Called directly (not via Tool.invoke, which wraps every exception in a
    # Haystack ToolInvocationError) to assert precisely which error our own
    # governance wrapper raises before Haystack ever sees it.
    assert tool.function is not None
    with pytest.raises(TenantContextMissingError):
        tool.function(query="coffee")


def test_read_only_tool_runs_once_tenant_context_is_bound() -> None:
    tool = to_haystack_tool(_contract(), function=lambda query: f"results for {query}")
    with bind_tenant_context(TenantContext(tenant_id="tn_test01")):
        assert tool.invoke(query="coffee") == "results for coffee"
