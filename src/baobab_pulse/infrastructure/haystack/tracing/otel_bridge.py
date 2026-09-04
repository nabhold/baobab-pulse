"""OpenTelemetry-backed ``haystack.tracing.Tracer``.

Wires Haystack's own tracing hook (``haystack.tracing.enable_tracing``) to
this service's OpenTelemetry ``TracerProvider``
(``infrastructure.observability.telemetry``), so a pipeline run's spans join
the same trace as the HTTP request / job that triggered it (item 76-77:
``correlation_id``/``research_mission_id``/``pipeline_run_id`` propagate as
span attributes, not just log fields).

Deliberately hand-rolled rather than depending on a separate
``opentelemetry-haystack`` integration package the platform brief's item 8
would count as an unnecessary integration to install for the initial
scaffold — Haystack's ``Tracer``/``Span`` ABCs are small enough that this is
a handful of lines, not a maintenance burden.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from haystack.tracing import Span as HaystackSpan
from haystack.tracing import Tracer as HaystackTracer
from opentelemetry import trace
from opentelemetry.trace import Span as OtelSpan

_TRACER_NAME = "baobab_pulse.infrastructure.haystack"


class _OtelSpanAdapter(HaystackSpan):
    def __init__(self, otel_span: OtelSpan) -> None:
        self._otel_span = otel_span

    def set_tag(self, key: str, value: Any) -> None:
        self._otel_span.set_attribute(key, str(value))

    def raw_span(self) -> OtelSpan:
        return self._otel_span


class OpenTelemetryHaystackTracer(HaystackTracer):
    """Registered once at process start via
    ``haystack.tracing.enable_tracing(OpenTelemetryHaystackTracer())`` — see
    ``infrastructure.observability.telemetry.configure_telemetry``."""

    def __init__(self) -> None:
        self._tracer = trace.get_tracer(_TRACER_NAME)
        self._current: _OtelSpanAdapter | None = None

    @contextmanager
    def trace(
        self, operation_name: str, tags: dict[str, Any] | None = None, parent_span: HaystackSpan | None = None
    ) -> Iterator[HaystackSpan]:
        with self._tracer.start_as_current_span(operation_name) as otel_span:
            adapter = _OtelSpanAdapter(otel_span)
            if tags:
                adapter.set_tags(tags)
            previous, self._current = self._current, adapter
            try:
                yield adapter
            finally:
                self._current = previous

    def current_span(self) -> HaystackSpan | None:
        return self._current


def enable_haystack_tracing() -> None:
    """Register :class:`OpenTelemetryHaystackTracer` with Haystack.

    ``infrastructure.observability.telemetry`` calls this instead of
    touching ``haystack.tracing`` itself, keeping ``infrastructure.haystack``
    the only package in the codebase that imports ``haystack`` directly.
    """
    from haystack.tracing import enable_tracing

    enable_tracing(OpenTelemetryHaystackTracer())
