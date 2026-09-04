"""Application services and ports.

This layer orchestrates domain objects and defines the ports (``Protocol``
interfaces) that infrastructure adapters implement. Per the dependency
direction mandated by the platform brief (item 9)::

    Domain
       ^
    Application
       ^
    Ports
       ^
    Infrastructure
       ^
    Haystack Adapter

application code may depend on ``baobab_pulse.domain`` and on its own
``baobab_pulse.application.ports``, but never on
``baobab_pulse.infrastructure`` or on Haystack/FastAPI/asyncpg directly.
"""
