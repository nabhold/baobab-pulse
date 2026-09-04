# ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-006`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:** `ADR-PULSE-001` through `ADR-PULSE-005`  
**Decision Type:** Provenance, Lineage, Evidence Relationship and Impact Analysis Architecture Decision

---

# 1. Context

Baobab Pulse is intended to produce intelligence that may influence:

```text
market entry
procurement
trade
investment
pricing
sourcing
risk management
regulatory response
commercial strategy
```

The credibility of that intelligence depends not only on storing evidence, but on being able to explain how intelligence was derived.

A commercially serious system must answer questions such as:

```text
Where did this number come from?

Which source record produced this observation?

Which transformation changed it?

Which mappings were used?

Which observations supported this analysis?

Which analyses generated this insight?

Which claims depend on this source?

Which reports used this methodology?

Which recommendations relied on this forecast?

Which reports are affected if this source is corrected?
```

These are not ordinary logging questions.

They require a persistent graph of:

```text
evidence
derivation
dependence
support
contradiction
revision
supersession
publication
```

relationships.

`ADR-PULSE-004` established that Pulse must preserve raw evidence and research snapshots.

`ADR-PULSE-005` established canonical observations and domain-specific evidence profiles.

This ADR defines how those objects SHALL be linked into a navigable **Evidence and Lineage Graph**.

---

# 2. Decision

Baobab Pulse SHALL implement provenance and lineage as explicit first-class domain relationships.

Pulse SHALL maintain a logical **Evidence Graph** connecting:

```text
Source
   ↓
DataSource
   ↓
Dataset
   ↓
DatasetVersion
   ↓
Acquisition
   ↓
SourceArtefact
   ↓
RawRecord
   ↓
NormalisedRecord
   ↓
Observation
   ↓
EvidenceEntry
   ↓
EvidenceSet
   ↓
Analysis
   ↓
Signal / Insight
   ↓
Opportunity / Risk / Forecast
   ↓
Recommendation
   ↓
Decision
   ↓
Outcome
   ↓
IntelligenceProduct / Claim / Publication
```

The graph SHALL support traversal:

```text
forward
```

for derivation,

and:

```text
backward
```

for explanation and impact analysis.

The graph is a semantic architecture.

A dedicated graph database SHALL NOT be required initially.

---

# 3. Provenance Principle

Every material intelligence object SHALL be capable of answering:

> **What did I derive from?**

---

# 4. Lineage Principle

Every material evidence object SHALL be capable of answering:

> **What was derived from me?**

These two perspectives are complementary.

---

# 5. Provenance versus Lineage

Pulse SHALL distinguish the concepts.

**Provenance** describes the origin and derivation history of an object.

**Lineage** describes the chain of dependencies between objects across processing and analytical stages.

Example:

```text
Observation provenance:
    RawRecord
    SourceArtefact
    Dataset
    Source

Observation lineage:
    Observation
      → EvidenceSet
      → Analysis
      → Insight
      → Recommendation
      → Report
```

---

# 6. Evidence Graph

The Evidence Graph SHALL represent canonical relationships between evidence-bearing and intelligence-bearing objects.

Conceptually:

```text
                           SOURCE
                             │
                             ▼
                         DATASET
                             │
                             ▼
                        ACQUISITION
                             │
                             ▼
                     SOURCE ARTEFACT
                             │
                             ▼
                         RAW RECORD
                             │
                             ▼
                        OBSERVATION
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
         SUPPORTS       CONTRADICTS      CONTEXTUALISES
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                         EVIDENCE SET
                             │
                             ▼
                           ANALYSIS
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
              SIGNAL       INSIGHT      FORECAST
                │            │            │
                └────────────┼────────────┘
                             ▼
                      OPPORTUNITY / RISK
                             │
                             ▼
                        RECOMMENDATION
                             │
                             ▼
                           DECISION
                             │
                             ▼
                           OUTCOME
```

---

# 7. The Graph Is Directed

Derivation relationships SHALL normally be directed.

Example:

```text
Observation A
    DERIVED_FROM
RawRecord B
```

not merely:

```text
A related_to B
```

Direction is essential for lineage traversal.

---

# 8. Relationship Semantics

Pulse SHALL use explicit relationship types.

Generic:

```text
RELATED_TO
```

SHALL not be sufficient for important lineage.

---

# 9. Canonical Relationship Families

The initial relationship families SHALL include:

```text
DERIVATION
EVIDENCE
REVISION
IDENTITY
PUBLICATION
DECISION
EXECUTION
QUALITY
CONTEXT
```

---

# 10. Derivation Relationships

Examples:

```text
DERIVED_FROM
GENERATED_FROM
TRANSFORMED_FROM
AGGREGATED_FROM
CALCULATED_FROM
EXTRACTED_FROM
NORMALISED_FROM
MODELLED_FROM
SUMMARISED_FROM
```

---

# 11. Evidence Relationships

Examples:

```text
SUPPORTS
CONTRADICTS
CONTEXTUALISES
CORROBORATES
WEAKENS
QUALIFIES
```

These describe argumentative or analytical relationships.

---

# 12. Revision Relationships

Examples:

```text
SUPERSEDES
REVISES
CORRECTS
RETRACTS
REPLACES
```

---

# 13. Identity Relationships

Examples:

```text
REFERS_TO
MAPS_TO
POSSIBLY_REFERS_TO
ALIAS_OF
```

Identity authority remains governed by the Control Plane where applicable.

---

# 14. Publication Relationships

Examples:

```text
CITED_BY
USED_IN
PUBLISHED_AS
SUMMARISED_IN
```

---

# 15. Decision Relationships

Examples:

```text
INFORMS
RECOMMENDS
ACCEPTED_BY
REJECTED_BY
MODIFIED_BY
```

---

# 16. Execution Relationships

Examples:

