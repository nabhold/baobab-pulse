import pytest

from baobab_pulse.domain.opportunities import Opportunity, OpportunityStatus, OpportunityType
from baobab_pulse.domain.risks import Risk
from baobab_pulse.domain.shared.enums import Classification, ConfidenceBand, ConfidenceMethod, TenantScope
from baobab_pulse.domain.shared.errors import InvariantViolation
from baobab_pulse.domain.shared.value_objects import Confidence


def _confidence() -> Confidence:
    return Confidence(
        confidence_band=ConfidenceBand.MODERATE,
        confidence_method=ConfidenceMethod.RULE_BASED,
        confidence_version="v1",
    )


def test_opportunity_requires_an_insight_unless_manually_originated() -> None:
    opportunity = Opportunity(
        id="opp_1",
        title="Coffee corridor",
        opportunity_type=OpportunityType.EXPORT,
        confidence=_confidence(),
        tenant_scope=TenantScope.GLOBAL,
        classification=Classification.PUBLIC,
    )
    with pytest.raises(InvariantViolation):
        opportunity.check_invariants()

    manual = opportunity.model_copy(update={"manually_originated": True})
    manual.check_invariants()  # does not raise


def test_opportunity_cannot_be_qualified_without_evidence() -> None:
    opportunity = Opportunity(
        id="opp_2",
        title="Coffee corridor",
        opportunity_type=OpportunityType.EXPORT,
        insight_references=("ins_1",),
        confidence=_confidence(),
        status=OpportunityStatus.QUALIFIED,
        tenant_scope=TenantScope.GLOBAL,
        classification=Classification.PUBLIC,
    )
    with pytest.raises(InvariantViolation):
        opportunity.check_invariants()


def test_opportunity_and_risk_are_independent_aggregates() -> None:
    # AGG-PULSE-009: documents the architectural separation at the type
    # level — neither aggregate's field set leaks the other's vocabulary.
    assert "risk_type" not in Opportunity.model_fields
    assert "opportunity_type" not in Risk.model_fields
