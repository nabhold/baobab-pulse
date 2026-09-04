"""The Haystack anti-corruption layer.

This is the *only* subtree of the codebase allowed to ``import haystack``
(enforced by ``tests/architecture/test_dependency_boundaries.py``). Every
public symbol Pulse exposes across this boundary — requests, results, tools,
model messages — is a plain type from ``baobab_pulse.application.ports`` or
``baobab_pulse.domain``, never a ``haystack.*`` class.

Layout (platform brief item 12, "minimum useful structural boundaries" —
categories not yet populated, e.g. ``rankers/``, ``serializers/``, are not
created until something actually needs them):

- ``pipeline_adapter`` — implements ``PipelinePort``.
- ``components/`` — Pulse-authored Haystack ``@component`` classes.
- ``pipelines/`` — pipeline *construction* (a Python function building a
  ``haystack.Pipeline``, not a business object).
- ``generators/`` — binds a ``ModelVersion`` to a concrete Haystack
  Generator/ChatGenerator; also the ``ModelExecutionPort`` adapter for
  non-pipeline model calls.
- ``document_stores/`` — retrieval *projections* built from canonical
  Evidence, always rebuildable, never canonical storage themselves.
- ``tools/`` — the Baobab Tool Contract -> Haystack ``Tool`` adapter.
- ``tracing/`` — bridges Haystack's tracer interface to this service's
  OpenTelemetry setup.
"""