```text
EXECUTED_BY
PRODUCED_BY_JOB
PRODUCED_BY_MODEL_RUN
PRODUCED_BY_METHOD
```

---

# 17. Quality Relationships

Examples:

```text
VALIDATED_BY
REVIEWED_BY
FLAGGED_BY
QUARANTINED_BY
```

---

# 18. Context Relationships

Examples:

```text
APPLIES_TO
OBSERVED_IN
AFFECTS
LOCATED_IN
PARTICIPATES_IN
```

---

# 19. Relationship Record

Every material graph edge SHALL itself be a first-class record.

Conceptually:

```text
LineageEdge
 ├── edge_id
 ├── edge_type
 ├── source_object_type
 ├── source_object_id
 ├── target_object_type
 ├── target_object_id
 ├── valid_time
 ├── recorded_at
 ├── actor
 ├── transformation_reference
 ├── confidence
 ├── classification
 ├── tenant_scope
 ├── metadata
 └── status
```

---

# 20. Relationship Identity

A LineageEdge SHALL have its own canonical identity.

This permits:

```text
versioning
auditing
correction
confidence
classification
```

of the relationship itself.

---

# 21. Edge Immutability

Material lineage edges SHALL normally be immutable once recorded.

Corrections SHALL supersede or invalidate prior edges.

They SHALL not silently rewrite history.

---

# 22. Edge Direction

Every lineage relationship SHALL define its canonical direction.

Example:

```text
Analysis
    DERIVED_FROM
EvidenceSet
```

not the reverse.

Reverse traversal is a query concern.

---

# 23. Symmetric Relationships

Some relationships may be conceptually symmetric.

Example:

```text
CORROBORATES
```

The canonical representation SHALL still define storage direction or paired semantics consistently.

---

# 24. Edge Confidence

Not all relationships are equally certain.

Examples:

```text
exact derivation
confirmed mapping
probabilistic entity relationship
machine-extracted claim relationship
```

Therefore LineageEdge MAY carry confidence.

---

# 25. Deterministic Provenance

Direct processing relationships SHOULD carry deterministic lineage.

Example:

```text
Observation O
DERIVED_FROM
RawRecord R
```

is usually certain.

---

# 26. Probabilistic Relationship

A relationship such as:

```text
NewsArticle
POSSIBLY_REFERS_TO
Company X
```

may be probabilistic.

It SHALL never be upgraded silently to:

```text
REFERS_TO
```

without resolution.

---

# 27. Evidence Direction

Evidence relationships SHALL preserve:

```text
SUPPORTS
CONTRADICTS
NEUTRAL
CONTEXTUAL
```

consistent with the canonical intelligence model.

---

# 28. Evidence Weight

An EvidenceEntry MAY assign analytical weight to evidence within one EvidenceSet.

The weight SHALL belong to the analytical context.

It SHALL not permanently alter the source observation.

---

# 29. Evidence Reuse

One Observation MAY support multiple EvidenceSets.

Example:

```text
TradeObservation A
    ├── supports Market Entry Study
    ├── supports Supplier Report
    └── supports Country Pulse
```

Each relationship may carry different analytical relevance.

---

# 30. EvidenceSet as Argument Boundary

An EvidenceSet SHALL act as the principal grouping boundary between raw/canonical evidence and a specific analytical purpose.

---

# 31. Evidence Graph Is Not Merely Data Lineage

Pulse lineage extends beyond ETL.

It includes:

```text
source lineage
data lineage
analytical lineage
claim lineage
recommendation lineage
decision lineage
publication lineage
```

---

# 32. Source Lineage

Source lineage SHALL answer:

```text
Which provider?
Which dataset?
Which version?
Which acquisition?
Which artefact?
```

---

# 33. Data Lineage

Data lineage SHALL answer:

```text
Which record?
Which parser?
Which mapping?
Which transformation?
Which observation?
```

---

# 34. Analytical Lineage

Analytical lineage SHALL answer:

```text
Which EvidenceSet?
Which method?
Which model?
Which parameters?
Which resulting analysis?
```

---

# 35. Claim Lineage

Claim lineage SHALL answer:

```text
Which analysis supports this claim?
Which evidence supports it?
Which evidence contradicts it?
```

---

# 36. Recommendation Lineage

Recommendation lineage SHALL answer:

```text
Which insights?
Which risks?
Which forecasts?
Which opportunities?
Which evidence?
```

---

# 37. Decision Lineage

Decision lineage SHALL answer:

```text
Which recommendation?
Who decided?
What rationale?
Which assumptions?
```

---

# 38. Outcome Lineage

Outcome lineage SHALL connect actual observed consequences back to:

```text
decision
recommendation
forecast
method
```

enabling feedback and evaluation.

---

# 39. Publication Lineage

Publication lineage SHALL connect:

```text
report
section
claim
chart
table
citation
```

to the underlying intelligence graph.

---

# 40. Claim-to-Evidence Rule

Every material published Claim SHALL resolve through at least one valid evidence path.

Conceptually:

```text
Claim
 ↓
Analysis
 ↓
EvidenceSet
 ↓
Evidence
 ↓
Observation
 ↓
Source
```

---

# 41. Narrative Is Not Exempt

A claim appearing only in prose SHALL still require evidence lineage if it is materially factual or analytical.

---

# 42. Chart Lineage

Charts SHALL be treated as publication artefacts with lineage.

Example:

```text
Chart
 ↓
AnalyticalDataset
 ↓
Observations
 ↓
Sources
```

---

# 43. Table Lineage

Published tables SHOULD similarly retain source relationships.

---

# 44. Citation Manifest Relationship

The CitationManifest defined previously SHALL be generated from the Evidence Graph.

It SHALL not exist as an unrelated manually maintained list.

---

# 45. Provenance Query

Pulse SHALL support the conceptual operation:

```text
TRACE_UPSTREAM(object_id)
```

to answer:

> What caused this object to exist?

---

# 46. Lineage Query

Pulse SHALL support:

