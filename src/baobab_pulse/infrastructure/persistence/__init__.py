"""PostgreSQL connectivity (item 62-63).

Only connection/pool management and a health check exist here — the full
Pulse physical schema is explicitly out of scope until ADR-PULSE-011
(PostgreSQL Physical Architecture) exists (item 63, 128 Phase 5). Until
then, ``in_memory_repositories`` provides working ``Repository[T]``
implementations for tests, examples, and local development.
"""
