# ADR-PULSE-002 — Canonical Intelligence Domain Model and Aggregate Boundaries

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-002`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:** `ADR-PULSE-001 — Engine Mission, Authority and System Boundary`  
**Decision Type:** Domain Architecture Decision

## Context

`ARCH-PULSE-CIM-001` establishes the semantic vocabulary for Baobab Pulse, including:

```text
Source
DataSource
Dataset
Acquisition
RawRecord
Observation
Evidence
EvidenceSet
Signal
Analysis
Insight
Opportunity
Risk
Forecast
Recommendation
Decision
Outcome
Feedback
Model
IntelligenceProduct
```

The next architectural problem is not merely how these entities relate semantically, but how they should be grouped into **transactional and consistency boundaries**.

Without explicit aggregate boundaries, a physical implementation can easily create one of two failures:

```text
one enormous intelligence object graph
```

or:

```text
dozens of independently mutable records
with no enforceable consistency rules
```

Both are undesirable.

The first creates excessive coupling, locking, persistence complexity and poor scalability.

The second permits invalid states such as:

```text
Recommendation without evidence

Observation without provenance

Forecast without model/method identity

Decision referring to a withdrawn recommendation

Evidence pointing at nonexistent source material
```

Pulse therefore requires clear aggregate roots and invariants before PostgreSQL tables or Python domain objects are designed.

---

# Decision

Baobab Pulse SHALL use a **domain-oriented aggregate model**.

Aggregates SHALL be deliberately small enough to scale independently but large enough to enforce local consistency.

Cross-aggregate consistency SHALL normally be:

```text
reference-based
+
event-driven
+
eventually consistent
```

rather than implemented through one large cross-domain transaction.

The following aggregate roots are adopted:

```text
1. Source
2. Dataset
3. Acquisition
4. Observation
5. EvidenceSet
6. Signal
7. Analysis
8. Insight
9. Opportunity
10. Risk
11. Forecast
12. Recommendation
13. Decision
14. Model
15. IntelligenceProduct
```

`Outcome`, `Feedback`, `RawRecord`, `Evidence`, `DatasetVersion`, `ModelVersion`, and related subordinate entities SHALL belong to or associate with those aggregate boundaries according to the rules below.

---

# 1. Aggregate Design Principles

The aggregate architecture SHALL follow these principles.

## 1.1 Aggregate roots own local invariants

Only an aggregate root may authoritatively change state within its aggregate.

---

## 1.2 Aggregates reference other aggregates by identity

Cross-aggregate relationships SHALL normally use canonical IDs.

Not:

```text
Recommendation
    embeds entire Insight object
```

but:

```text
Recommendation
    references insight_id
```

---

## 1.3 Aggregate boundaries are not API boundaries

A domain aggregate does not imply:

```text
microservice
REST endpoint
database schema
container
```

The initial Pulse implementation SHOULD remain modular rather than decomposing every aggregate into a deployable service.

---

## 1.4 Aggregate boundaries are not report boundaries

Read projections may join many aggregates.

Transactional ownership remains separate.

---

# 2. Source Aggregate

`Source` SHALL be an aggregate root.

It owns the identity and governance profile of an information authority.

Conceptual structure:

```text
Source
 ├── SourceIdentity
 ├── SourceType
 ├── AuthorityProfile
 ├── TrustProfile
 ├── Jurisdiction
 ├── LicenceSummary
 └── Lifecycle
```

A Source does not own its DataSources transactionally.

Instead:

```text
Source
 1 ─────── * DataSource
```

is implemented through identity references.

---

# 3. Source Invariants

The Source aggregate SHALL enforce:

```text
source_id immutable

source name non-empty

source type valid

status valid

trust assessments versioned where material
```

A Source SHALL remain reconstructable even after retirement.

---

# 4. DataSource Ownership

A `DataSource` is logically subordinate to a Source but SHALL be treated as an independently addressable entity within the source-management domain.

This prevents a Source aggregate containing hundreds of endpoints from becoming unnecessarily large.

The implementation MAY therefore use:

```text
Source
```

and:

```text
DataSource
```

as separate aggregate roots if operational scale justifies it.

For the canonical decision in this ADR, they remain part of one **Source Management bounded context**, but not necessarily one transactional object graph.

---

# 5. Dataset Aggregate

`Dataset` SHALL be an aggregate root.

It owns:

```text
Dataset
 ├── metadata
 ├── DatasetVersion[]
 ├── semantic profile
 ├── frequency
 ├── classification
 └── lifecycle
