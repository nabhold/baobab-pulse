"""Normalisation — RawRecord -> canonical Observation, with provenance.

The actual field mapping (``mapper``) is necessarily provider/dataset
specific (ADR-PULSE-003 §26: "Provider-specific identifiers and schemas
SHALL be confined to adapter and mapping layers") — this module only
guarantees that every normalisation is recorded as a :class:`Provenance`
step, never performed silently.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from baobab_pulse.domain.ingestion import RawRecord
from baobab_pulse.domain.observations import Observation
from baobab_pulse.domain.shared.enums import ActorType, TransformationType
from baobab_pulse.domain.shared.value_objects import Provenance, Reference

Mapper = Callable[[RawRecord], Observation]


def normalise(raw_record: RawRecord, mapper: Mapper, *, mapper_version: str) -> tuple[Observation, Provenance]:
    observation = mapper(raw_record)
    provenance = Provenance(
        input_reference=Reference(object_type="raw_record", object_id=raw_record.id),
        output_reference=Reference(object_type="observation", object_id=observation.id),
        transformation_type=TransformationType.NORMALISE,
        transformation_version=mapper_version,
        actor_type=ActorType.SYSTEM,
        executed_at=datetime.now(UTC),
    )
    return observation, provenance