```text
TRACE_DOWNSTREAM(object_id)
```

to answer:

> What depends on this object?

---

# 47. Bounded Traversal

Traversal SHALL support:

```text
depth
relationship type
time
tenant
classification
domain
```

filters.

---

# 48. Full Graph Traversal Is Not Always Safe

Cross-tenant graph traversal SHALL be policy constrained.

Knowledge of an edge may itself reveal confidential information.

---

# 49. Classification Propagation

Lineage edges SHALL carry or resolve classification sufficient to prevent graph traversal from bypassing evidence security.

---

# 50. Tenant Propagation

A downstream confidential object SHALL not become discoverable merely because an upstream public source is discoverable.

---

# 51. Reverse Leakage

Consider:

```text
Public News Article
      ↓
used in
Confidential Acquisition Study
```

A user authorised to see the public article SHALL NOT automatically learn that the confidential study exists.

---

# 52. Traversal Policy

Every graph traversal SHALL evaluate authorisation for both:

```text
nodes
edges
```

---

# 53. Provenance Views

Pulse SHOULD provide multiple views:

```text
INTERNAL_FULL
ANALYST
CLIENT
PUBLICATION
AUDIT
```

with different disclosure levels.

---

# 54. Public Provenance

Public provenance may expose:

```text
source
dataset
publication date
methodology
citation
```

without exposing:

```text
private analyst notes
tenant data
internal model configuration
restricted sources
```

---

# 55. Client Provenance

A client view MAY expose deeper evidence lineage for the client's own intelligence products.

---

# 56. Audit Provenance

Audit users MAY receive broader visibility subject to legal and security policy.

---

# 57. Impact Analysis

One of the most important capabilities of the graph SHALL be downstream impact analysis.

Example:

```text
Source correction
     ↓
affected RawRecords
     ↓
affected Observations
     ↓
affected EvidenceSets
     ↓
affected Analyses
     ↓
affected Claims
     ↓
affected Reports
```

---

# 58. Impact Query

Pulse SHALL support:

```text
FIND_DEPENDENTS(object_id)
```

with materiality filters.

---

# 59. Revision Impact

When an Observation is revised, Pulse SHALL be capable of identifying every downstream object derived from the superseded version.

---

# 60. Mapping Impact

When a canonical mapping changes:

```text
provider entity
→ canonical entity
```

Pulse SHALL identify downstream observations and intelligence that used the old mapping.

---

# 61. Methodology Impact

If a MethodVersion is found defective, Pulse SHALL identify:

```text
analyses
forecasts
scores
claims
reports
recommendations
```

that depended on it.

---

# 62. Model Impact

If a ModelVersion is withdrawn, Pulse SHALL identify all outputs created from that model.

---

# 63. Source Retraction Impact

If a source publication is retracted, Pulse SHALL locate all affected claims and products.

---

# 64. Licence Impact

If source rights change, lineage SHALL permit identification of all publications or products using that source.

---

# 65. Classification Impact

If evidence classification is upgraded:

```text
TENANT
→ CONFIDENTIAL
```

Pulse SHALL identify affected downstream intelligence and exposure paths.

---

# 66. Impact Does Not Equal Automatic Invalidity

A dependency change SHALL create an impact candidate.

It SHALL not automatically imply every downstream conclusion is invalid.

---

# 67. Impact Classification

Impacts SHOULD be classified:

```text
INFORMATIONAL
LOW
MODERATE
MATERIAL
CRITICAL
```

according to policy or methodology.

---

# 68. ResearchInvalidationCandidate

Material lineage changes MAY create:

```text
ResearchInvalidationCandidate
```

containing:

```text
cause
affected objects
materiality
recommended review
```

---

# 69. Reassessment Workflow

Conceptually:

```text
UPSTREAM CHANGE
      ↓
LINEAGE TRAVERSAL
      ↓
IMPACT SET
      ↓
MATERIALITY ASSESSMENT
      ↓
NO ACTION
or
REASSESSMENT_REQUIRED
      ↓
ANALYST REVIEW
      ↓
REVISE / RETAIN / RETRACT
```

---

# 70. Living Intelligence Dependency Monitoring

Recurring IntelligenceProducts SHALL register important dependencies.

---

# 71. Dependency Watch

A product MAY subscribe to changes affecting:

```text
datasets
metrics
commodities
countries
companies
regulations
methodologies
```

---

# 72. Dependency Trigger

Example:

```text
TariffObservation revised
     ↓
affected LandedCostAnalysis
     ↓
affected Opportunity
     ↓
client alert candidate
```

---

# 73. Assumption Lineage

Pulse SHOULD support lineage for analytical assumptions.

Example:

```text
Assumption:
freight cost remains below X
```

may depend on:

```text
freight observations
FX
fuel prices
```

---

# 74. Decision Assumption Graph

A high-value advisory Decision MAY therefore be connected:

```text
Decision
   ↓
Recommendation
   ↓
Assumptions
   ↓
Evidence
```

---

# 75. Assumption Monitoring

If evidence undermines an assumption:

```text
AssumptionStatus
    VALID
→
AT_RISK
```

may be generated.

---

# 76. Commercial Value

This enables a potentially high-value service:

> **Monitor whether the assumptions supporting a client's strategic decision remain valid.**

---

# 77. Relationship Temporal Semantics

Lineage edges MAY have:

```text
valid_from
valid_to
recorded_at
superseded_at
```

where the relationship changes over time.

---

# 78. Relationship History

Historical graph state SHALL remain reconstructable where material.

---

# 79. Bitemporal Lineage

Where justified, Pulse MAY track:

```text
relationship validity
```

and:

```text
system knowledge time
```

separately.

---

# 80. Historical Graph Query

Pulse SHOULD eventually support:

> Show the evidence graph as it was known on 1 June 2026.

---

# 81. Research Snapshot Relationship