```

A DatasetVersion SHALL not exist independently of a Dataset.

---

# 6. Dataset Versioning Invariant

Each version SHALL have:

```text
dataset_id
version identifier
valid_from
schema/methodology identity
```

where applicable.

Two active DatasetVersions SHALL NOT occupy an invalid overlapping applicability interval where the dataset semantics require uniqueness.

---

# 7. Dataset versus Source Boundary

A Source answers:

> Who or what provides the information?

A DataSource answers:

> Through which channel do we acquire it?

A Dataset answers:

> Which logically coherent information collection are we consuming?

These distinctions SHALL remain explicit.

---

# 8. Acquisition Aggregate

`Acquisition` SHALL be an aggregate root.

It represents one ingestion execution.

It owns:

```text
Acquisition
 ├── mode
 ├── source/dataset reference
 ├── timing
 ├── cursor/checkpoint
 ├── processing counts
 ├── failure state
 ├── retry state
 └── completion state
```

---

# 9. RawRecord Boundary

`RawRecord` SHALL be subordinate to Acquisition for lineage purposes but SHALL NOT require embedding inside the Acquisition aggregate.

A single Acquisition may produce millions of RawRecords.

Therefore:

```text
Acquisition
 1 ─────── * RawRecord
```

is a logical ownership relation, not an in-memory aggregate collection.

RawRecords SHALL be independently persisted and append-oriented.

---

# 10. Acquisition Invariants

An Acquisition SHALL satisfy:

```text
started_at <= completed_at
```

where `completed_at` exists.

Counts SHALL obey:

```text
accepted + rejected <= received
```

unless provider semantics explicitly require a different counting model.

A completed Acquisition SHALL not revert to running.

Retries SHALL create retry state or subsequent attempt records rather than erasing previous failures.

---

# 11. Observation Aggregate

`Observation` SHALL be one of the most important aggregate roots in Pulse.

It represents canonicalised evidence-bearing fact claims.

Its aggregate SHALL contain:

```text
Observation
 ├── subject reference
 ├── indicator/metric
 ├── value
 ├── unit/currency
 ├── temporal context
 ├── market/geography
 ├── classification
 ├── provenance references
 ├── quality references
 └── lifecycle/revision state
```

---

# 12. Observation Immutability

Once published as a canonical Observation, its semantic content SHALL be immutable.

If the source changes the reported value, Pulse SHALL create:

```text
Observation v2
```

and link it through revision or supersession.

It SHALL NOT overwrite:

```text
Observation v1
```

destructively.

---

# 13. Observation Identity

An Observation ID identifies one canonical claim.

It SHALL not be generated solely from:

```text
source value
timestamp
external source ID
```

because corrections and provider quirks may violate uniqueness assumptions.

---

# 14. Observation Lineage

An Observation MAY be derived from:

```text
1 RawRecord
```

or:

```text
many RawRecords
```

and one RawRecord MAY generate many Observations.

Therefore:

```text
RawRecord
 * ─────── * Observation
```

SHALL use explicit provenance relations.

---

# 15. EvidenceSet Aggregate

`EvidenceSet` SHALL be an aggregate root.

This decision is important.

Evidence is not merely a loose join table.

An EvidenceSet represents the bounded collection of evidence assembled for a specific analytical purpose.

Example:

```text
EvidenceSet:
    SA specialty-coffee opportunity assessment
```

may contain:

```text
trade observation
commodity-price observation
FX observation
news article
ERP demand observation
```

---

# 16. EvidenceSet Ownership

The aggregate owns:

```text
EvidenceSet
 ├── purpose
 ├── scope
 ├── EvidenceEntry[]
 ├── created_at
 ├── frozen_at
 └── version
