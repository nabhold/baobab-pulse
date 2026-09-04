"""ConfidenceService — one of the domain services the platform brief (item 14)
requires to remain Baobab-owned, never delegated to a Haystack Component.

ADR-PULSE-009 §115 gives the composition as a *conceptual* relationship,
explicitly not a universal arithmetic formula::

    Evidence Quality + Corroboration + Method Quality + Temporal Fitness
      + Coverage - Contradictions - Material Missingness - Identity Uncertainty
      = JUSTIFIED CONFIDENCE

so this service never collapses a ``QualityProfile`` into a weighted-sum
float. It composes ordinal ``ConfidenceBand`` values by taking the *weakest*
material dimension — a defensible, explainable, non-fabricated method that
is itself declared as ``ConfidenceMethod.RULE_BASED`` — never claims to be
authoritative statistical calibration.

ADR-PULSE-009 §282-284: ``QualityService`` answers "what is the quality of
this evidence?"; ``ConfidenceService`` answers "given this evidence and
methodology, how strongly is this conclusion justified?" — the two are
never conflated, hence ``QualityService`` (in ``quality_service.py``) is a
separate class even though both work over the same ``QualityProfile``.
"""

from __future__ import annotations

from baobab_pulse.domain.shared.enums import ConfidenceBand, ConfidenceMethod
from baobab_pulse.domain.shared.value_objects import Confidence, QualityProfile

_BAND_ORDER = (
    ConfidenceBand.UNKNOWN,
    ConfidenceBand.VERY_LOW,
    ConfidenceBand.LOW,
    ConfidenceBand.MODERATE,
    ConfidenceBand.HIGH,
    ConfidenceBand.VERY_HIGH,
)

_METHOD_VERSION = "confidence-service-weakest-link-1"


class ConfidenceService:
    """Deterministic, explainable, non-LLM confidence composition.

    QUAL-PULSE-021 (ADR-PULSE-009): "LLM self-reported confidence SHALL NOT
    be accepted as intelligence confidence." This service is the only
    sanctioned way a Confidence value object is constructed for consequential
    intelligence; a Haystack pipeline never sets ``Confidence`` fields
    itself (see ``infrastructure.haystack.components.claim_grounding_component``,
    which calls back into this service rather than trusting model output).
    """

    def compose(
        self,
        quality: QualityProfile,
        *,
        independent_corroborating_sources: int,
        has_unresolved_contradiction: bool,
    ) -> Confidence:
        dimensions = (
            quality.accuracy,
            quality.completeness,
            quality.consistency,
            quality.authority,
            quality.methodology_quality,
        )
        band = self._weakest(dimensions)

        # QUAL-PULSE-011: duplicate/syndicated evidence is not independent
        # corroboration — a caller must have already deduplicated sources
        # before counting them here. Fewer than two independent sources
        # caps the result at MODERATE regardless of how strong any single
        # dimension looks.
        if independent_corroborating_sources < 2 and band.value in (
            ConfidenceBand.HIGH.value,
            ConfidenceBand.VERY_HIGH.value,
        ):
            band = ConfidenceBand.MODERATE

        # A material unresolved contradiction caps confidence rather than
        # being silently averaged away (QUAL-PULSE-014).
        if has_unresolved_contradiction and band != ConfidenceBand.UNKNOWN:
            band = self._cap(band, ConfidenceBand.LOW)

        return Confidence(
            confidence_band=band,
            confidence_method=ConfidenceMethod.RULE_BASED,
            confidence_version=_METHOD_VERSION,
        )

    @staticmethod
    def _weakest(bands: tuple[ConfidenceBand, ...]) -> ConfidenceBand:
        return min(bands, key=_BAND_ORDER.index)

    @staticmethod
    def _cap(band: ConfidenceBand, ceiling: ConfidenceBand) -> ConfidenceBand:
        return band if _BAND_ORDER.index(band) <= _BAND_ORDER.index(ceiling) else ceiling
