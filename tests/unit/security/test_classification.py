from baobab_pulse.domain.shared.enums import Classification
from baobab_pulse.security.classification import may_access


def test_public_clearance_cannot_read_restricted() -> None:
    assert not may_access(
        requester_clearance=Classification.PUBLIC, object_classification=Classification.RESTRICTED
    )


def test_restricted_clearance_can_read_public() -> None:
    assert may_access(
        requester_clearance=Classification.RESTRICTED, object_classification=Classification.PUBLIC
    )


def test_equal_clearance_is_sufficient() -> None:
    assert may_access(
        requester_clearance=Classification.TENANT, object_classification=Classification.TENANT
    )