```

Each EvidenceEntry references another canonical object.

---

# 17. EvidenceEntry

`Evidence` SHALL preferably be implemented as an EvidenceEntry subordinate to an EvidenceSet where its semantics are contextual.

For example:

```text
Observation A
```

may:

```text
SUPPORT
```

one analysis while:

```text
CONTRADICT
```

another.

Therefore evidence direction belongs to the relationship, not necessarily the source object.

---

# 18. EvidenceSet Freeze Rule

Once an EvidenceSet has been used to publish consequential intelligence, its historical version SHALL be immutable.

Additional evidence SHALL produce:

```text
EvidenceSet v2
```

or an equivalent versioned extension.

This preserves reproducibility.

---

# 19. EvidenceSet Invariants

Published EvidenceSets SHALL:

```text
contain >= 1 evidence entry

contain no dangling references

record classification

record contextual scope
```

Classification SHALL be at least as restrictive as permitted by its evidence.

---

# 20. Signal Aggregate

`Signal` SHALL be an aggregate root.

It owns:

```text
Signal
 ├── signal type
 ├── subject
 ├── detector identity
 ├── EvidenceSet reference
 ├── severity
 ├── confidence
 ├── temporal validity
 └── lifecycle
```

---

# 21. Signal versus Observation

An Observation says:

```text
USD/ZAR = 18.40
```

A Signal says:

```text
ZAR has depreciated materially over 30 days
```

The distinction SHALL remain enforced in domain semantics.

---

# 22. Trend and Anomaly

`Trend` and `Anomaly` SHALL be Signal specialisations.

The physical implementation SHOULD favour:

```text
Signal
+
signal_type
+
specialised attributes
```

over deep ORM inheritance unless there is compelling benefit.

---

# 23. Signal Invariants

A published Signal SHALL reference:

```text
detection method
evidence
confidence method
subject/context
```

where applicable.

A Signal cannot be:

```text
CONFIRMED
```

before it has been:

```text
DETECTED
```

or otherwise legitimately created by an equivalent workflow.

---

# 24. Analysis Aggregate

`Analysis` SHALL be an aggregate root.

It represents the execution of an analytical method over defined evidence.

It owns:

```text
Analysis
 ├── method
 ├── version
 ├── EvidenceSet reference
 ├── parameters
 ├── ModelVersion reference where applicable
 ├── execution timing
 ├── result metadata
 └── reproducibility profile
```

---

# 25. Analysis and Job Separation

`Analysis` and `IntelligenceJob` SHALL not be synonymous.

An IntelligenceJob represents execution orchestration.

An Analysis represents a domain analytical act.

Example:

```text
IntelligenceJob:
    weekly coffee opportunity scan
```

may produce:

```text
Analysis A
Analysis B
Analysis C
```

---

# 26. Analysis Reproducibility Invariant

A material Analysis SHALL preserve enough metadata to identify:

```text
method
method_version
parameters
input EvidenceSet
model version if any
execution timestamp
```

---

# 27. Insight Aggregate

`Insight` SHALL be an aggregate root.

It owns:

```text
Insight
 ├── statement
 ├── type
 ├── subject
 ├── EvidenceSet reference
 ├── Analysis references
 ├── confidence
 ├── significance
 ├── validity
 └── lifecycle
```

---

# 28. Insight Publication Boundary

Draft Insight generation may be mutable.

Once an Insight becomes:

```text
PUBLISHED
```

its historical semantic content SHALL be immutable.

Changes SHALL produce:

```text
new revision
```

or:

```text
superseding Insight
```

---

# 29. Insight Invariants

A published Insight SHOULD have:

```text
at least one Analysis
```

and SHALL have:

```text
at least one EvidenceSet
```

except where explicitly classified as human-authored opinion or hypothesis.

---

# 30. Opportunity Aggregate

`Opportunity` SHALL be an aggregate root.

An Opportunity has a lifecycle independent of the Insight that produced it.

This is important because:

```text
Insight remains valid
```

while:

```text
Opportunity expires
```

may be perfectly legitimate.

---

# 31. Opportunity Aggregate Contents

```text
Opportunity
 ├── scope
 ├── opportunity type
 ├── Insight references
 ├── EvidenceSet
 ├── estimated value
 ├── feasibility
 ├── urgency
 ├── confidence
 ├── time horizon
 └── lifecycle