A ResearchSnapshot SHALL freeze references to specific graph nodes and edges.

---

# 82. Snapshot Is Not Graph Copy

Pulse SHOULD NOT duplicate the entire Evidence Graph for every report.

The snapshot references immutable/versioned graph identities.

---

# 83. Snapshot Manifest

A ResearchSnapshot SHOULD contain or derive a manifest of:

```text
node IDs
edge IDs
method versions
model versions
source vintages
```

needed for reproduction.

---

# 84. Graph Integrity

The lineage graph SHALL enforce referential integrity where practical.

A lineage edge SHALL not point to a nonexistent canonical node without an explicit external-reference state.

---

# 85. External Node

Some sources may not be fully stored due to licensing.

Pulse MAY maintain:

```text
ExternalEvidenceReference
```

as a graph node representing the unavailable external artefact.

---

# 86. Tombstone Nodes

When evidence is legally deleted, a tombstone MAY remain so downstream lineage does not become unintelligible.

---

# 87. Tombstone Semantics

A tombstone SHALL indicate:

```text
object once existed
current content unavailable
reason
date
```

where lawful.

---

# 88. No Dangling Silent Edges

Deletion SHALL not create unexplained lineage gaps.

---

# 89. Transformation Nodes

Transformations SHOULD be represented explicitly where analytically material.

Example:

```text
Observation B
    ↑
UnitConversion v2
    ↑
Observation A
```

---

# 90. Minor Technical Operations

Not every low-level technical operation requires a graph node.

Example:

```text
gzip decompression
```

may remain acquisition metadata unless material to interpretation.

---

# 91. Materiality Rule

Transformation lineage SHALL capture operations that materially affect:

```text
meaning
value
identity
classification
selection
aggregation
interpretation
```

---

# 92. Parser Lineage

Provider parser/version SHALL be recorded for canonical data derived from structured sources.

---

# 93. Mapping Lineage

Every material canonical mapping SHOULD appear in lineage.

---

# 94. Unit Conversion Lineage

Unit conversion SHALL identify:

```text
original value
target value
conversion method
```

---

# 95. Currency Conversion Lineage

Currency-converted values SHALL reference the FX Observation used.

Example:

```text
ConvertedCost
   ├── source price
   └── FX Observation
```

---

# 96. Inflation Adjustment Lineage

Real-value conversions SHALL reference:

```text
nominal value
price index
base period
method
```

---

# 97. Geospatial Derivation Lineage

Spatial analysis SHALL reference:

```text
geometry datasets
distance/route method
coordinate transformation
```

where material.

---

# 98. Entity Resolution Lineage

Confirmed entity mappings SHALL record the evidence or authority supporting resolution.

---

# 99. Probabilistic Resolution Lineage

Probabilistic resolution SHALL preserve:

```text
candidates
features
scores
method
```

where relevant.

---

# 100. Human Resolution

Human-confirmed mappings SHALL preserve:

```text
reviewer
reason
timestamp
```

---

# 101. News Event Lineage

An extracted event SHALL link to every contributing article.

---

# 102. Article Clustering Lineage

An EventCluster SHALL preserve cluster membership and clustering-method version.

---

# 103. Regulatory Lineage

A RegulatoryChange SHOULD connect:

```text
prior instrument
new instrument
amendment
affected provisions
```

where available.

---

# 104. Forecast Lineage

Every Forecast SHALL reference:

```text
EvidenceSet
method/model
parameters
forecast origin
```

---

# 105. Forecast Evaluation Lineage

A ForecastEvaluation SHALL connect:

```text
Forecast
    ↔
Actual Observation
```

---

# 106. Opportunity Lineage

A qualified Opportunity SHALL expose its supporting:

```text
Insights
Analyses
EvidenceSets
```

---

# 107. Risk Lineage

A Risk SHALL expose:

```text
risk indicators
evidence
method
assumptions
```

---

# 108. Recommendation Lineage

A Recommendation SHALL preserve the exact versions of:

```text
Insight
Opportunity
Risk
Forecast
EvidenceSet
```

used when the recommendation was issued.

---

# 109. Recommendation Freeze

A historical Recommendation SHALL not silently rebind to newer Insights.

---

# 110. Decision Lineage

A Decision SHALL reference the exact Recommendation version considered.

---

# 111. Modified Decisions

Where a human modifies a Recommendation, the Decision SHALL capture:

```text
original recommendation
modified decision
rationale
```

rather than rewriting the Recommendation.

---

# 112. Outcome Lineage

Outcome SHALL connect observed consequences to the Decision and relevant operational evidence.

---

# 113. Learning Lineage

Feedback SHALL be capable of tracing backward to:

```text
Outcome
Decision
Recommendation
Insight
Analysis
Method
Evidence
```

---

# 114. Method Performance

This enables Pulse to evaluate:

```text
which methodologies
produce useful recommendations
under which contexts
```

---

# 115. Source Performance

Likewise, Pulse can eventually assess whether particular source combinations correlate with better intelligence outcomes.

---

# 116. Evidence Contribution

Future methodology MAY estimate relative evidence contribution.

Such attribution SHALL be treated as analytical output, not objective fact.

---

# 117. Explanation Query

Pulse SHALL support conceptual queries such as:

```text
EXPLAIN(recommendation_id)
```

returning:

```text
recommendation
rationale
supporting insights
risks
forecasts
evidence
sources
confidence
assumptions
```

subject to access policy.

---

# 118. "Why?" Traversal

The system SHOULD support repeated why-navigation:

```text
Why this recommendation?
    ↓
Because of Insight A

Why Insight A?
    ↓
Because of Analysis B

Why Analysis B?
    ↓
Because of EvidenceSet C

Why EvidenceSet C?
    ↓
Because of Observations D, E, F
```

---

# 119. "What If?" Traversal

Pulse SHOULD also support:

```text
What if Observation D is wrong?
```

by finding all downstream dependencies.

---

