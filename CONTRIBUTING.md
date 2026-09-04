# Contributing to Baobab Pulse

Thank you for contributing to Baobab Pulse — the Baobab Platform's
Intelligence, Research and Evidence Engine. This document covers what is
specific to this repository; org-wide conventions (branch naming, commit
style, PR process) follow Nabhold's standard practice as seen across
`nabhold/*`.

## Before you start

Read, in order:

1. `README.md` — what Pulse is, and is not.
2. `docs/adr/Baobab Pulse Intelligence Engine.md` (`ARCH-PULSE-001`) and the
   `ADR-PULSE-*` family in `docs/adr/` — these are binding architecture,
   not background reading. If a change conflicts with one, the ADR wins;
   propose a new ADR instead of working around it silently.
3. `docs/adr/ADR-PULSE-010 — Embedding Deepset Haystack as Pulse's Headless AI Orchestration Engine.md`
   for how Haystack fits behind Pulse's boundaries.

## The one rule that matters most

**`baobab_pulse.domain` and `baobab_pulse.application` never import
Haystack, FastAPI, asyncpg, or a model-provider SDK.** Only
`baobab_pulse.infrastructure.haystack` imports `haystack`. This is enforced
by `tests/architecture/test_dependency_boundaries.py` — a PR that breaks it
fails CI, no exceptions without a new ADR.

## Development environment

This repository uses the org's `baobab-dev` devcontainer image and `uv` for
Python dependency management.

```bash
uv sync --all-groups   # installs runtime + dev + security dependency groups
make test               # pytest, excluding the "provider" marker
make lint                # ruff check
make typecheck           # mypy --strict
make security             # bandit + pip-audit
```

Core tests never require a model-provider API key (item 96) — the
reference Haystack pipeline uses `haystack.components.generators.chat.MockChatGenerator`.
Do not add a test to `tests/unit`, `tests/integration`, `tests/architecture`,
or `tests/contract` that needs one; if you're adding provider-specific
tests, mark them `@pytest.mark.provider` so `make test` continues to skip
them by default.

## Adding a Haystack component or pipeline

- New components live in `infrastructure/haystack/components/`, one class
  per narrow technical capability (platform brief item 13) — do not fold
  domain logic (confidence scoring, quality assessment, entity resolution)
  into a component; call the relevant `application.services.*` class
  instead (item 14).
- New pipelines live in `infrastructure/haystack/pipelines/`, expose a
  `PIPELINE_NAME`/`PIPELINE_VERSION`, and are built by a plain function
  (`build_*_pipeline`) — never treat a pipeline definition as the source of
  truth for a domain object (item 18).
- Anything a pipeline returns that crosses back into application code must
  be a plain type from `application.ports.pipeline_port` (or a new port you
  add there) — never a `haystack.*` type.

## Adding a domain aggregate or value object

- Match the field names and enum values already extracted from the
  governing ADRs (see the `ADR-PULSE-*` citations in each module's
  docstring) — do not invent a different name for a concept the ADRs
  already name.
- New aggregates that are versioned/immutable per ADR-PULSE-002 §63 use
  `model_config = ConfigDict(frozen=True)` and `supersedes_id`/
  `superseded_by_id`, not in-place mutation.

## Pull requests

- Keep PRs focused on one architectural concern.
- Run `make lint typecheck test security` before opening a PR — CI runs the
  same checks (`ci.yml`, `security-python.yml`, `security-codeql.yml`,
  `foundation.yml`).
- If your change touches a contract in `contracts/` that mirrors a
  `nabhold/shared` schema, re-verify against the live schema and update the
  vendored copy under `tests/fixtures/contracts/`.

## Reporting a security issue

Do not open a public issue — see `SECURITY.md`.
