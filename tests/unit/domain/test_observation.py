from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from baobab_pulse.domain.observations import Observation, ObservationValueType
from baobab_pulse.domain.shared.enums import Classification, TenantScope
from baobab_pulse.domain.shared.value_objects import Reference, TemporalContext


def _observation() -> Observation:
    return Observation(
        id="obs_1",
        subject_reference=Reference(object_type="currency_pair", object_id="USD/ZAR"),
        metric="fx_rate",
        value=17.82,
        value_type=ObservationValueType.DECIMAL,
        temporal_context=TemporalContext(valid_time=datetime.now(UTC)),
        source_id="src_1",
        tenant_scope=TenantScope.GLOBAL,
        classification=Classification.PUBLIC,
    )


def test_observation_is_immutable_once_constructed() -> None:
    observation = _observation()
    with pytest.raises(ValidationError):
        observation.value = 18.0  # type: ignore[misc]


def test_observation_revision_uses_supersession_not_mutation() -> None:
    original = _observation()
    revised = original.model_copy(
        update={"id": "obs_2", "value": 18.0, "revision": 2, "supersedes_id": original.id}
    )
    assert revised.supersedes_id == original.id
    assert original.value == 17.82  # the original is untouched