# 120. Confidence Dependency

Confidence SHOULD be traceable to:

```text
evidence quality
method confidence
model confidence
analyst assessment
```

where the methodology supports it.

---

# 121. Confidence Is Not Inherited Blindly

A high-confidence Observation does not automatically produce a high-confidence Recommendation.

---

# 122. Contradiction Graph

Contradictory evidence SHALL remain explicit.

Example:

```text
Evidence A ─── SUPPORTS ───► Claim X

Evidence B ─ CONTRADICTS ──► Claim X
```

---

# 123. Contradiction Resolution

If an analyst resolves a contradiction, the reasoning SHALL be attributable.

---

# 124. Unresolved Contradiction

A Claim MAY be published with unresolved contradiction if product policy permits and limitations disclose it.

---

# 125. Evidence Independence

The graph SHOULD record known evidence dependence.

Example:

```text
News B
REPUBLISHES
News A
```

This avoids falsely counting dependent evidence as independent corroboration.

---

# 126. Source Derivation

International datasets may themselves derive from national statistics.

Where known, Pulse SHOULD preserve:

```text
DERIVES_FROM
```

relationships between sources.

---

# 127. Corroboration Quality

Ten sources ultimately deriving from one original source do not equal ten independent confirmations.

---

# 128. Evidence Network

This source-dependency information SHALL support more sophisticated corroboration assessment.

---

# 129. Evidence Diversity

Methodologies MAY assess:

```text
source diversity
source independence
domain diversity
```

as part of evidence quality.

---

# 130. Provenance Service

Pulse SHALL expose a dedicated logical `ProvenanceService`.

Responsibilities:

```text
record lineage
validate edges
trace upstream
trace downstream
resolve graph paths
produce citation paths
support impact analysis
```

---

# 131. EvidenceGraphService

A logical `EvidenceGraphService` MAY provide higher-level graph operations.

It SHALL not necessarily be a separately deployed microservice.

---

# 132. Lineage Repository

Persistence SHALL expose lineage-specific repository abstractions.

A generic CRUD repository SHALL not substitute for lineage semantics.

---

# 133. Example Interfaces

Conceptually:

```text
record_edge()
supersede_edge()
get_upstream()
get_downstream()
find_paths()
find_dependents()
find_supporting_evidence()
find_contradicting_evidence()
```

Exact Python contracts are deferred.

---

# 134. Path Query

Pulse SHALL support bounded path queries such as:

```text
Claim
→ EvidenceSet
→ Observation
→ Source
```

without requiring callers to know physical storage layout.

---

# 135. Shortest Path

Certain analytical interfaces MAY support shortest lineage path.

---

# 136. All Paths

Audit operations MAY require all relevant lineage paths.

---

# 137. Path Explosion

The implementation SHALL protect against uncontrolled graph traversal.

Controls MAY include:

```text
maximum depth
node count
time bounds
relationship filters
```

---

# 138. High-Volume Lineage

Observation-level lineage may become very large.

The architecture SHALL permit:

```text
fine-grained lineage
```

where important,

and:

```text
batch lineage
```

for high-volume transformations where individual-edge storage is impractical.

---

# 139. Batch Lineage

Example:

```text
DatasetPartition A
    ↓ transformed_by
TransformationRun X
    ↓ produced
ObservationPartition B
```

with finer record-level traceability available through deterministic keys where necessary.

---

# 140. Lineage Granularity Policy

Each pipeline SHALL define appropriate lineage granularity.

---

# 141. Commercial Research Requires Fine Lineage

Claims appearing in high-value reports SHOULD generally have finer evidence lineage than low-risk bulk analytical aggregates.

---

# 142. Materiality-Based Lineage

Pulse SHALL invest detailed lineage where the commercial, legal or analytical value warrants it.

---

# 143. Graph Persistence

Initial graph persistence MAY use PostgreSQL.

Possible implementation techniques MAY include:

```text
edge tables
recursive CTEs
indexed adjacency relationships
materialised dependency projections
```

The physical design is deferred.

---

# 144. Graph Database Position

A dedicated graph database SHALL NOT be required initially.

---

# 145. Conditions for Graph Database Adoption

A graph database MAY be introduced if measured workloads demonstrate material need for:

```text
deep traversals
high path-query frequency
complex network analysis
large relationship volumes
```

that PostgreSQL cannot economically satisfy.

---

# 146. Canonical Graph Remains Technology Independent

If storage technology changes, canonical lineage semantics SHALL remain stable.

---

# 147. Search Index Position

Search engines MAY index graph-associated metadata.

Search indexes SHALL not become provenance authority.

---

# 148. Vector Database Position

Vector stores MAY reference canonical evidence nodes.

They SHALL not replace lineage.

---

# 149. Knowledge Graph Position

Pulse MAY eventually expose portions of the Evidence Graph as a broader knowledge graph.

This ADR does not require RDF, OWL or a dedicated semantic-web stack.

---

# 150. Ontology Evolution

If formal ontology tooling is later introduced, it SHALL map to the canonical semantics rather than replace them without migration.

---

# 151. Event Publication

Material lineage changes MAY produce events.

Examples:

```text
pulse.lineage.edge.created
pulse.lineage.edge.superseded
pulse.research.impact.detected
pulse.evidence.invalidated
```

Canonical event contracts belong in `nabhold/shared`.

---

# 152. Outbox Rule

Lineage-related state changes requiring publication SHALL use the transactional outbox pattern where appropriate.

---

# 153. Idempotency

Recording the same deterministic lineage relationship twice SHALL not produce logically duplicated lineage.

---

# 154. Corroboration Exception

Idempotency SHALL not collapse genuinely independent evidence relationships.

---

# 155. Eventual Consistency

Downstream lineage projections MAY be eventually consistent.

Core local lineage required for aggregate correctness SHOULD commit consistently with the relevant aggregate state.

---

# 156. Cross-Aggregate Lineage