```

---

# 32. Opportunity Invariants

An Opportunity SHALL:

```text
reference >= 1 supporting Insight or Analysis
```

unless manually originated.

Any estimated monetary value SHALL preserve:

```text
amount
currency
method
```

---

# 33. Risk Aggregate

`Risk` SHALL be an aggregate root independent of Opportunity.

Risk and Opportunity SHALL NOT be implemented as one generic:

```text
Finding
```

aggregate.

They have materially different lifecycle and assessment semantics.

---

# 34. Risk Aggregate Contents

```text
Risk
 ├── risk type
 ├── Insight references
 ├── EvidenceSet
 ├── likelihood
 ├── impact
 ├── severity
 ├── exposure
 ├── confidence
 ├── horizon
 └── lifecycle
```

---

# 35. Risk Invariants

A Risk assessment SHALL distinguish:

```text
likelihood
impact
confidence
```

These MUST NOT collapse into one unexplained numeric score.

---

# 36. Forecast Aggregate

`Forecast` SHALL be an aggregate root.

It owns the prediction and its evaluation lifecycle.

```text
Forecast
 ├── target
 ├── origin
 ├── horizon
 ├── predicted value
 ├── uncertainty interval
 ├── method/ModelVersion
 ├── EvidenceSet
 ├── evaluation
 └── lifecycle
```

---

# 37. Forecast Evaluation

`ForecastEvaluation` SHOULD remain subordinate to Forecast.

```text
Forecast
 1 ─────── 0..* ForecastEvaluation
```

This keeps predicted and actual performance directly connected.

---

# 38. Forecast Invariants

A Forecast SHALL identify:

```text
forecast_origin
target_time/horizon
method
```

and SHALL NOT be confused with a Scenario.

---

# 39. Recommendation Aggregate

`Recommendation` SHALL be an aggregate root.

It represents an actionable proposal.

It owns:

```text
Recommendation
 ├── action proposal
 ├── rationale
 ├── Insight references
 ├── Opportunity references
 ├── Risk references
 ├── Forecast references
 ├── EvidenceSet
 ├── expected benefit
 ├── expected cost
 ├── confidence
 ├── authority requirement
 └── lifecycle
```

---

# 40. Recommendation Isolation

A Recommendation SHALL not embed mutable copies of upstream intelligence.

It references immutable or versioned upstream objects.

This preserves the state on which the recommendation was based.

---

# 41. Recommendation Invariants

A consequential Recommendation SHALL have:

```text
rationale
evidence
authority requirement
classification
context
```

It SHALL NOT automatically become a Decision.

---

# 42. Decision Aggregate

`Decision` SHALL be an aggregate root.

This aggregate records human or policy authority.

It SHALL contain:

```text
Decision
 ├── Recommendation reference
 ├── decision
 ├── rationale
 ├── actor
 ├── authority reference
 ├── decision timestamp
 ├── Action references
 ├── Outcome[]
 └── lifecycle
```

---

# 43. Decision History

Decision changes SHALL preserve history.

For example:

```text
DEFER
    ↓
later
    ↓
ACCEPT
```

is represented as either:

```text
multiple Decision records
```

or explicit version history.

The prior decision SHALL not disappear.

---

# 44. Action Boundary

Operational `Action` records MAY be subordinate to Decision from Pulse's perspective.

However, the actual business transaction remains owned by the external engine.

Pulse stores only:

```text
action intent
external execution reference
execution status
```

where appropriate.

---

# 45. Outcome Ownership

`Outcome` SHALL be subordinate to the Decision domain.

It records the observed consequence of a decision.

```text
Decision
 1 ─────── * Outcome
```

An Outcome MAY reference external system-of-record evidence.

---

# 46. Feedback Ownership

`Feedback` SHALL normally attach to:

```text
Outcome
Recommendation
Insight
Signal
Forecast
ModelRun
```

depending on feedback type.

Feedback itself does not require a top-level aggregate for the initial architecture.

It SHOULD be a subordinate or append-only domain entity.

---

# 47. Feedback Immutability

Submitted Feedback SHOULD be append-only.

A changed human view should normally create another Feedback entry rather than modifying history.

---

# 48. Model Aggregate

`Model` SHALL be an aggregate root.

It owns:

```text
Model
 ├── identity
 ├── purpose
 ├── ModelVersion[]
 ├── governance state
 └── lifecycle
