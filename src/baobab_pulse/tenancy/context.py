"""Structural tenant-context propagation.

Item 49 (Tenant Isolation): "Never rely solely upon prompt instructions for
tenant isolation. Isolation SHALL be enforced structurally." This module is
that structural mechanism: a ``contextvars.ContextVar`` set once per
request/job at the boundary (API middleware, worker task entry point) and
read by every layer beneath it — retrieval filters, tool calls, persistence
queries — rather than threaded through every function signature by
convention (which is exactly the kind of thing that gets forgotten on one
new code path and becomes a cross-tenant leak).

``require_tenant_context()`` is the architecture-test-enforced guard
(architecture test #7: "tenant context cannot be silently omitted from
tenant-scoped application execution") — any tenant-scoped application
service or retrieval path calls it and gets a loud
:class:`~baobab_pulse.domain.shared.errors.TenantContextMissingError`
instead of quietly defaulting to "no tenant filter."
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token

from baobab_pulse.domain.shared.errors import TenantContextMissingError
from baobab_pulse.domain.shared.value_objects import TenantContext

_current_tenant_context: ContextVar[TenantContext | None] = ContextVar(
    "baobab_pulse_tenant_context", default=None
)


@contextmanager
def bind_tenant_context(context: TenantContext) -> Iterator[None]:
    """Bind ``context`` for the duration of the enclosed block — called once
    at a request/job boundary, never deep inside application logic."""
    token: Token[TenantContext | None] = _current_tenant_context.set(context)
    try:
        yield
    finally:
        _current_tenant_context.reset(token)


def current_tenant_context() -> TenantContext | None:
    return _current_tenant_context.get()


def require_tenant_context() -> TenantContext:
    context = _current_tenant_context.get()
    if context is None:
        raise TenantContextMissingError(
            "tenant-scoped execution attempted with no bound TenantContext; "
            "call bind_tenant_context() at the request/job boundary first"
        )
    return context