Cross-aggregate lineage does not require distributed transactions.

---

# 157. Publication Atomicity

When publishing a consequential IntelligenceProduct, the system SHALL ensure its ResearchSnapshot references a complete and coherent lineage set.

---

# 158. Provenance Completeness

Pulse SHOULD assess whether required provenance is complete before publication.

---

# 159. Broken Lineage

A material object with missing required provenance SHALL enter:

```text
LINEAGE_INCOMPLETE
```

or equivalent status.

---

# 160. Publication Gate

Product policy MAY block publication for unresolved material lineage gaps.

---

# 161. Manual Provenance Repair

Authorised users MAY repair missing lineage.

Such repair SHALL itself be audited.

---

# 162. No Invented Lineage

If origin is unknown, Pulse SHALL record:

```text
UNKNOWN
```

rather than constructing a plausible but false provenance path.

---

# 163. Imported Historical Data

Legacy datasets lacking complete provenance MAY be imported with explicit provenance quality.

---

# 164. Provenance Quality

Pulse MAY classify provenance:

```text
COMPLETE
SUBSTANTIAL
PARTIAL
WEAK
UNKNOWN
```

according to defined criteria.

---

# 165. Provenance Quality Is Not Evidence Quality

A perfectly traceable source may still be low quality.

A high-quality historical dataset may have incomplete provenance.

These dimensions remain distinct.

---

# 166. Audit Relationship

The provenance system SHALL integrate with audit metadata without merging the two abstractions.

---

# 167. Actor Provenance

Lineage may identify:

```text
SYSTEM
HUMAN
MODEL
EXTERNAL_SOURCE
BAOBAB_ENGINE
```

as contributing actors.

---

# 168. Human Contribution

Human-authored transformations or analytical judgments SHALL be attributable where material.

---

# 169. Model Contribution

Model-generated outputs SHALL link to ModelRun.

---

# 170. Agent Contribution

Agentic workflows SHALL preserve:

```text
agent identity
tool call/result references
evidence used
resulting artefact
```

where consequential.

---

# 171. Agent Is Not Evidence

An agent's reasoning step is not independent evidence.

Its output derives from the evidence it used.

---

# 172. Tool Output Provenance

If an agent retrieves a source using a tool, the resulting acquired evidence SHALL enter the canonical acquisition pipeline before becoming publishable evidence.

---

# 173. External Calculation Provenance

If an external analytical service returns a calculation, Pulse SHALL retain:

```text
service
version
inputs
output
time
```

where material.

---

# 174. Human Review Relationship

Published Claims MAY carry:

```text
REVIEWED_BY
APPROVED_BY
```

edges.

---

# 175. Review Does Not Change Evidence

Reviewer approval does not make evidence objectively true.

It records governance.

---

# 176. Editorial Relationship

Publication objects MAY retain:

```text
EDITED_BY
APPROVED_FOR_PUBLICATION_BY
```

relationships.

---

# 177. Research Team Attribution

A report MAY therefore expose its research team internally without embedding authorship into every source object.

---

# 178. Legal Review

Rights-sensitive products MAY include:

```text
RIGHTS_REVIEWED_BY
```

relationship.

---

# 179. Methodology Review

High-assurance methods MAY have:

```text
VALIDATED_BY
APPROVED_BY
```

governance relationships.

---

# 180. Evidence Graph and Commercial Due Diligence

A premium diligence product MAY permit clients to drill down:

```text
Conclusion
    ↓
Claim
    ↓
Evidence
    ↓
Original Source
```

This can materially increase client confidence.

---

# 181. Research Transparency Levels

Products MAY expose varying transparency:

```text
SUMMARY
CITED
EVIDENCE_TRACEABLE
AUDIT_PACKAGE
```

depending on commercial tier.

---

# 182. Transparency Is Product Capability

This allows Nabhold to differentiate products not only by analytical depth but also by evidence transparency.

---

# 183. Evidence Graph Reuse

Once the graph exists, it supports:

```text
research
reporting
auditing
impact analysis
search
recommendation explanation
model evaluation
client transparency
```

from one canonical relationship infrastructure.

---

# 184. Opportunity Graph

The Evidence Graph can support higher-order opportunity relationships.

Example:

```text
Country
   │
imports
   ▼
Commodity
   │
supplied_by
   ▼
Origin
   │
affected_by
   ▼
Weather
   │
affects
   ▼
Supply Risk
```

---

# 185. Opportunity Graph Is Derived

Higher-order commercial graphs SHALL be derived from canonical evidence.

They SHALL not bypass source lineage.

---

# 186. Research Navigation

Analysts SHOULD eventually be able to navigate intelligence visually:

```text
Source
→ Evidence
→ Insight
→ Opportunity
→ Recommendation
```

and backwards.

---

# 187. Visualisation Is Projection

Graph visualisation SHALL remain a projection of canonical lineage.

---

# 188. Evidence Cluster

Pulse MAY identify clusters of related evidence.

These clusters SHALL not erase individual provenance.

---

# 189. Cross-Sector Discovery

The graph MAY eventually enable questions such as:

> Which sectors are jointly affected by rising fertiliser prices and currency depreciation?

This is one path toward the broader cross-sector intelligence ambition.

---

# 190. Weak-Signal Graph

Weak signals from unrelated domains MAY converge.

Example:

```text
new company registrations
+
rising imports
+
public infrastructure spending
+
regulatory change
```

may collectively support an emerging OpportunityCandidate.

---

# 191. Convergence Is Derived Evidence

The convergence itself SHALL be represented as analytical output with lineage to all constituent signals.

---

# 192. Causation Rule

Graph connectivity SHALL NOT imply causation.

```text
CONNECTED_TO
```

or:

```text
CORRELATED_WITH
```

must not become:

```text
CAUSED_BY
```

without a stronger methodology.

---

# 193. Causal Relationship

Any causal assertion SHALL identify:

