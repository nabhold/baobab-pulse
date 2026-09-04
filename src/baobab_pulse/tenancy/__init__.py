"""Tenant context propagation (item 48-51, architecture test #7).

Tenant context SHALL propagate through every layer — API request,
application service, job, pipeline execution, retrieval, tool call, model
invocation, persistence, events, logs, traces — and SHALL NEVER be silently
omitted from tenant-scoped execution (INV-PULSE-010, PULSE-013/014).
"""