```

---

# 49. ModelVersion Boundary

`ModelVersion` belongs to exactly one Model.

A version is immutable once approved or used in a consequential analysis.

---

# 50. ModelRun Boundary

`ModelRun` SHALL normally be recorded as an execution entity associated with:

```text
ModelVersion
```

but it does not need to reside inside the entire Model aggregate transactionally.

High-volume ModelRun persistence SHALL remain scalable independently.

---

# 51. IntelligenceProduct Aggregate

`IntelligenceProduct` SHALL be an aggregate root.

It defines reusable intelligence composition.

Examples:

```text
Country Pulse
Commodity Pulse
Opportunity Radar
Risk Radar
Executive Brief
```

---

# 52. IntelligenceProduct Contents

```text
IntelligenceProduct
 ├── product type
 ├── audience
 ├── scope
 ├── data requirements
 ├── analytical configuration
 ├── delivery configuration
 ├── schedule
 └── lifecycle
```

---

# 53. IntelligenceProductRun

`IntelligenceProductRun` SHALL be independently persisted because execution volume may become large.

It references:

```text
product version
inputs
outputs
job
run time
status
```

---

# 54. Aggregate Relationship Overview

```text
Source
   │
   ▼
Dataset
   │
   ▼
Acquisition
   │
   ▼
RawRecord
   │
   ▼
Observation
   │
   ▼
EvidenceSet
   │
   ▼
Signal
   │
   ▼
Analysis
   │
   ▼
Insight
   │
   ├────────────┬──────────────┐
   ▼            ▼              ▼
Opportunity    Risk         Forecast
   │            │              │
   └────────────┴──────┬───────┘
                       ▼
                Recommendation
                       │
                       ▼
                    Decision
                       │
                       ▼
                    Outcome
                       │
                       ▼
                    Feedback
```

This is a derivation flow.

It is NOT one transaction.

---

# 55. Transaction Boundaries

Transactions SHALL generally remain inside one aggregate.

Examples:

```text
create Observation
```

is one transaction.

```text
publish Insight
```

is one transaction.

```text
record Decision
```

is one transaction.

A workflow spanning:

```text
Observation
→ Signal
→ Analysis
→ Insight
→ Recommendation
```

SHALL NOT ordinarily execute as one database transaction.

---

# 56. Cross-Aggregate Workflow

Cross-aggregate workflows SHALL use domain/application orchestration.

Example:

```text
Observation created
      ↓
event
      ↓
Signal detector
      ↓
Signal created
      ↓
event
      ↓
