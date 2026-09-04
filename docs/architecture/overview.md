# Baobab Pulse — Architecture Overview

This document orients a reader across the repository's actual package
layout, dependency direction, and deployment shape. It is a map, not a
decision record — decisions live in `docs/adr/`.

## What Pulse is (and is not)

See the root `README.md` and `docs/adr/Baobab Pulse Intelligence Engine.md`
(`ARCH-PULSE-001`) for the full statement. In one line: Pulse turns
heterogeneous internal and external evidence into traceable, contextualised,
time-aware intelligence, without becoming the system of record for the
operational domains that evidence describes.

## Package layout and dependency direction

```mermaid
graph TD
    subgraph "src/baobab_pulse"
        domain["domain/<br/>(no external deps)"]
        application["application/<br/>(ports + services)"]
        contracts["contracts/<br/>(wire shapes)"]
        infrastructure["infrastructure/<br/>(adapters)"]
        haystack_acl["infrastructure/haystack/<br/>(the ONLY package<br/>that imports haystack)"]
        api["api/ (FastAPI)"]
        ingestion["ingestion/<br/>(SourceAdapter)"]
        tenancy["tenancy/"]
        security["security/"]
        configuration["configuration/"]
    end

    api --> application
    api --> contracts
    ingestion --> domain
    application --> domain
    application --> tenancy
    infrastructure --> application
    haystack_acl --> application
    haystack_acl --> domain
    contracts --> domain
    api --> infrastructure
    api --> haystack_acl

    domain -.->|"forbidden"| haystack_acl
    application -.->|"forbidden"| haystack_acl
    contracts -.->|"forbidden"| haystack_acl
```

`tests/architecture/test_dependency_boundaries.py` enforces the solid
arrows' absence in the wrong direction mechanically (AST import scanning),
not by convention alone.

## The Haystack anti-corruption boundary

```mermaid
graph LR
    RM["ResearchMission<br/>(domain)"] --> Service["ResearchMissionService<br/>(application)"]
    Service --> Port["PipelinePort<br/>(application.ports, a Protocol)"]
    Port --> Adapter["HaystackPipelineAdapter<br/>(infrastructure.haystack)"]
    Adapter --> Pipeline["haystack.Pipeline<br/>(EvidenceContextComponent -&gt;<br/>ChatGenerator -&gt; ClaimGroundingComponent)"]
    Pipeline --> Adapter
    Adapter --> Candidate["ClaimCandidate<br/>(plain pydantic DTO,<br/>status=CANDIDATE)"]
    Candidate --> Validation["Baobab Validation Boundary<br/>(ResearchMissionService._ground_candidate)"]
    Validation --> Claim["domain.Claim<br/>(status=EVIDENCED or dropped)"]
```

Every arrow crossing from `Adapter` back out is a plain Python/pydantic
type — never a `haystack.*` class. See
`docs/adr/ADR-PULSE-010 — Embedding Deepset Haystack as Pulse's Headless AI Orchestration Engine.md`
for the full reasoning, and
`tests/integration/test_haystack_reference_pipeline.py` for this exact flow
executing deterministically.

## Deployment topology

```mermaid
graph TD
    subgraph "pulse-api (this repo's Dockerfile)"
        API["FastAPI app<br/>(headless HTTP boundary)"]
    end
    subgraph "pulse-worker (future — item 67; not yet built)"
        Worker["Async job execution<br/>(ingestion, analysis, pipeline runs)"]
    end
    subgraph "pulse-scheduler (future — item 69; not yet built)"
        Scheduler["Acquisition scheduling"]
    end

    API --> PG[("PostgreSQL 17")]
    API --> OS[("Object Storage<br/>(raw evidence)")]
    API --> Queue[("Job Queue<br/>(not yet selected)")]
    Worker --> PG
    Worker --> OS
    Worker --> Haystack["Haystack Engine<br/>(models, tools, retrieval)"]
    Scheduler --> Queue
```

Only `pulse-api` exists as a runnable deployment role today (this
repository's `Dockerfile`/`docker-compose.yml`). `pulse-worker` and
`pulse-scheduler` are reserved roles (item 67-69) — introduced once there is
a real asynchronous workload to run, not speculatively.

## Data flow (the canonical pipeline)

```mermaid
graph LR
    A[ACQUIRE] --> B[PRESERVE] --> C[NORMALISE] --> D[VALIDATE] --> E[ENRICH]
    E --> F[RESOLVE] --> G[CORRELATE] --> H[DERIVE] --> I[ANALYSE]
    I --> J[SCORE] --> K[EXPLAIN] --> L[PUBLISH] --> M[OBSERVE OUTCOME] --> N[LEARN]
```

This scaffold implements a thin, verifiable slice of this chain (Acquire
via `ReferenceSourceAdapter`, Normalise via `ingestion.pipelines.normalisation`,
and Analyse/Explain via the reference Haystack research pipeline) — the
full chain is not built out (item 113: no premature business code).

## Research / RAG flow

See `docs/adr/ADR-PULSE-010 — Embedding Deepset Haystack as Pulse's Headless AI Orchestration Engine.md`
§"RAG over governed evidence" for the flow diagram and why it is not naive
vector-search RAG.

## Agent/tool security

See `docs/security/agent-and-tool-security.md`.

## API framework decision

See `docs/architecture/api-framework-decision.md`.
