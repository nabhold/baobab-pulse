"""Retrieval projections — never Pulse's canonical persistence (item 29-31).

A Haystack ``DocumentStore`` here is always a rebuildable *projection* of
canonical Evidence, not a system of record. If the projection is lost, it is
rebuilt from ``EvidenceSet``/``Observation`` rows in PostgreSQL — never the
other way around.
"""
