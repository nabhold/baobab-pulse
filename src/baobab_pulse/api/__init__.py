"""The headless API boundary (item 6, 60-61).

FastAPI is this scaffold's ASGI framework choice — see
``docs/architecture/api-framework-decision.md`` for why. The domain and
application layers stay independent of it: nothing under
``baobab_pulse.domain``/``baobab_pulse.application`` imports FastAPI: only
``baobab_pulse.api`` and ``baobab_pulse.contracts`` (pydantic request/
response schemas) do.
"""