Analysis scheduled
```

---

# 57. Strong versus Eventual Consistency

Strong consistency is REQUIRED for:

```text
aggregate-local invariants
classification
valid state transition
identity uniqueness
revision links
```

Eventual consistency is ACCEPTABLE for:

```text
dashboards
derived signals
search indexes
recommendation feeds
analytics projections
```

---

# 58. Reference Integrity

Cross-aggregate references SHOULD be validated at application boundaries.

Physical foreign keys MAY be used within the Pulse relational database where they do not create undesirable coupling.

Foreign keys SHALL NOT cross engine database boundaries.

---

# 59. External Aggregate References

References to:

```text
CanonicalEntity
Market
Context
EngineInstance
DigitalEstate
```

are external canonical references governed by the Control Plane.

Pulse SHALL store their IDs but SHALL NOT assume ownership.

---

# 60. Deletion Rules

Aggregate deletion SHALL preserve derivation integrity.

If a Source becomes retired:

```text
historical Observations remain
```

If an Insight becomes withdrawn:

```text
historical Recommendations remain
```

If a Model becomes retired:

```text
historical ModelRuns remain
```

---

# 61. Aggregate Lifecycle Principle

Retirement of an aggregate SHALL normally affect future use, not erase historical derivation.

---

# 62. Provenance Independence

Provenance relations SHALL be stored in a way that can survive lifecycle changes to source aggregates.

---

# 63. Aggregate Versioning

The following aggregates SHOULD support explicit semantic version or revision history:

```text
Dataset
Observation
EvidenceSet
Insight
Forecast
Recommendation
Model
IntelligenceProduct
```

Versioning SHALL reflect semantic change, not every technical update timestamp.

---

# 64. Revision versus Lifecycle

Example:

```text
Insight version 1
status = PUBLISHED
```

then later:

```text
Insight version 2
status = PUBLISHED
```

does not mean:

```text
version 1 = DELETED
```

Version 1 becomes superseded while retaining history.

---

# 65. Context Snapshot

Consequential aggregates SHOULD preserve a contextual snapshot or immutable context references sufficient to understand historical scope.

This prevents current Control Plane metadata changes from rewriting historical meaning.

---

# 66. Classification Snapshot

Similarly, a historical Recommendation SHALL retain the classification under which it was issued.

---

# 67. Evidence Snapshot

Recommendations SHALL reference the exact EvidenceSet version used at issuance time.

Not:

```text
latest EvidenceSet
```

---

# 68. Model Snapshot

Analyses and Forecasts SHALL reference the exact ModelVersion used.

---

# 69. Method Snapshot

Deterministic analyses SHALL preserve exact method/version identity even where no ML Model exists.

---

# 70. Source Schema Independence

Source provider schemas SHALL not be aggregate definitions.

Provider-specific structures terminate before canonical aggregate construction.

---

# 71. Domain Events

Each aggregate root MAY emit domain events.

Examples:

```text
SourceRegistered
SourceRetired

DatasetVersionPublished

AcquisitionStarted
AcquisitionCompleted
AcquisitionFailed

ObservationRecorded
ObservationRevised

EvidenceSetFrozen

SignalDetected
SignalResolved

AnalysisCompleted
AnalysisFailed

InsightPublished
InsightSuperseded

OpportunityQualified
RiskMaterialised

ForecastGenerated
ForecastEvaluated

RecommendationPresented
RecommendationAccepted

DecisionRecorded
OutcomeObserved
FeedbackRecorded

ModelVersionApproved
ModelVersionRetired
```

---

# 72. Domain Event Publication

Domain events SHALL describe completed domain facts.

Not:

```text
Please create Insight
```

but:

```text
InsightPublished
```

Commands and events SHALL remain distinct.

---

# 73. Command Model

Commands MAY include:

```text
RecordObservation
FreezeEvidenceSet
DetectSignals
RunAnalysis
PublishInsight
QualifyOpportunity
AssessRisk
GenerateForecast
IssueRecommendation
RecordDecision
RecordOutcome
SubmitFeedback
```

---

# 74. Application Services

Application services SHALL orchestrate commands across aggregates.

Example:

```text
OpportunityDetectionService
```

may:

1. load relevant Insights;
2. validate context;
3. load supporting EvidenceSet IDs;
4. create Opportunity;
5. commit Opportunity;
6. publish `OpportunityDetected`.

It does not acquire ownership of Insight or EvidenceSet.

---

# 75. Domain Services

Pure domain logic that spans entities but requires no independent identity MAY reside in domain services.

Examples:

```text
ConfidenceCalculator
ClassificationResolver
RiskScoringPolicy
OpportunityQualificationPolicy
TemporalValidityPolicy
```

---

# 76. Aggregate Repositories

Persistence interfaces SHOULD correspond to aggregate roots.

Illustrative:

```text
SourceRepository
DatasetRepository
AcquisitionRepository
ObservationRepository
EvidenceSetRepository
SignalRepository
AnalysisRepository
InsightRepository
OpportunityRepository
RiskRepository
ForecastRepository
RecommendationRepository
DecisionRepository
ModelRepository
IntelligenceProductRepository
```

This does not require one physical database table per repository.

---

# 77. Query Repositories

Read-heavy use cases MAY use separate query interfaces:

```text
MarketIntelligenceQuery
RiskFeedQuery
OpportunityQuery
EvidenceTraceQuery
DecisionAuditQuery
```

These may project across aggregate boundaries.

---

# 78. CQRS Position

Pulse MAY use light CQRS patterns where beneficial.

This ADR does NOT mandate a full CQRS architecture.

The guiding principle is:

```text
write models enforce domain rules
read models optimise consumption
```

---

# 79. Event Sourcing Position

Pulse SHALL NOT initially require full event sourcing.

Historical versioning, provenance and an event outbox are sufficient for the initial architecture.

Event sourcing MAY be considered later for a bounded domain if justified.

---

# 80. Aggregate Size Rule

An aggregate SHOULD NOT contain unbounded child collections.

Therefore these patterns are prohibited:

```text
Source containing every historical RawRecord

