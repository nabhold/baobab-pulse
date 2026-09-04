"""Pydantic request/response schemas for the API boundary.

These are deliberately separate types from the domain aggregates in
``baobab_pulse.domain`` — an API contract and a domain model are allowed to
diverge (item 61: "the application/domain layer independent of the HTTP
framework"), even though today's mapping between them is close to 1:1.
"""