```text
method
assumptions
evidence
confidence
```

appropriate to the claim.

---

# 194. Correlation Relationship

Correlation MAY be represented as derived analytical lineage.

---

# 195. Graph Inference

Automated graph inference SHALL produce:

```text
CANDIDATE_RELATIONSHIP
```

unless methodology authorises stronger status.

---

# 196. Human Validation

Important inferred relationships MAY require human validation.

---

# 197. Graph Quality

Pulse SHOULD monitor:

```text
orphan nodes
broken edges
cycles
unknown sources
dangling mappings
classification conflicts
tenant conflicts
```

---

# 198. Graph Consistency Checks

Automated checks SHALL identify structurally impossible lineage.

---

# 199. Cycle Rules

Not every graph cycle is invalid.

For example:

```text
Company A owns Company B
Company B trades with Company A
```

may form a legitimate knowledge graph cycle.

But direct derivation lineage SHOULD remain acyclic.

---

# 200. Derivation DAG

Material transformation lineage SHALL form a directed acyclic graph unless a clearly defined iterative analytical process explicitly models iterations.

---

# 201. Iterative Models

Iterative computation SHALL represent successive runs or states rather than circular self-derivation.

---

# 202. Provenance IDs in Publications

Public products MAY expose stable citation identifiers that resolve internally to provenance objects.

---

# 203. Source Link Rot

External URLs may disappear.

The internal evidence identity SHALL remain stable.

---

# 204. Link-Rot Status

Pulse MAY record:

```text
SOURCE_URL_ACTIVE
SOURCE_URL_CHANGED
SOURCE_URL_UNAVAILABLE
```

without invalidating preserved evidence.

---

# 205. Source Identity Change

If an organisation moves a dataset to another URL, the DataSource identity MAY remain stable if semantics remain the same.

---

# 206. Dataset Split

If one dataset becomes several incompatible datasets, lineage SHALL preserve the split.

---

# 207. Dataset Merge

Likewise, merged datasets SHALL preserve predecessor relationships.

---

# 208. Source Succession

Institutional changes SHOULD support relationships such as:

```text
SUCCESSOR_OF
PREDECESSOR_OF
```

where relevant.

---

# 209. Regulation Succession

Regulatory instruments SHOULD preserve amendment and replacement chains.

---

# 210. Company Succession

Corporate mergers or restructurings MAY require lineage relationships while retaining historical legal identities.

---

# 211. Geographic Succession

Administrative boundary changes MAY likewise require predecessor relationships.

---

# 212. Research Reuse Graph

Pulse SHALL be able to identify which research assets are repeatedly reused.

---

# 213. Reuse Metrics

Possible internal metrics:

```text
Observation reuse count
EvidenceSet reuse
Method reuse
Dataset reuse
Source reuse
```

These may inform commercial investment decisions.

---

# 214. Evidence ROI

Source acquisition cost MAY eventually be compared with downstream product/revenue use.

Example:

```text
premium dataset
   ↓
used by 14 reports
   ↓
supports 6 subscriptions
```

This helps justify source licensing.

---

# 215. Method ROI

Likewise:

```text
OpportunityMethod v3
```

may support multiple commercial product families.

---

# 216. Knowledge Compounding

The lineage graph therefore becomes part of the mechanism by which Pulse's intellectual capital compounds.

---

# 217. Rejected Alternative — Provenance as JSON Metadata Only

Rejected.

Reason:

Unstructured provenance fields are difficult to traverse, validate and use for impact analysis.

---

# 218. Rejected Alternative — Log Files as Lineage

Rejected.

Logs are operational and ephemeral.

They do not provide canonical semantic relationships.

---

# 219. Rejected Alternative — Citation List Only

Rejected.

A bibliography cannot answer:

```text
which claim used which observation
```

or:

```text
which reports are affected by a revised dataset
```

---

# 220. Rejected Alternative — Graph Database First

Rejected.

The semantic model is required immediately.

A specialist graph datastore is not.

---

# 221. Rejected Alternative — Fully Event-Sourced Lineage

Rejected for the initial architecture.

Versioned edges and immutable records provide the required semantics without imposing full event sourcing.

---

# 222. Rejected Alternative — Hide Contradictory Evidence

Rejected.

The graph SHALL preserve disagreement.

---

# 223. Rejected Alternative — Flatten All Relationships to `RELATED_TO`

Rejected.

Relationship semantics are themselves valuable intelligence.

---

# 224. Governing Invariants

**LIN-PULSE-001**  
Every consequential intelligence object SHALL have traversable upstream provenance.

**LIN-PULSE-002**  
Every material evidence object SHALL support downstream dependency discovery.

**LIN-PULSE-003**  
Lineage relationships SHALL use explicit semantics.

**LIN-PULSE-004**  
Material lineage edges SHALL be independently identifiable.

**LIN-PULSE-005**  
Historical lineage SHALL not be silently rewritten.

**LIN-PULSE-006**  
Deterministic derivation and probabilistic association SHALL remain distinct.

**LIN-PULSE-007**  
Contradictory evidence SHALL remain represented.

**LIN-PULSE-008**  
Evidence direction SHALL belong to the analytical relationship.

**LIN-PULSE-009**  
Published Claims SHALL resolve to actual evidence paths.

**LIN-PULSE-010**  
Published charts and tables SHOULD retain data lineage.

**LIN-PULSE-011**  
ResearchSnapshots SHALL freeze specific lineage versions.

**LIN-PULSE-012**  
Cross-tenant traversal SHALL enforce tenant isolation.

**LIN-PULSE-013**  
Graph traversal SHALL not expose confidential downstream object existence through public upstream nodes.

**LIN-PULSE-014**  
Material mapping changes SHALL support impact analysis.

**LIN-PULSE-015**  
Method and model changes SHALL support impact analysis.

**LIN-PULSE-016**  
Source revisions and retractions SHALL support downstream impact discovery.

