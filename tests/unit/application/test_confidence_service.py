from baobab_pulse.application.services.confidence_service import ConfidenceService
from baobab_pulse.domain.shared.enums import ConfidenceBand
from baobab_pulse.domain.shared.value_objects import QualityProfile


def test_confidence_is_the_weakest_material_dimension() -> None:
    service = ConfidenceService()
    quality = QualityProfile(
        accuracy=ConfidenceBand.VERY_HIGH,
        completeness=ConfidenceBand.HIGH,
        consistency=ConfidenceBand.LOW,  # the weakest link
        authority=ConfidenceBand.HIGH,
        methodology_quality=ConfidenceBand.HIGH,
    )
    confidence = service.compose(
        quality, independent_corroborating_sources=3, has_unresolved_contradiction=False
    )
    assert confidence.confidence_band == ConfidenceBand.LOW


def test_fewer_than_two_sources_caps_confidence_at_moderate() -> None:
    service = ConfidenceService()
    quality = QualityProfile(
        accuracy=ConfidenceBand.VERY_HIGH,
        completeness=ConfidenceBand.VERY_HIGH,
        consistency=ConfidenceBand.VERY_HIGH,
        authority=ConfidenceBand.VERY_HIGH,
        methodology_quality=ConfidenceBand.VERY_HIGH,
    )
    confidence = service.compose(
        quality, independent_corroborating_sources=1, has_unresolved_contradiction=False
    )
    assert confidence.confidence_band == ConfidenceBand.MODERATE


def test_unresolved_contradiction_caps_confidence_at_low() -> None:
    service = ConfidenceService()
    quality = QualityProfile(
        accuracy=ConfidenceBand.VERY_HIGH,
        completeness=ConfidenceBand.VERY_HIGH,
        consistency=ConfidenceBand.VERY_HIGH,
        authority=ConfidenceBand.VERY_HIGH,
        methodology_quality=ConfidenceBand.VERY_HIGH,
    )
    confidence = service.compose(
        quality, independent_corroborating_sources=5, has_unresolved_contradiction=True
    )
    assert confidence.confidence_band == ConfidenceBand.LOW
