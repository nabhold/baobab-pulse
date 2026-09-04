"""OpenTelemetry setup (item 73, 75-77).

``configure_telemetry`` is called once, at process start (API and worker
entry points), never per-request. It is opt-in for trace export
(``Settings.otel_traces_enabled``) — the default ``TracerProvider`` still
runs so ``get_tracer(...).start_as_current_span(...)`` calls throughout the
codebase never fail even when no collector is configured (spans are simply
not exported anywhere).
"""

from __future__ import annotations

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from baobab_pulse.configuration.settings import Settings

_configured = False


def configure_telemetry(settings: Settings) -> None:
    """Idempotent: OpenTelemetry's global ``TracerProvider`` can only be set
    once per process, so a second call (e.g. ``create_app()`` invoked more
    than once in the same test process) is a deliberate no-op rather than a
    noisy "overriding provider" warning on every subsequent call."""
    global _configured
    if _configured:
        return
    _configured = True

    resource = Resource.create(
        {"service.name": settings.service_name, "deployment.environment": settings.environment.value}
    )
    provider = TracerProvider(resource=resource)

    if settings.otel_traces_enabled and settings.otel_exporter_otlp_endpoint:
        # Deliberately not a base dependency (item 8: minimal, only what the
        # scaffold needs): `opentelemetry-exporter-otlp-proto-http` is an
        # extra a deployment installs only once it actually wants to export
        # traces somewhere. Failing here with a clear ImportError is
        # preferable to bundling an exporter nothing may ever use.
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

    # Only `infrastructure.haystack` may import `haystack` (architecture
    # test `test_only_the_haystack_infrastructure_package_imports_haystack`)
    # — this module calls into that package's own registration function
    # rather than touching `haystack.tracing` itself.
    from baobab_pulse.infrastructure.haystack.tracing.otel_bridge import enable_haystack_tracing

    enable_haystack_tracing()
