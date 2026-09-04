"""Pipeline construction.

A pipeline here is an execution graph (item 15), not the canonical
definition of the Pulse business domain (item 18) — the objects it produces
(``ClaimCandidate``) are still unvalidated until
``application.services.research_mission_service`` promotes them.
"""
