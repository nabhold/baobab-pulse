"""Canonical identifier generation.

``ARCH-PULSE-CIM-001`` §4 requires every canonical entity's ``id`` to be
globally unique, immutable, and independent of provider identifiers, tenant
identifiers, database sequence numbers, source URLs, or external business
keys. The CIM document deliberately does not mandate a specific format
(§187), so this module is Pulse's own derivation: a type-prefixed UUID4,
which keeps ids collision-resistant without a coordinating authority while
remaining easy to eyeball in logs and API responses (e.g. ``obs_3f1c...``).
"""

from __future__ import annotations

from uuid import uuid4

_SEPARATOR = "_"


def new_id(prefix: str) -> str:
    """Return a new canonical identifier for the given entity-type prefix.

    :param prefix: A short lowercase entity-type tag (e.g. ``"obs"``,
        ``"evs"``, ``"sig"``). Never itself treated as meaningful identity —
        only the full string is the id.
    """
    if not prefix or not prefix.islower() or not prefix.isalnum():
        raise ValueError("id prefix must be a non-empty lowercase alphanumeric tag")
    return f"{prefix}{_SEPARATOR}{uuid4().hex}"


def is_valid_id(value: str, *, prefix: str | None = None) -> bool:
    """Structural validation only — this never confirms the id actually exists."""
    if not value or _SEPARATOR not in value:
        return False
    tag, _, rest = value.partition(_SEPARATOR)
    if prefix is not None and tag != prefix:
        return False
    return len(rest) == 32
