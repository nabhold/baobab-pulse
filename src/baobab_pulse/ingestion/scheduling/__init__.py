"""Acquisition scheduling — deliberately not implemented in this scaffold.

Item 69: "A scheduler SHALL eventually support scheduled acquisition,
source refresh, monitoring, backfill, reprocessing, continuous
intelligence... but do not implement the full scheduler in the initial
scaffold." This package exists as the reserved boundary a future
``pulse-scheduler`` deployment role (item 67-68) fills in; it holds no code
yet because there is no acquisition workload to schedule until the first
real ``SourceAdapter`` exists.

Execution/acquisition modes already exist —
``baobab_pulse.domain.ingestion.AcquisitionMode`` — and are reused here
rather than duplicated once a scheduler is built.
"""
