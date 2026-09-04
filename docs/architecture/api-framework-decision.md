# API Framework Decision

**Status:** Decided for this scaffold. **Scope:** implementation choice, not
a platform-level architecture decision — recorded here rather than as a
numbered `ADR-PULSE-0NN` because it is reversible without touching the
domain/application layers (item 61 requires exactly that independence).

## Decision

FastAPI, served by Uvicorn.

## Why

- **No Baobab or `nabhold` precedent to reuse.** `baobab-cp` is Go
  (`net/http`), `baobab-trade`/`baobab-cms` are TypeScript/MedusaJS/Payload,
  `baobab-erp` is Java/iDempiere. Pulse is the first Python engine in the
  ecosystem, so this is a fresh choice, not a deviation from an established
  one.
- **Pydantic-native.** The application already uses Pydantic v2 throughout
  the domain and contracts layers (item 93). FastAPI's request/response
  validation, dependency injection, and OpenAPI generation are built
  directly on Pydantic v2 — no second validation library, no manual JSON
  Schema authoring for `contracts.api.*`.
- **Async-first.** Pulse's execution model is asynchronous by preference
  (item 16, `PULSE-016`) — FastAPI/Starlette/Uvicorn are ASGI-native, which
  a WSGI framework (Flask, Django without ASGI) is not.
- **Automatic OpenAPI.** Item 105 asks for documented API architecture;
  FastAPI derives the OpenAPI document from the same type annotations that
  give request validation, so the two cannot drift silently.
- **Ecosystem maturity for a headless service.** No admin UI, no templating
  engine, no ORM opinion bundled in — matches the headless requirement
  (item 6) without extra weight to strip out.

## What this does not decide

- The domain and application layers remain FastAPI-independent (enforced by
  `tests/architecture/test_dependency_boundaries.py`). Replacing FastAPI
  later touches `api/` and `contracts/api/` only.
- This is not a claim that FastAPI is the only reasonable choice — Litestar
  and a hand-rolled ASGI app were the main alternatives considered, and
  either would have been defensible. FastAPI won on ecosystem maturity and
  the absence of any reason to prefer a smaller framework at this stage.
