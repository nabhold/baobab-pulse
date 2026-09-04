"""External source acquisition (ADR-PULSE-003).

Source adapters own provider authentication, request construction,
pagination, provider-specific rate limiting and cursoring, transport
retries, response decoding, and provider error handling. They do NOT own
canonical business interpretation, cross-source entity resolution,
opportunity/risk scoring, report writing, or tenant decisions
(ADR-PULSE-003 §25) — those stay in ``application``/``domain``.
"""