Dataset containing every Observation

Insight containing every Recommendation

Model containing every ModelRun
```

---

# 81. High-Volume Entity Rule

High-volume entities SHALL be independently persisted even when logically subordinate.

Examples:

```text
RawRecord
Observation
ModelRun
IntelligenceProductRun
Feedback
```

---

# 82. Historical Query Rule

Historical reconstruction SHALL use versioned references and provenance rather than rehydrating one massive domain object graph.

---

# 83. Opportunity and Risk Separation Decision

A tempting alternative is:

```text
Finding
 ├── positive
 └── negative
```

This is rejected.

Opportunity and Risk SHALL remain separate aggregates because they differ in:

```text
qualification
valuation
severity
mitigation
materialisation
lifecycle
decision treatment
```

---

# 84. Signal and Insight Separation Decision

A Signal SHALL NOT be modelled as an Insight subtype.

Reason:

```text
Signal = detected phenomenon

Insight = interpreted significance
```

The semantic distinction is foundational to Pulse.

---

# 85. Observation and Evidence Separation Decision

Observation and Evidence SHALL remain separate.

Reason:

An Observation is a fact claim.

Evidence describes how a referenced item participates in an argument or analysis.

---

# 86. Analysis and Insight Separation Decision

Analysis is execution.

Insight is interpreted domain output.

One Analysis may produce several Insights.

One Insight may synthesize several Analyses.

Thus:

```text
Analysis
 * ─────── * Insight
```

is permitted.

---

# 87. Recommendation and Decision Separation Decision

This separation is mandatory.

Pulse recommends.

An authorised actor decides.

No ORM convenience shall merge the two.

---

# 88. Decision and Outcome Separation Decision

A Decision records intent or authority.

Outcome records observed consequence.

A successful Decision may produce:

```text
unexpected negative Outcome
```

and vice versa.

They must remain distinct.

---

# 89. Aggregate Classification Propagation

When a new aggregate is derived from upstream objects, classification SHALL be resolved before persistence.

Example:

```text
EvidenceSet:
    PUBLIC + CONFIDENTIAL
```

produces:

```text
Insight.classification = CONFIDENTIAL
```

unless authorised policy says otherwise.

---

# 90. Aggregate Tenant Propagation

Tenant/context propagation SHALL also occur during aggregate creation.

Derived aggregates SHALL not be allowed to exist without resolvable tenancy where tenant scope applies.

---

# 91. Cross-Market Aggregates

An Insight MAY span several Markets if explicitly scoped.

Its child Opportunity may narrow to one Market.

This is permitted.

---

# 92. Cross-Tenant Aggregate Prohibition

One Recommendation SHALL NOT ordinarily span mutually isolated tenants.

Separate tenant-scoped Recommendations SHOULD be generated.

---

# 93. Aggregate Ownership and PostgreSQL

The later physical model MAY organise these aggregates into PostgreSQL schemas such as:

```text
source
ingestion
evidence
intelligence
decision
model
```

but this ADR does not yet mandate schema names.

---

# 94. Aggregate Ownership and Python

The later Python package model SHOULD reflect bounded domain areas rather than database tables.

Example:

```text
domain/
    sources/
    ingestion/
    observations/
    evidence/
    signals/
    analysis/
    insights/
    opportunities/
    risks/
    forecasting/
    recommendations/
    decisions/
    models/
    products/
