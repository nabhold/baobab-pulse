from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from baobab_pulse.domain.shared.enums import (
    ActorType,
    Classification,
    ConfidenceBand,
    ConfidenceMethod,
    TransformationType,
    most_restrictive,
)
from baobab_pulse.domain.shared.value_objects import Confidence, Money, Provenance, Reference


def test_money_requires_iso_currency() -> None:
    Money(amount=1.0, currency="ZAR")
    with pytest.raises(ValidationError):
        Money(amount=1.0, currency="Rand")


def test_confidence_score_must_be_within_unit_interval() -> None:
    Confidence(
        confidence_band=ConfidenceBand.HIGH,
        confidence_method=ConfidenceMethod.STATISTICAL,
        confidence_version="v1",
        confidence_score=0.9,
    )
    with pytest.raises(ValidationError):
        Confidence(
            confidence_band=ConfidenceBand.HIGH,
            confidence_method=ConfidenceMethod.STATISTICAL,
            confidence_version="v1",
            confidence_score=1.5,
        )


def test_most_restrictive_classification() -> None:
    assert most_restrictive(Classification.PUBLIC, Classification.TENANT) == Classification.TENANT
    assert (
        most_restrictive(Classification.RESTRICTED, Classification.PUBLIC, Classification.CONFIDENTIAL)
        == Classification.RESTRICTED
    )


def test_provenance_is_frozen() -> None:
    provenance = Provenance(
        output_reference=Reference(object_type="observation", object_id="obs_1"),
        transformation_type=TransformationType.NORMALISE,
        transformation_version="v1",
        actor_type=ActorType.SYSTEM,
        executed_at=datetime.now(UTC),
    )
    with pytest.raises(ValidationError):
        provenance.transformation_version = "v2"  # type: ignore[misc]
