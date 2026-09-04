# Baobab Pulse

Baobab Pulse is the Baobab Platform's **Intelligence, Research and Evidence
Engine** — a headless, API-first, event-driven, multi-tenant service that
turns external data, other Baobab engines' events, and documentary evidence
into traceable, contextualised, time-aware intelligence.

> **Status:** Scaffold — domain model, application services, the Haystack
> anti-corruption layer, a headless API boundary, and a deterministic
> reference research pipeline are implemented and tested. Persistence is
> connectivity-only (no physical schema yet — see `ADR-PULSE-011`,
> pending), and no production intelligence domain (FX, commodities, trade
> statistics, ...) is implemented. See "Current implementation status"
> below.

## What Pulse is

Pulse continuously acquires, normalises, preserves, correlates, and
analyses evidence so Baobab-consuming organisations can understand what is
happening, what changed, why it may matter, what evidence supports an
assessment, and which decisions merit human consideration. See
`docs/adr/Baobab Pulse Intelligence Engine.md` (`ARCH-PULSE-001`) for the
full architectural mission.

## What Pulse is not

- **Not an ERP, commerce, or content system.** iDempiere, MedusaJS, and
  Payload CMS remain the systems of record for their domains; Pulse
  consumes their events/APIs, never their databases.
- **Not the Baobab Control Plane.** Tenant, market, context, and canonical
  entity identities are owned by `nabhold/baobab-cp` and referenced, never
  redefined, here.
- **Not an LLM wrapper.** Pulse remains functional for deterministic,
  rule-based and statistical intelligence without an LLM. AI is a
  capability inside Pulse, not its architectural centre.
- **Not a Haystack application with Baobab scripts glued on.** The
  dependency direction is the reverse: Baobab domain and application code
  is the core; Haystack is one embedded, replaceable engine behind a single
  anti-corruption boundary. See "Why Haystack" below.

## Why Haystack, and how it fits behind Pulse's boundaries

Pulse uses [deepset Haystack](https://haystack.deepset.ai) (`haystack-ai==3.1.1`,
verified to officially support Python 3.14) as its embedded AI
orchestration engine — components, pipelines, retrieval, generation, and
(future) agents/tools. Haystack is treated exactly like Baobab treats
MedusaJS, iDempiere, or Payload CMS: a specialist engine embedded behind a
Baobab-owned boundary, never the domain model itself.

```text
BAOBAB PULSE
│
├── Domain Model, Application Services, Canonical Contracts,
│   Provenance, Evidence, Quality, Temporal Semantics, Tenancy,
│   Security, Research, Intelligence Products
│
└── Haystack Integration Boundary (src/baobab_pulse/infrastructure/haystack/)
       │
       ├── Components   (EvidenceContextComponent, ClaimGroundingComponent)
       ├── Pipelines    (the reference research pipeline)
       ├── Tools        (BaobabToolContract -> haystack.tools.Tool)
       ├── Generators   (provider-neutral ModelExecutionPort adapter)
       ├── Document Stores (rebuildable retrieval projections)
       └── Tracing      (OpenTelemetry bridge)
```

Only `infrastructure/haystack/` imports `haystack` — enforced mechanically
by `tests/architecture/test_dependency_boundaries.py`. Full reasoning,
alternatives considered, and the upgrade/exit strategy are in
`docs/adr/ADR-PULSE-010 — Embedding Deepset Haystack as Pulse's Headless AI Orchestration Engine.md`.

**The test that matters:** if Baobab replaced Haystack tomorrow, would
Pulse's domain survive? Yes — `ResearchMission`, `Evidence`, `Observation`,
`Insight`, `Opportunity`, `Risk`, `Recommendation`, `Decision`, tenant
context, the API, and the event contracts are defined without importing
Haystack anywhere. Only the two reference components, one pipeline, and the
adapters in `infrastructure/haystack/` would need rewriting.

## Architecture

```text
Domain            (baobab_pulse.domain)           — no external dependencies
   ^
Application       (baobab_pulse.application)      — depends on domain + its own ports
   ^
Ports             (baobab_pulse.application.ports) — Protocol interfaces
   ^
Infrastructure    (baobab_pulse.infrastructure)    — implements ports
   ^
Haystack Adapter  (baobab_pulse.infrastructure.haystack) — the only Haystack import site
```

See `docs/architecture/overview.md` for Mermaid diagrams of the package
graph, the Haystack boundary, deployment topology, and the canonical
acquire-to-intelligence data flow, and
`docs/architecture/api-framework-decision.md` for why FastAPI.

## Repository structure

```text
src/baobab_pulse/
├── domain/            Canonical intelligence domain (ARCH-PULSE-CIM-001, ADR-PULSE-002)
│   ├── shared/         Value objects, enums, base types
│   ├── sources/ ingestion/ observations/ evidence/ signals/ analysis/
│   │   insights/ opportunities/ risks/ forecasting/ recommendations/
│   │   decisions/ models/ products/ research/
├── application/
│   ├── ports/          Protocol interfaces (PipelinePort, ModelExecutionPort, ...)
│   └── services/       ConfidenceService, QualityService, ResearchMissionService
├── contracts/          Wire shapes: CloudEvents envelope, RFC 9457 errors, API schemas
├── infrastructure/
│   ├── haystack/        The anti-corruption layer (see above)
│   ├── persistence/      asyncpg connectivity + in-memory repositories
│   ├── object_storage/   Raw evidence storage (in-memory reference impl)
│   ├── messaging/        Transactional outbox
│   └── observability/    Structured logging + OpenTelemetry
├── ingestion/           SourceAdapter port (ADR-PULSE-003) + reference/normalisation
├── api/                 FastAPI app, routers, middleware, error handling
├── tenancy/             Structural tenant-context propagation
├── security/            Classification enforcement
└── configuration/       Typed, fail-fast settings

tests/
├── unit/          domain, application, tenancy, security, infrastructure
├── integration/   real Haystack pipeline execution (deterministic, no credentials)
├── architecture/  dependency-boundary + platform-invariant enforcement
└── contract/      validates PulseEventEnvelope/ProblemDetails against vendored schemas

docs/
├── adr/            ARCH-PULSE-001, ARCH-PULSE-CIM-001, ADR-PULSE-001..010
├── architecture/    diagrams and the API framework decision
└── security/        agent/tool security posture

migrations/        Foundational SQL migration (schema boundaries + outbox table)
examples/          Runnable end-to-end reference pipeline demonstration
```

