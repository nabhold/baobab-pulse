"""Domain-level errors.

These are the only exceptions the domain layer raises. Infrastructure and
provider-specific exceptions (Haystack, asyncpg, httpx, ...) are translated
into these — or into ``baobab_pulse.infrastructure`` error types that
subclass :class:`PulseError` — at the relevant anti-corruption boundary; they
never cross into application/domain code directly (req. #120).
"""

from __future__ import annotations


class PulseError(Exception):
    """Base for every error raised by Pulse's own domain/application code."""


class InvariantViolation(PulseError):
    """Raised when an aggregate invariant defined in ADR-PULSE-002 (or a
    domain-specific ADR) would otherwise be violated."""


class ImmutableObjectError(PulseError):
    """Raised when code attempts to mutate a value that ADR-PULSE-002/004
    require to be immutable or append-only (e.g. a published Observation,
    a frozen EvidenceSet, a committed SourceArtefact)."""


class TenantContextMissingError(PulseError):
    """Raised when tenant-scoped application execution is attempted without
    an established :class:`~baobab_pulse.tenancy.context.TenantContext`
    (architecture invariant: tenant context cannot be silently omitted)."""