**LIN-PULSE-017**  
Impact detection SHALL not automatically imply invalidity.

**LIN-PULSE-018**  
Causation SHALL never be inferred merely from graph connectivity.

**LIN-PULSE-019**  
Source dependence SHALL be preserved where known.

**LIN-PULSE-020**  
Independent corroboration SHALL not be collapsed.

**LIN-PULSE-021**  
Lineage technology SHALL remain separable from lineage semantics.

**LIN-PULSE-022**  
A dedicated graph database SHALL require demonstrated workload need.

**LIN-PULSE-023**  
Lineage gaps SHALL be explicit rather than fabricated.

**LIN-PULSE-024**  
Restricted or deleted source content SHOULD retain lineage tombstones where lawful.

**LIN-PULSE-025**  
Operational logs SHALL not be relied upon as canonical provenance.

**LIN-PULSE-026**  
Agent and LLM outputs SHALL preserve provenance to the evidence they used.

**LIN-PULSE-027**  
Recommendations SHALL reference exact upstream versions.

**LIN-PULSE-028**  
Decisions SHALL reference the exact Recommendation considered.

**LIN-PULSE-029**  
Outcome feedback SHALL remain traceable to the decision and analytical path that preceded it.

**LIN-PULSE-030**  
Provenance completeness SHALL be a publication-quality concern.

---

# 225. Consequences

## Positive

This architecture gives Pulse:

```text
explainability
impact analysis
research reproducibility
source accountability
client transparency
correction propagation
method evaluation
historical reconstruction
cross-domain reasoning
evidence reuse
```

It also creates a foundation for increasingly sophisticated intelligence navigation and opportunity discovery.

## Costs

The architecture introduces:

```text
edge persistence
graph validation
lineage indexing
security-aware traversal
versioned relationships
impact-processing workflows
```

and potentially substantial lineage volumes.

These costs are justified because Pulse is intended to produce consequential and commercially defensible intelligence rather than opaque analytics.

---

# 226. Strategic Consequence — Intelligence That Can Explain Itself

A mature Pulse recommendation should not merely say:

```text
Enter Market X.
```

It should be capable of unfolding:

```text
RECOMMENDATION
      ↓
because Opportunity A
      ↓
because Insights B, C, D
      ↓
because Analyses E, F
      ↓
because Observations G..N
      ↓
from Sources O..R
```

That is not simply technical traceability.

It is commercially useful explanation.

---

# 227. Strategic Consequence — Research That Knows When It Is Becoming Stale

The reverse graph provides an equally important capability:

```text
SOURCE CHANGED
      ↓
OBSERVATION AFFECTED
      ↓
ANALYSIS AFFECTED
      ↓
CLAIM AFFECTED
      ↓
REPORT AFFECTED
      ↓
CLIENT DECISION ASSUMPTION MAY BE AFFECTED
```

Pulse can therefore move beyond publication into ongoing intelligence maintenance.

---

# 228. Strategic Consequence — The Decision Dependency Graph

Over time, high-value client advisory engagements may create:

```text
DECISION
  │
  ├── Recommendation
  │
  ├── Assumptions
  │
  ├── Opportunities
  │
  ├── Risks
  │
  ├── Forecasts
  │
  └── Evidence
```

Pulse can monitor the dependency graph continuously.

This is potentially more valuable than the original report.

---

# 229. Strategic Consequence — From Citation to Institutional Memory

Traditional research usually leaves:

```text
PDF
+
bibliography
```

Pulse instead accumulates:

```text
source
+
evidence
+
relationship
+
analysis
+
claim
+
decision
+
outcome
```

This gives Nabhold a research memory capable of learning not only what was discovered, but how discoveries were connected and whether resulting decisions worked.

---

# 230. Strategic Consequence — Opportunity Discovery Through Convergence

The graph creates another possibility.

Pulse may eventually discover commercially interesting convergence:

```text
TradeSignal
       \
        \
RegulatorySignal ─────► EmergingOpportunity
        /
       /
CompanyActivitySignal
       \
        \
InfrastructureSignal
```

No individual signal may be sufficiently meaningful.

The graph enables Pulse to see their intersection.

This is one architectural route toward identifying opportunities before they become obvious through conventional sector reports.

---

# 231. Strategic Consequence — Evidence as a Network Effect

Every correctly linked object increases the value of existing objects.

A newly identified company may connect to:

```text
trade flows
procurement records
ownership
news
locations
sector activity
```

A new regulation may connect to:

```text
products
countries
companies
trade corridors
reports
```

A new commodity observation may affect:

```text
suppliers
landed-cost models
risks
opportunities
```

The evidence base therefore becomes more valuable not merely because it grows in size, but because it grows in **connectivity**.

---

# 232. Final Decision Statement

Baobab Pulse SHALL maintain a **first-class, versioned, security-aware Evidence and Lineage Graph** connecting source information to canonical evidence, analysis, intelligence, publication, decisions and outcomes.

The graph SHALL support both:

```text
UPSTREAM EXPLANATION

Recommendation
    ↓
Insight
    ↓
Analysis
    ↓
Evidence
    ↓
Observation
    ↓
Source
```

and:

```text
DOWNSTREAM IMPACT

Source Change
    ↓
Observation
    ↓
Analysis
    ↓
Claim
    ↓
Report
    ↓
Recommendation
    ↓
Decision Assumption
```

Pulse SHALL therefore know not only:

```text
where its intelligence came from
```

but also:

```text
what depends upon each piece of evidence.
```

That capability is foundational to:

```text
defensible research
living reports
continuous advisory
decision monitoring
method backtesting
commercial trust
opportunity discovery
```

The Evidence Graph shall remain logically canonical even if its physical storage later evolves from PostgreSQL toward specialist graph technology.

For Baobab Pulse, provenance is not a footnote attached to intelligence.

**Provenance is part of the intelligence architecture itself.**