## Development setup

This repository uses the org's `baobab-dev` devcontainer image
(`.devcontainer/devcontainer.json`, `.nabhold/environment.yaml`) and `uv`
for Python dependency management.

```bash
uv sync --all-groups        # runtime + dev + security dependency groups
cp .env.example .env         # local configuration (no real secrets needed for tests)
make test                    # pytest, excludes the opt-in "provider" marker
make lint                    # ruff check
make typecheck                # mypy --strict
make security                  # bandit + pip-audit
uv run python examples/reference_research_pipeline.py   # runnable end-to-end demo
```

Local API + PostgreSQL: `docker compose up --build`, then
`curl localhost:8000/healthz`.

**Toolchain note:** targets `requires-python = ">=3.14"`, matching
`nabhold/baobab-dev`'s pinned Python 3.14.x. See `ADR-PULSE-010`'s "Version
verification" section for the Haystack/Python 3.14 compatibility check and
a caveat encountered with a pre-release CPython build in one sandboxed
authoring session (not a real gap in Haystack or Python 3.14 support).

## Testing

- **Core suite requires no external services or model-provider
  credentials** (`make test`): domain/application unit tests, a real
  Haystack pipeline run against `MockChatGenerator`, dependency-boundary
  enforcement, and contract validation against vendored `nabhold/shared`
  JSON Schemas.
- **Architecture tests** (`tests/architecture/`) mechanically enforce the
  ten invariants the platform brief requires (Haystack isolation, no HTTP
  framework/DB driver in the domain, tenant context cannot be silently
  omitted, provider exceptions don't escape as raw exceptions, the
  reference pipeline is deterministic, and the repository's dependency
  inputs are locked/pinned).
- **Provider-specific tests** (opt-in, marked `@pytest.mark.provider`, none
  yet exist) will require real credentials and run separately from `make
  test`.

## Configuration

Twelve-factor, typed, fail-fast (`baobab_pulse.configuration.settings.Settings`,
`pydantic-settings`). See `.env.example` for every recognised
`PULSE_*` environment variable. Invalid configuration raises immediately at
`Settings()` construction with the exact field at fault.

## Security

- **Tenant isolation is structural**, not prompt-based:
  `tenancy.context.require_tenant_context()` and
  `security.classification.may_access` — see `docs/security/agent-and-tool-security.md`
  for how this extends to Haystack retrieval/tools.
- **No mutating or `EXECUTE`-authority tool can be constructed** — see
  `infrastructure/haystack/tools/tool_adapter.py`.
- **Every Haystack/provider exception is translated** before it can leak a
  framework-specific structure through the public API
  (`infrastructure/haystack/errors.py`, `api/error_handlers.py`).
- Report vulnerabilities per `SECURITY.md` — never via a public issue.

## Tenancy

Every entity that participates in the evidence/intelligence chain carries a
`tenant_scope` (`GLOBAL`/`PLATFORM`/`TENANT`/`CONTEXT`/`PRIVATE`) and, where
required, a `tenant_context` referencing the Control-Plane-minted tenant id
— never a locally-invented one. See `domain/shared/base.GovernedEntity`.

## Integration boundaries

- **`nabhold/shared`**: canonical event envelope (CloudEvents profile) and
  RFC 9457 error contract are mirrored field-for-field in
  `contracts/events.py`/`contracts/errors.py`, validated in CI against
  vendored copies of the live schemas.
- **`nabhold/baobab-cp`**: Control Plane owns `CanonicalEntity`,
  `ExternalReference`, `Mapping`, `Market`, `DigitalEstate`, `Engine`,
  `Capability`, `Context`, `IsolationProfile` — Pulse references these by
  id, never redefines them.
- **MedusaJS / iDempiere / Payload CMS**: consumed through approved
  APIs/events only; direct database coupling is prohibited
  (`PULSE-003`).

## Current implementation status

Implemented and tested: the canonical domain model (all fifteen
ADR-PULSE-002 aggregates plus `ResearchMission`/`Claim`), application ports
and services, the Haystack anti-corruption layer with a deterministic
reference pipeline, a minimal headless API, `SourceAdapter` +
reference/normalisation ingestion, PostgreSQL connectivity, the
transactional outbox, and CI security/quality gates.

Not yet implemented (deliberately, per the platform brief's "no premature
business code/infrastructure"): the full physical PostgreSQL schema
(pending `ADR-PULSE-011`), a real (non-reference) source adapter, a
worker/scheduler deployment role, entity resolution, any production
intelligence domain (FX, commodities, weather, trade statistics, ...), and
any Haystack `Agent` instantiation.

## Roadmap

See `docs/adr/Baobab Pulse Intelligence Engine.md` §97-98 for the full ADR
family and derived-contract roadmap this scaffold works toward.

## Contributing

See `CONTRIBUTING.md`.
