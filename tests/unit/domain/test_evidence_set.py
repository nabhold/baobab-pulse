from datetime import UTC, datetime

import pytest

from baobab_pulse.domain.evidence import Evidence, EvidenceSet
from baobab_pulse.domain.shared.enums import Classification, EvidenceDirection, TenantScope
from baobab_pulse.domain.shared.errors import InvariantViolation
from baobab_pulse.domain.shared.value_objects import Reference


def _evidence_set(*, with_entries: bool = True) -> EvidenceSet:
    entries = (
        (
            Evidence(
                id="evd_1",
                referenced_object=Reference(object_type="observation", object_id="obs_1"),
                direction=EvidenceDirection.SUPPORTS,
            ),
        )
        if with_entries
        else ()
    )
    return EvidenceSet(
        id="evs_1",
        purpose="test",
        entries=entries,
        tenant_scope=TenantScope.GLOBAL,
        classification=Classification.PUBLIC,
    )


def test_frozen_evidence_set_requires_at_least_one_entry() -> None:
    evidence_set = _evidence_set(with_entries=False)
    with pytest.raises(InvariantViolation):
        evidence_set.freeze(at=datetime.now(UTC))


def test_freeze_returns_a_new_frozen_copy() -> None:
    evidence_set = _evidence_set()
    frozen = evidence_set.freeze(at=datetime.now(UTC))
    assert frozen.frozen_at is not None
    assert evidence_set.frozen_at is None  # the original is untouched
    frozen.check_invariants()