```

---

# 95. Aggregate Ownership and API Design

REST resources MAY expose aggregate roots directly.

However, APIs MAY also expose purpose-built projections.

The public API SHALL not leak persistence implementation.

---

# 96. Aggregate Ownership and Events

Canonical events SHOULD be anchored around aggregate lifecycle changes.

---

# 97. Aggregate Ownership and Testing

Each aggregate SHALL have domain tests covering:

```text
valid construction
invalid construction
state transitions
classification rules
tenant rules
versioning
immutability
```

---

# 98. Cross-Aggregate Contract Tests

Integration tests SHALL validate chains such as:

```text
Observation
→ EvidenceSet
→ Analysis
→ Insight
→ Recommendation
→ Decision
```

without collapsing them into one transaction.

---

# 99. Rejected Alternative — One Intelligence Aggregate

Rejected:

```text
IntelligenceCase
 ├── observations
 ├── evidence
 ├── signals
 ├── analyses
 ├── insights
 ├── risks
 ├── opportunities
 ├── recommendations
 └── decisions
```

Reason:

It would create an enormous transactional boundary and make concurrent analytical processing difficult.

---

# 100. Rejected Alternative — Fully Anemic Record Model

Rejected:

```text
tables with setters
+
application logic everywhere
```

Reason:

Important invariants such as classification propagation, lifecycle transitions and evidence freezing would become inconsistent.

---

# 101. Rejected Alternative — Aggregate-per-Database-Table

Rejected.

Relational table structure is not equivalent to a domain consistency boundary.

---

# 102. Rejected Alternative — Aggregate-per-Microservice

Rejected.

Domain boundaries do not automatically justify network distribution.

---

# 103. Consequences

## Positive

This decision provides:

- clear transactional ownership;
- manageable aggregate size;
- independent scaling of high-volume records;
- strong local invariants;
- historical reproducibility;
- explicit domain semantics;
- clean event-driven workflows;
- straightforward repository boundaries;
- easier unit testing;
- a stable basis for PostgreSQL and Python design.

## Negative

The architecture requires explicit orchestration across aggregates.

Some workflows become eventually consistent rather than immediately visible as one atomic transaction.

Developers must avoid shortcuts such as directly modifying another aggregate's state.

---

# 104. Governing Rules

**AGG-PULSE-001**  
Every mutable domain object SHALL have an identifiable aggregate owner.

**AGG-PULSE-002**  
Aggregate-local invariants SHALL be transactionally enforced.

**AGG-PULSE-003**  
Cross-aggregate relationships SHALL normally use canonical identity references.

**AGG-PULSE-004**  
Cross-aggregate business workflows SHALL not require distributed database transactions.

**AGG-PULSE-005**  
Published historical intelligence SHALL be immutable or versioned.

**AGG-PULSE-006**  
EvidenceSets used for published intelligence SHALL be historically frozen.

**AGG-PULSE-007**  
High-volume subordinate entities SHALL not create unbounded aggregate collections.

**AGG-PULSE-008**  
Observation, Signal, Insight, Recommendation, Decision and Outcome SHALL remain separate semantic and transactional concepts.

**AGG-PULSE-009**  
Opportunity and Risk SHALL remain separate aggregates.

**AGG-PULSE-010**  
Classification and tenancy shall be resolved at aggregate creation.

**AGG-PULSE-011**  
ModelVersion and method identity SHALL be immutable for historical analyses.

**AGG-PULSE-012**  
Read projections SHALL not become canonical write models.

**AGG-PULSE-013**  
Domain boundaries SHALL not be equated with microservice boundaries.

**AGG-PULSE-014**  
Foreign aggregate state SHALL not be mutated directly.

**AGG-PULSE-015**  
Historical references SHALL resolve to the version used at the time, not automatically to the current latest version.

---

# 105. Final Decision Statement

Baobab Pulse SHALL use **explicit domain aggregates with narrow transactional boundaries and versioned cross-aggregate references**.

The architecture is therefore not:

```text
one giant intelligence graph
```

and not:

```text
a bag of independent database rows
```

but:

```text
bounded domain aggregates
        │
        ├── local invariants
        ├── immutable historical versions
        ├── canonical references
        ├── domain events
        └── application orchestration
```

This provides the foundation required to transform:

```text
Source
→ Observation
→ Evidence
→ Signal
→ Analysis
→ Insight
→ Opportunity / Risk / Forecast
→ Recommendation
→ Decision
→ Outcome
→ Feedback
```

without sacrificing scalability, provenance, auditability or domain ownership.