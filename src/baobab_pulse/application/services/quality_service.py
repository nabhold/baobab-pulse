"""QualityService — answers "what is the quality of this evidence?"

Kept as a distinct class from :class:`~baobab_pulse.application.services.confidence_service.ConfidenceService`
per ADR-PULSE-009 §282-284: quality and confidence are related but never
conflated. This reference implementation only covers missingness-aware
completeness scoring; corroboration/consistency/outlier detection etc.
(ADR-PULSE-009 §39-58) are left for the dedicated data-quality
implementation this scaffold does not attempt (req. 113/128).
"""

from __future__ import annotations

from baobab_pulse.domain.shared.enums import ConfidenceBand, Missingness


class QualityService:
    def completeness(self, *, total_fields: int, missing_fields: int) -> ConfidenceBand:
        """A deliberately simple, explainable completeness heuristic.

        QUAL-PULSE-008: missing SHALL never silently become zero — a caller
        with genuinely missing values should pass a real ``Missingness``
        reason on the affected :class:`~baobab_pulse.domain.observations.Observation`
        field rather than relying on this method to "fix" a hole in the data.
        """
        if total_fields <= 0:
            return ConfidenceBand.UNKNOWN
        ratio = 1 - (missing_fields / total_fields)
        if ratio >= 0.95:
            return ConfidenceBand.VERY_HIGH
        if ratio >= 0.8:
            return ConfidenceBand.HIGH
        if ratio >= 0.5:
            return ConfidenceBand.MODERATE
        if ratio > 0:
            return ConfidenceBand.LOW
        return ConfidenceBand.VERY_LOW

    def missingness_reason(self, *, collected: bool, applicable: bool, withheld: bool) -> Missingness:
        if withheld:
            return Missingness.WITHHELD
        if not applicable:
            return Missingness.NOT_APPLICABLE
        if not collected:
            return Missingness.NOT_COLLECTED
        return Missingness.NOT_AVAILABLE
