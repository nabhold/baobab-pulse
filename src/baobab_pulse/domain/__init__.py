"""The Baobab Pulse canonical intelligence domain.

This package and everything beneath it implements the domain model defined by
``ARCH-PULSE-CIM-001`` (the Baobab Pulse Canonical Intelligence Model) and the
``ADR-PULSE-*`` decision family in ``docs/adr/``.

Hard rule (ADR-PULSE-001, INV-PULSE-012 and the platform's anti-corruption
mandate): nothing under ``baobab_pulse.domain`` may import Haystack, an HTTP
framework, a database driver/ORM, a cloud SDK, or a model-provider SDK. This
is enforced mechanically by ``tests/architecture/test_dependency_boundaries.py``.
If Baobab replaced Haystack tomorrow, every module in this package must still
compile and mean exactly what it means today.
"""
