# Changelog

All notable changes to Baobab Pulse are documented in this file. Format
loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

- Initial application scaffold: domain model (Source, Observation,
  EvidenceSet, Signal, Analysis, Insight, Opportunity, Risk, Forecast,
  Recommendation, Decision, Model, IntelligenceProduct, ResearchMission,
  Claim) per `ARCH-PULSE-CIM-001` and `ADR-PULSE-002`.
- Application layer: ports (`PipelinePort`, `ModelExecutionPort`,
  `EventPublisher`, `ObjectStoragePort`, `Repository[T]`), and the
  `ConfidenceService`/`QualityService`/`ResearchMissionService` domain
  services.
- Haystack anti-corruption layer (`infrastructure/haystack/`): a reference
  pipeline (`EvidenceContextComponent` -> `ChatGenerator` ->
  `ClaimGroundingComponent`), a provider-neutral model-execution adapter, a
  `BaobabToolContract` -> `haystack.tools.Tool` adapter with mandatory
  authority/side-effect refusal, and an OpenTelemetry tracing bridge.
- Headless FastAPI API (`api/`): health/readiness endpoints and a minimal
  `/research-missions` resource, with RFC 9457 problem+json error
  responses and a CloudEvents-profile event envelope
  (`contracts/events.py`, `contracts/errors.py`) mirroring
  `nabhold/shared`'s schemas.
- Ingestion layer: `SourceAdapter` port (ADR-PULSE-003) and a deterministic
  `ReferenceSourceAdapter` for tests.
- PostgreSQL connectivity (`asyncpg`) and a foundational migration
  (`migrations/0001_init.sql`) establishing schema boundaries and the
  transactional outbox table.
- Test suite: unit, integration (real Haystack pipeline execution),
  architecture (dependency-boundary enforcement), and contract
  (JSON-Schema validation against vendored `nabhold/shared` contracts)
  tests — none require external services or model-provider credentials.
- `docs/adr/ADR-PULSE-010`: the decision to embed deepset Haystack
  (`haystack-ai==3.1.1`) as Pulse's headless AI orchestration engine.
- CI: `security-python.yml` (Bandit + pip-audit) and `security-codeql.yml`
  adopted from `nabhold/shared`; `ci.yml` extended with lint/typecheck/test
  gates; `dependabot.yml` extended to track `uv` and `docker` ecosystems.
- Production `Dockerfile` (multi-stage, non-root, distinct from the
  `baobab-dev` development image) and a local-development
  `docker-compose.yml`.

### Notes

- Targets Python 3.14 (`requires-python = ">=3.14"`), matching
  `nabhold/baobab-dev`'s pinned runtime. See `ADR-PULSE-010`'s "Version
  verification" section for the compatibility check performed against
  Haystack 3.1.1 and the toolchain caveat encountered while authoring this
  scaffold.
