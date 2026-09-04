# ADR-PULSE-004 — Raw Acquisition, Immutable Evidence and Research Reproducibility

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-004`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:**  
`ADR-PULSE-001 — Engine Mission, Authority and System Boundary`  
`ADR-PULSE-002 — Canonical Intelligence Domain Model and Aggregate Boundaries`  
`ADR-PULSE-003 — External Source Adapter, Intelligence Acquisition and Commercial Research Fabric`  
**Decision Type:** Evidence Integrity, Auditability and Reproducibility Architecture Decision

## Context

Baobab Pulse is intended to produce intelligence that may be used in:

```text
investment decisions
market-entry decisions
procurement
supplier qualification
trade decisions
pricing
risk management
regulatory interpretation
strategic planning
commercial advisory
paid intelligence reports
```

The commercial value of such intelligence depends on more than analytical sophistication.

It depends on the ability to answer:

> **What exactly did Pulse know at the time, where did that information come from, what did the source actually say, how was it transformed, and can we reproduce the conclusion?**

This question becomes increasingly important as Pulse begins producing:

```text
commercial research papers
subscription intelligence
opportunity reports
risk reports
regulatory briefs
forecast products
client-specific advisory
```

If Pulse stores only the latest cleaned values, a future analyst may know that the system currently believes:

```text
coffee exports = X
```

but may no longer know:

```text
what the provider originally published
when it was published
which API response contained it
whether it was later revised
which parser interpreted it
which mapping transformed it
which methodology used it
```

That would weaken:

```text
auditability
research credibility
legal defensibility
client trust
historical analysis
model evaluation
```

Pulse therefore requires a deliberate evidence-preservation architecture.

---

# Decision

Baobab Pulse SHALL preserve external and internal source material through a **versioned, append-oriented evidence architecture**.

The architecture SHALL distinguish at least:

```text
SOURCE ARTEFACT
      ↓
RAW RECORD
      ↓
NORMALISED RECORD
      ↓
CANONICAL OBSERVATION
      ↓
EVIDENCE
      ↓
ANALYSIS
      ↓
CLAIM / INSIGHT
      ↓
PUBLICATION
```

Each stage SHALL be independently identifiable and traceable.

Published intelligence SHALL be reproducible against the evidence and methodology available at the time of publication, subject to applicable retention and licensing constraints.

---

# 1. Evidence Preservation Principle

The governing rule is:

> **Transformation may add meaning, but it must not erase origin.**

Pulse may:

```text
parse
clean
normalise
map
resolve
aggregate
derive
score
summarise
```

but the original source relationship SHALL remain recoverable.

---

# 2. Evidence Layers

Pulse SHALL recognise five principal evidence layers.

```text
L0 — SOURCE ARTEFACT
     provider-native object

L1 — RAW RECORD
     structured provider-native record

L2 — NORMALISED RECORD
     cleaned but source-semantic representation

L3 — CANONICAL OBSERVATION
     Pulse semantic representation

L4 — DERIVED EVIDENCE
     analytical or composite evidence
```

These layers SHALL not be collapsed indiscriminately.

---

# 3. Layer 0 — Source Artefact

A `SourceArtefact` is the preserved provider-native object.

Examples:

```text
JSON API response
CSV file
XLSX workbook
PDF report
government gazette
XML response
news article
GeoJSON file
image
ZIP archive
web page snapshot where lawful
```

---

# 4. SourceArtefact Structure

Conceptually:

```text
SourceArtefact
 ├── artefact_id
 ├── source_id
 ├── data_source_id
 ├── acquisition_id
 ├── external_identifier
 ├── media_type
 ├── original_filename
 ├── source_uri
 ├── publication_time
 ├── source_modified_time
 ├── retrieved_time
 ├── content_length
 ├── content_hash
 ├── storage_reference
 ├── licence_profile
 ├── classification
 ├── retention_policy
 └── metadata
```

---

# 5. Provider-Native Preservation

Where rights permit, the exact provider-native bytes SHALL be preserved.

This ensures later processors can operate against:

```text
what was actually retrieved
```

rather than a reconstructed approximation.

---

# 6. Raw Evidence Vault

SourceArtefacts SHALL be stored in a logically separate **Raw Evidence Vault**.

The Raw Evidence Vault SHALL be designed for:

```text
immutability
integrity checking
version retention
controlled access
reprocessing
audit
```

---

# 7. Storage Technology Independence

The Raw Evidence Vault SHALL initially be implementable using object storage.

This ADR does NOT require a dedicated data lake or lakehouse.

Conceptually:

```text
PostgreSQL
    metadata / lineage / indexes

Object Storage
    source artefacts
```

is sufficient for the initial architecture.

---

# 8. Object Identity

Every SourceArtefact SHALL receive an immutable Pulse identifier.

The identifier SHALL remain independent from:

```text
filename
URL
provider key
bucket key
```

---

# 9. Content Addressing

Every preservable SourceArtefact SHOULD have a cryptographic digest.

Conceptually:

```text
SHA-256(source bytes)
```

or an organisationally approved equivalent.

The digest provides:

```text
integrity validation
duplicate detection
change detection
audit evidence
```

---

# 10. Content Hash Is Not Business Identity

Two identical files may have the same hash.

They may still represent different acquisitions.

Therefore:

```text
content_hash
```

SHALL NOT substitute for:

```text
artefact_id
acquisition_id
```

---

# 11. Immutable Source Artefacts

Once committed:

```text
SourceArtefact.bytes
```

SHALL NOT be modified.

If the upstream publisher changes the document:

```text
Artefact A
```

and later:

```text
Artefact B
```

shall exist as separate artefacts.

---

# 12. Metadata Correction

Certain descriptive metadata MAY be corrected.

Examples:

```text
wrong language tag
misclassified source type
missing jurisdiction
```

Such changes SHALL be audited.

They SHALL NOT modify the source bytes.

---

# 13. Layer 1 — RawRecord

A `RawRecord` represents one provider-level logical record extracted or identified from a SourceArtefact or stream.

Examples:

```text
one row in CSV
one object in JSON array
one SDMX observation
one trade-flow record
one registry entity
one regulation notice
```

---

# 14. RawRecord Structure

```text
RawRecord
 ├── raw_record_id
 ├── artefact_id
 ├── acquisition_id
 ├── external_record_id
 ├── record_index
 ├── provider_schema
 ├── raw_payload
 ├── raw_hash
 ├── observed_time
 ├── publication_time
 ├── retrieved_time
 └── metadata
```

For very large payloads, `raw_payload` MAY be stored outside relational storage.

---

# 15. RawRecord Immutability

A RawRecord SHALL be immutable once successfully persisted.

---

# 16. Streaming Sources

For streaming sources where no natural file artefact exists, Pulse SHALL still create an immutable acquisition envelope.

Examples:

```text
event payload
websocket message
webhook
stream record
```

The message itself becomes the raw evidence object.

---

# 17. Layer 2 — NormalisedRecord

A `NormalisedRecord` represents source data after technical cleaning but before full Pulse semantic canonicalisation.

This is important.

Example:

Provider sends:

```text
"17,45"
```

Pulse may technically normalise this to:

```text
17.45
```

while preserving that the provider sent:

```text
"17,45"
```

---

# 18. NormalisedRecord Purpose

Normalisation MAY include:

```text
encoding correction
date parsing
numeric parsing
whitespace cleanup
provider field renaming
technical null handling
basic unit parsing
```

It SHALL NOT silently perform high-level business interpretation.

---

# 19. Raw versus Normalised

The relationship SHALL remain:

```text
RawRecord
    ↓
normalisation method
    ↓
NormalisedRecord
```

Both are retained where the transformation is material.

---

# 20. Layer 3 — Canonical Observation

A `CanonicalObservation` is the Pulse semantic representation defined by the canonical intelligence model.

Example:

```text
source field:
    "Coffee Exports"

provider code:
    090111

provider value:
    "12345"

canonical:
    commodity = green coffee
    measure = export_volume
    quantity = 12,345
    unit = kg
    reporter = Uganda
    period = 2026-01
```

---

# 21. Canonicalisation Must Be Reconstructable

Every canonical Observation SHALL identify:

```text
source record(s)
mapping rules
normalisation method
transformation version
entity resolution
classification mappings
unit conversions
```

that materially contributed to it.

---

# 22. Layer 4 — Derived Evidence

Derived evidence may include:

```text
aggregated observations
calculated indicators
model outputs
trend detections
forecast outputs
analytical results
```

These are no longer direct source facts.

Their derived nature SHALL be explicit.

---

# 23. Provenance Graph

Pulse SHALL maintain a provenance graph.

Example:

```text
SourceArtefact
      │
      ▼
RawRecord
      │
      ▼
NormalisedRecord
      │
      ▼
Observation
      │
      ▼
EvidenceEntry
      │
      ▼
EvidenceSet
      │
      ▼
Analysis
      │
      ▼
Claim
      │
      ▼
Report
```

---

# 24. Provenance Must Be Directed

A provenance relationship SHALL identify:

```text
input
transformation
output
```

This produces a directed acyclic derivation graph under normal processing semantics.

---

# 25. Provenance Cycles

Pulse SHALL reject provenance relationships that create impossible derivation cycles.

Example:

```text
Observation A
derived_from
Insight B

Insight B
derived_from
Observation A
```

cannot be accepted as direct derivation semantics.

---

# 26. TransformationRecord

Every material transformation SHOULD produce a `TransformationRecord`.

Conceptually:

```text
TransformationRecord
 ├── transformation_id
 ├── transformation_type
 ├── implementation
 ├── version
 ├── configuration_hash
 ├── input_references
 ├── output_references
 ├── actor_type
 ├── actor_reference
 ├── started_at
 ├── completed_at
 └── status
```

---

# 27. Transformation Types

```text
EXTRACT
PARSE
NORMALISE
MAP
RESOLVE
CONVERT
AGGREGATE
JOIN
FILTER
CLASSIFY
CALCULATE
MODEL
SUMMARISE
SYNTHESISE
CORRECT
```

---

# 28. Transformation Versioning

A transformation version SHALL change when its semantic effect changes.

Minor code refactoring that produces identical semantics need not create a new methodology version.

---

# 29. Configuration Is Part of Reproducibility

Where behaviour depends on configuration, the configuration SHALL be versioned or hashed.

Example:

```text
outlier_threshold = 3.0
```

versus:

```text
outlier_threshold = 2.0
```

may materially alter results.

---

# 30. Software Environment Capture

For consequential analysis, Pulse SHOULD preserve sufficient execution metadata to identify:

```text
application version
method version
model version
dependency lock identity
container image digest
```

where reproducibility requirements justify it.

---

# 31. Exact Reproducibility versus Semantic Reproducibility

Pulse SHALL distinguish:

```text
BITWISE REPRODUCIBILITY
```

from:

```text
SEMANTIC REPRODUCIBILITY
```

Bitwise reproduction may be impossible for:

```text
non-deterministic models
external inference APIs
floating-point differences
provider changes
```

The minimum requirement is semantic reproducibility sufficient to explain and reasonably recreate the published conclusion.

---

# 32. Research Snapshot

Every published commercial intelligence product SHALL have a `ResearchSnapshot`.

Conceptually:

```text
ResearchSnapshot
 ├── snapshot_id
 ├── research_mission_id
 ├── publication_id
 ├── created_at
 ├── dataset_versions
 ├── source_artefact_versions
 ├── evidence_sets
 ├── methodology_versions
 ├── model_versions
 ├── parameter_sets
 ├── analyst_version
 ├── report_version
 └── rights_manifest
```

---

# 33. Publication Freeze

When a report is published:

```text
relevant ResearchSnapshot
```

SHALL be frozen.

New data does not silently change the evidentiary basis of the published report.

---

# 34. Living Intelligence

A living report SHALL therefore have:

```text
Report v1
  └── Snapshot A

Report v2
  └── Snapshot B
```

rather than:

```text
one mutable report
pointing to today's data
```

---

# 35. Reproduce-As-Published

Pulse SHALL support the conceptual operation:

```text
REPRODUCE_AS_PUBLISHED(report_version)
```

This means:

> use the evidence, mappings, methods and models associated with the frozen ResearchSnapshot.

---

# 36. Recompute-With-Latest

Pulse SHOULD also support:

```text
RECOMPUTE_WITH_LATEST(report)
```

which intentionally applies current:

```text
data
methods
mappings
models
```

and therefore creates a new analytical result.

---

# 37. These Operations Must Remain Distinct

`REPRODUCE_AS_PUBLISHED` and `RECOMPUTE_WITH_LATEST` SHALL NEVER be treated as equivalent.

---

# 38. Data Vintage

Every revisable dataset SHALL support vintage semantics where meaningful.

Example:

```text
2026-Q1 GDP
published May 2026
```

and:

```text
2026-Q1 GDP
revised August 2026
```

are separate source states.

---

# 39. Vintage Identifier

A vintage MAY be identified by:

```text
publication timestamp
release identifier
source version
provider revision identifier
```

depending on source capability.

---

# 40. Observation Revision

If a provider revises a source fact:

```text
Observation A1
```

SHALL be superseded by:

```text
Observation A2
```

not overwritten.

---

# 41. Revision Relationship

Canonical relation:

```text
A2 SUPERSEDES A1
```

The older observation remains queryable historically.

---

# 42. Correction versus Revision

Pulse SHALL distinguish:

```text
SOURCE_REVISION
```

from:

```text
PULSE_CORRECTION
```

A source revision changes the upstream information.

A Pulse correction fixes our interpretation or processing.

---

# 43. Pulse Correction Example

Original source:

```text
USD 1.5 million
```

Pulse incorrectly parsed:

```text
15 million
```

A correction must preserve:

```text
original artefact
incorrect observation
correction event
corrected observation
reason
```

---

# 44. Evidence Immutability

Evidence that supported a published Claim SHALL not be destructively replaced merely because better evidence later appears.

The new evidence should support a new Claim version or publication revision.

---

# 45. EvidenceSet Versioning

```text
EvidenceSet v1
    ↓
used by Report v1

EvidenceSet v2
    ↓
used by Report v2
```

Both remain historically valid.

---

# 46. EvidenceSet Freeze

A frozen EvidenceSet SHALL prohibit:

```text
adding evidence
removing evidence
changing direction
changing evidence weight
```

Any such change produces another version.

---

# 47. Claim Versioning

Published Claims SHALL be versioned when substantive meaning changes.

Example:

```text
Claim v1:
    market demand is accelerating
```

may later become:

```text
Claim v2:
    previously observed demand acceleration has reversed
```

The second does not delete the first.

---

# 48. Claim Retraction

A false Claim may be:

```text
RETRACTED
```

while its historical existence remains auditable.

---

# 49. Citation Persistence

A citation SHALL resolve to the evidence version used at publication time.

It SHALL not automatically point to today's version of the source.

---

# 50. Citation Locator

Citation metadata SHOULD support:

```text
document
page
table
row
cell
paragraph
record identifier
URL
dataset
API observation
```

where applicable.

---

# 51. Citation Granularity

Pulse SHOULD cite at the narrowest practical evidence scope.

Not merely:

```text
World Bank
```

when:

```text
specific dataset
specific indicator
specific country
specific vintage
specific period
```

can be identified.

---

# 52. Citation Manifest

Every commercial publication SHALL have a machine-readable `CitationManifest`.

Conceptually:

```text
CitationManifest
 ├── publication_id
 ├── citations[]
 ├── source references
 ├── artefact references
 ├── attribution strings
 ├── licence obligations
 └── access dates
```

---

# 53. Rights-Aware Preservation

Evidence preservation is subject to source rights.

Pulse SHALL distinguish whether it may:

```text
store indefinitely
store temporarily
store metadata only
store extracted facts
store hashes only
redistribute
quote
```

---

# 54. Restricted Evidence

Where full storage is prohibited, Pulse MAY preserve:

```text
source reference
hash
retrieval metadata
derived observation
licence metadata
```

while omitting restricted raw content.

---

# 55. Evidence Availability State

Evidence SHALL support states such as:

```text
AVAILABLE
ARCHIVED
RESTRICTED
EXPIRED
SOURCE_REMOVED
LEGAL_HOLD
PURGED
```

---

# 56. Purging

Where data must legally or contractually be removed, Pulse SHALL retain an auditable tombstone if permitted.

Example:

```text
artefact removed
reason = licence expiry
removed_at = ...
```

---

# 57. Legal Hold

Evidence subject to a legal or contractual preservation requirement MAY enter:

```text
LEGAL_HOLD
```

preventing ordinary retention deletion.

---

# 58. Retention Policy

Every source SHOULD define a `RetentionPolicy`.

Conceptually:

```text
RetentionPolicy
 ├── retention_period
 ├── archival_period
 ├── deletion_policy
 ├── legal_hold_supported
 ├── raw_retention
 ├── derived_retention
 └── policy_reference
```

---

# 59. Evidence Classification

Classification SHALL apply independently from retention.

Example:

```text
PUBLIC
```

does not mean:

```text
retain forever
```

and:

```text
CONFIDENTIAL
```

does not necessarily mean:

```text
retain briefly
```

---

# 60. Tenant Evidence

Tenant-private source artefacts SHALL inherit tenant isolation.

---

# 61. Derived Classification

A derived EvidenceSet SHALL be classified at least as restrictively as its contributing evidence unless an authorised policy permits otherwise.

---

# 62. Classification Snapshot

Published products SHALL preserve the classification applied at publication.

---

# 63. Evidence Access Control

Access SHALL be evaluated against:

```text
tenant
context
classification
role
purpose
licence
retention
```

not merely whether an artefact ID is known.

---

# 64. Evidence Purpose Limitation

Restricted or personal data MAY require explicit purpose metadata.

---

# 65. Raw Vault Access

Raw Evidence Vault access SHOULD be narrower than canonical Observation access.

Most analysts should not require direct unrestricted access to every raw source artefact.

---

# 66. Chain of Custody

For high-value or sensitive evidence, Pulse SHOULD be capable of recording a chain of custody.

Conceptually:

```text
acquired by
validated by
transformed by
reviewed by
published by
```

---

# 67. Evidence Integrity Verification

Pulse SHOULD periodically verify stored content hashes.

Integrity failures SHALL be treated as security or storage incidents.

---

# 68. Corruption Detection

If:

```text
stored bytes
```

no longer match:

```text
registered content hash
```

the artefact SHALL be quarantined.

---

# 69. Storage Replication

Replication MAY improve durability.

Replication SHALL not alter evidence identity.

---

# 70. Backup

Backup policy SHALL preserve both:

```text
relational provenance metadata
```

and:

```text
raw evidence artefacts
```

as a coherent recoverable system.

---

# 71. Orphan Prevention

The system SHALL prevent:

```text
database metadata pointing to missing artefact
```

without explicit missing-state semantics.

---

# 72. Evidence Garbage Collection

Garbage collection SHALL be policy-aware.

A raw artefact referenced by:

```text
published report
legal hold
frozen evidence set
```

SHALL not be deleted by ordinary cleanup.

---

# 73. Duplicate Artefacts

If identical content is acquired twice, Pulse MAY physically deduplicate storage.

However, logical acquisition records SHALL remain separate.

---

# 74. Physical Deduplication versus Logical Provenance

This distinction is mandatory.

```text
one stored object
```

may support:

```text
Acquisition A
Acquisition B
```

without losing historical provenance.

---

# 75. Acquisition Snapshot

Every Acquisition SHOULD preserve:

```text
request parameters
pagination/cursor state
endpoint
adapter version
source response metadata
retrieval time
```

sufficient for reconstruction.

---

# 76. API Query Provenance

For API sources, the exact query parameters used to acquire data SHOULD be preserved.

---

# 77. Sensitive Query Parameters

Secrets SHALL NOT be preserved in provenance.

For example:

```text
API key
bearer token
session cookie
```

must be excluded or redacted.

---

# 78. HTTP Metadata

Useful acquisition metadata MAY include:

```text
ETag
Last-Modified
Content-Type
Content-Length
response status
```

without persisting sensitive headers.

---

# 79. Source URL Stability

A URL SHALL be treated as descriptive metadata.

It SHALL not be the sole durable evidence identity.

---

# 80. Dynamic Web Sources

Where a web page changes continuously, Pulse SHOULD preserve:

```text
retrieval timestamp
content hash
permitted snapshot
```

where lawful.

---

# 81. Evidence Extraction from PDF

For PDFs, Pulse SHALL distinguish:

```text
source PDF
```

from:

```text
extracted text
```

from:

```text
extracted table
```

from:

```text
canonical observation
```

Each is a separate derivation layer.

---

# 82. Table Extraction Provenance

A table-derived Observation SHOULD retain:

```text
source document
page
table
row
column
extraction method/version
```

where available.

---

# 83. OCR Evidence

Where OCR is necessary, OCR output SHALL be marked as machine-extracted text and retain confidence where available.

OCR output is not the original document.

---

# 84. Language Translation

Translated source text SHALL retain:

```text
original text reference
source language
target language
translation method
translation version
```

---

# 85. Translation Is a Transformation

A translation used as evidence SHALL not be treated as source-native text.

---

# 86. Machine Summaries

Summaries SHALL be derived artefacts.

They SHALL not replace underlying documents.

---

# 87. LLM Outputs

LLM outputs SHALL preserve:

```text
model identity
model version/provider identifier
prompt template version
structured inputs
generation parameters where material
timestamp
output
validation status
```

for consequential analytical use.

---

# 88. Non-Deterministic Outputs

If exact model output cannot be reproduced, Pulse SHALL still preserve the original generated result as an immutable analytical artefact.

---

# 89. Prompt Versioning

A materially changed prompt template SHALL receive a new version.

---

# 90. Model Replacement

Historical analysis SHALL continue to reference the model originally used even after that model is retired.

---

# 91. Model Availability Loss

If an external model becomes unavailable, the historical ModelRun and output remain part of the ResearchSnapshot.

---

# 92. Human Analysis

Human analytical contributions SHALL also be attributable.

A human-written Claim SHOULD preserve:

```text
author
reviewer
created_at
revision
```

---

# 93. Analyst Notes

Internal notes MAY be preserved separately from publishable evidence.

They SHALL not automatically become citations.

---

# 94. Evidence versus Working Material

Pulse SHALL distinguish:

```text
WORKING_MATERIAL
```

from:

```text
APPROVED_EVIDENCE
```

---

# 95. Research Drafts

Draft reports are mutable working artefacts.

Published reports are versioned immutable publications.

---

# 96. Report Versioning

Conceptually:

```text
Report 1.0
Report 1.1
Report 2.0
```

Version semantics shall be defined in the publication contract.

---

# 97. Minor Correction

A typographical correction MAY produce:

```text
1.0 → 1.0.1
```

without changing evidence.

---

# 98. Analytical Revision

A changed analytical conclusion SHOULD create a materially new report version.

---

# 99. Publication Timestamp

Every publication SHALL have an immutable publication timestamp.

---

# 100. Research State at Publication

Pulse SHALL be capable of answering:

> What did this report know at 09:00 on 4 September 2026?

without substituting information acquired later.

---

# 101. Bitemporal Evidence

Where justified, observations SHALL preserve both:

```text
valid_time
```

and:

```text
system_time
```

This allows historical questions such as:

> What did Pulse believe about January trade volumes in March, before the June revision?

---

# 102. System-Time History

A current canonical row alone is insufficient where revisions materially affect research conclusions.

---

# 103. Regulatory Evidence

Regulatory sources SHALL preserve:

```text
publication time
adoption time
effective time
supersession/repeal
```

independently.

---

# 104. Regulatory Reproducibility

A report produced before a regulation became effective must not later appear to have known the regulation was already effective.

---

# 105. Forecast Reproducibility

Every Forecast SHALL freeze its:

```text
input evidence
model/method
forecast origin
parameters
```

---

# 106. Backtesting

Forecast backtesting SHALL use:

```text
information available at forecast origin
```

not revised future datasets unless the test explicitly states otherwise.

---

# 107. Look-Ahead Bias Prohibition

Pulse SHALL prohibit accidental use of future information in historical model evaluation.

---

# 108. Research Backtesting

Opportunity-detection methodologies SHOULD eventually support historical replay.

Question:

> If this methodology had existed three years ago, what would it have identified using only evidence available then?

This capability could become one of Pulse's strongest methodology-validation mechanisms.

---

# 109. Historical Replay

Historical replay SHALL use:

```text
historical source vintages
historical mappings where relevant
historical methodology version
```

or explicitly state when approximations are used.

---

# 110. Methodology Evaluation

Pulse SHOULD preserve outcomes sufficiently to compare:

```text
predicted opportunity
```

against:

```text
later observed reality
```

---

# 111. Research Integrity Tiers

Commercial products MAY have different reproducibility standards.

Example:

```text
TIER 1 — EXPLORATORY
best-effort sourcing

TIER 2 — PROFESSIONAL
full claim/evidence traceability

TIER 3 — DECISION GRADE
frozen snapshot + methodology + review

TIER 4 — AUDIT GRADE
enhanced chain of custody + reproducibility package
```

These names remain conceptual.

---

# 112. Product Tier Determines Evidence Burden

A short public brief need not carry the same internal audit package as a high-value investment diligence report.

But all tiers SHALL preserve minimum provenance.

---

# 113. Evidence Package

For high-value engagements, Pulse MAY produce an `EvidencePackage`.

Conceptually:

```text
EvidencePackage
 ├── source manifest
 ├── citation manifest
 ├── methodology
 ├── evidence coverage
 ├── contradiction register
 ├── data vintages
 ├── limitations
 ├── report snapshot
 └── integrity manifest
```

---

# 114. Integrity Manifest

An `IntegrityManifest` MAY contain:

```text
artefact hashes
snapshot hash
report hash
method versions
```

to prove publication integrity.

---

# 115. Signed Publications

Future high-assurance products MAY cryptographically sign:

```text
publication
research snapshot
integrity manifest
```

This ADR permits but does not mandate digital signatures initially.

---

# 116. Commercial Dispute Resolution

If a client challenges a conclusion, Pulse should permit investigators to trace:

```text
Report
 ↓
Claim
 ↓
EvidenceSet
 ↓
Observation
 ↓
RawRecord
 ↓
SourceArtefact
```

and determine whether the dispute concerns:

```text
source fact
source revision
mapping
methodology
analysis
interpretation
```

---

# 117. Error Taxonomy

Research corrections SHOULD classify errors as:

```text
SOURCE_ERROR
ACQUISITION_ERROR
EXTRACTION_ERROR
NORMALISATION_ERROR
MAPPING_ERROR
ENTITY_RESOLUTION_ERROR
METHOD_ERROR
MODEL_ERROR
ANALYST_ERROR
EDITORIAL_ERROR
PUBLICATION_ERROR
```

---

# 118. Root-Cause Analysis

Material research errors SHOULD permit root-cause analysis and remediation.

---

# 119. Error Learning

Corrections SHALL feed:

```text
quality rules
adapter tests
mapping tests
methodology improvements
analyst guidance
```

where relevant.

---

# 120. Reproducibility and Commercial Trust

This architecture creates an important commercial distinction.

Nabhold should be able to say, in substance:

> We do not merely provide a generated report. We maintain the evidence lineage, source vintage, methodology and publication history behind the report.

That is materially stronger than opaque generated research.

---

# 121. Research as Institutional Memory

The immutable evidence architecture means each engagement adds to a durable institutional research history.

---

# 122. Research Corpus Integrity

The ResearchCorpus SHALL distinguish:

```text
current truth
historical truth
superseded analysis
retracted analysis
draft material
```

---

# 123. Historical Knowledge Shall Not Be Rewritten

A conclusion that was reasonable in 2026 may become wrong in 2028.

That does not make the 2026 research record worthless.

Pulse SHALL preserve the distinction:

```text
reasonable given evidence then
```

versus:

```text
correct according to later knowledge
```

---

# 124. Data Lineage Query

Pulse SHALL ultimately support queries such as:

```text
show every report using Observation X

show every Insight derived from DatasetVersion Y

show every Claim affected by MappingVersion Z

show every report using a now-retracted source

show every forecast produced by ModelVersion M
```

---

# 125. Impact Analysis

This lineage permits proactive impact analysis.

Example:

```text
Source revises trade dataset
        ↓
Pulse identifies affected Observations
        ↓
affected EvidenceSets
        ↓
affected Claims
        ↓
affected Reports
```

---

# 126. Research Invalidation Event

A material upstream revision MAY generate:

```text
ResearchInvalidationCandidate
```

rather than automatically retracting reports.

---

# 127. Human Review of Invalidation

A source revision does not always materially change a conclusion.

Pulse SHOULD assess significance before requiring publication revision.

---

# 128. Significance Threshold

Product methodologies MAY define whether an upstream change is:

```text
IMMATERIAL
MINOR
MATERIAL
CRITICAL
```

---

# 129. Living-Report Refresh

A material update MAY trigger:

```text
REASSESSMENT_REQUIRED
```

for a living report.

---

# 130. Subscription Advantage

This enables a premium recurring service:

> **We do not simply issue the report. We continue monitoring the evidence that supports it.**

---

# 131. Evidence Dependency Monitoring

Pulse SHOULD maintain dependency graphs for subscription intelligence.

---

# 132. Evidence Expiry

If a key evidence source becomes stale, affected intelligence MAY enter:

```text
EVIDENCE_STALE
```

state.

---

# 133. Confidence Degradation

Staleness MAY reduce confidence according to methodology.

It SHALL not silently replace the original confidence without preserving history.

---

# 134. Research Validity Window

A report MAY define:

```text
valid_until
```

or:

```text
review_by
```

where appropriate.

---

# 135. No Eternal Market Report

Time-sensitive intelligence SHALL not be presented as permanently current.

---

# 136. Reproducible Tables and Charts

Tables and charts in commercial products SHOULD derive from versioned analytical outputs.

They SHOULD NOT be manually altered in ways that break data lineage.

---

# 137. Chart Provenance

A chart SHOULD be able to identify:

```text
query/method
dataset
filters
observation versions
rendering version
```

where practical.

---

# 138. Narrative Numbers

Numbers appearing in prose SHOULD be traceable to canonical evidence or derived analytical outputs.

---

# 139. Hand-Entered Numbers

Manual numerical entries SHALL be explicitly marked as manual evidence or analyst input.

---

# 140. Manual Evidence

Manual Evidence SHALL preserve:

```text
author
source description
entry time
validation status
```

---

# 141. Telephone and Interview Evidence

Where research includes interviews, Pulse MAY represent them as controlled evidence objects.

Their use SHALL respect:

```text
consent
confidentiality
attribution preference
recording rights
```

---

# 142. Confidential Sources

Pulse MAY support source attribution levels such as:

```text
PUBLICLY_ATTRIBUTABLE
CLIENT_VISIBLE
INTERNAL_ONLY
CONFIDENTIAL_SOURCE
```

subject to policy.

---

# 143. Anonymous Evidence

Anonymous or confidential evidence SHALL be clearly distinguished from publicly verifiable evidence.

---

# 144. Research Evidence Balance

High-value research MAY legitimately use both:

```text
machine-readable statistical evidence
```

and:

```text
qualitative expert evidence
```

without pretending they are methodologically identical.

---

# 145. Evidence Type

Canonical EvidenceType SHOULD support:

```text
STRUCTURED_DATA
SOURCE_DOCUMENT
REGULATORY_DOCUMENT
NEWS
COMPANY_DISCLOSURE
INTERVIEW
MANUAL_OBSERVATION
MODEL_OUTPUT
INTERNAL_SYSTEM_RECORD
ANALYST_DERIVATION
OTHER
```

---

# 146. Evidence Strength

Evidence strength SHALL be contextual and methodology-specific.

Pulse SHALL not assign universal truth rankings such as:

```text
official = 100
news = 50
```

without methodological justification.

---

# 147. Evidence Weight

Evidence weight belongs to an analytical EvidenceSet or method.

The same source may carry different relevance across different questions.

---

# 148. Contradiction Preservation

If two sources disagree:

```text
Source A = 10
Source B = 14
```

Pulse SHALL preserve both source paths.

---

# 149. Resolution Is Analytical

A methodology MAY select one as preferable.

That analytical choice SHALL itself be recorded.

---

# 150. Consensus Calculation

Where consensus values are calculated:

```text
mean
median
weighted estimate
```

the aggregation method SHALL be explicit.

---

# 151. Source Replacement

If a commercial provider is later replaced, old reports SHALL continue referencing the original provider.

---

# 152. Mapping Evolution

Canonical mappings change over time.

Example:

```text
HS code mappings
company entity resolution
geographic boundaries
```

Historical ResearchSnapshots SHALL reference the mapping version used.

---

# 153. Mapping Correction

If an entity was incorrectly mapped:

```text
Company A → Company B
```

a correction SHALL preserve:

```text
old mapping
new mapping
reason
affected intelligence
```

---

# 154. Entity Merge

If two canonical entities are later determined to be identical, Pulse SHALL preserve alias/merge history rather than rewriting every historical identifier invisibly.

---

# 155. Geographic Boundary Change

Boundary changes SHALL not rewrite historical geographic meaning.

---

# 156. Methodology Drift

A methodology that changes gradually without versioning creates irreproducible research.

Therefore methodology versioning is mandatory.

---

# 157. Model Drift

Model performance drift SHALL not alter historical ModelRun interpretation.

---

# 158. Dependency Drift

Software dependency changes MAY matter for analytical reproducibility.

High-assurance jobs SHOULD preserve dependency lock identity.

---

# 159. Container Digest

Where a container executes consequential research, the immutable image digest SHOULD be recorded.

---

# 160. Reproducible Build Relationship

Pulse runtime artefacts SHOULD be reproducibly buildable according to wider Baobab engineering governance.

---

# 161. Time Standard

Machine timestamps SHALL be stored as timezone-aware instants.

UTC SHALL be the default machine comparison basis.

Source-local timezone SHALL be preserved when relevant.

---

# 162. Calendar Period

Statistical periods such as:

```text
2026-Q1
2026-M03
FY2026
```

SHALL not be reduced blindly to arbitrary timestamps.

A `ReportingPeriod` concept SHALL preserve the source period semantics.

---

# 163. Fiscal Calendars

Company and government fiscal-year periods MAY differ.

Pulse SHALL preserve fiscal-calendar context.

---

# 164. Partial Dates

A source reporting only:

```text
March 2026
```

SHALL not be falsely converted into an exact event timestamp.

---

# 165. Approximate Dates

Approximate or inferred time SHALL be marked as such.

---

# 166. Unknown Time

Unknown timestamps SHALL remain unknown.

They SHALL not default to acquisition time unless the semantic field explicitly means retrieval time.

---

# 167. Source Publication versus Retrieval

These times are especially important:

```text
published_at
retrieved_at
```

A source may be published days before Pulse retrieves it.

---

# 168. Detection Latency

The difference:

```text
retrieved_at - published_at
```

can help measure acquisition latency.

---

# 169. Intelligence Latency

Similarly:

```text
insight_published_at - source_published_at
```

may measure intelligence time advantage.

---

# 170. Evidence Provenance API

Pulse SHALL eventually expose authorised provenance queries.

Examples:

```text
GET evidence lineage
GET claim sources
GET report snapshot
GET observation revisions
```

Exact API paths are deferred.

---

# 171. Internal versus Client Provenance

Not every internal implementation detail needs to be exposed externally.

Pulse SHALL support:

```text
INTERNAL_PROVENANCE
```

and:

```text
CLIENT_VISIBLE_PROVENANCE
```

views.

---

# 172. Client Evidence Portal

A future premium capability MAY allow a client to inspect:

```text
report
claims
citations
source list
methodology
revision history
```

without exposing restricted internal data.

---

# 173. Research Certification

Nabhold MAY eventually define internal publication certifications such as:

```text
Pulse Verified
Pulse Decision Grade
```

but these SHALL only exist if supported by measurable quality gates.

---

# 174. Evidence SLA

Certain product classes MAY define minimum evidence coverage and freshness.

---

# 175. Publication Blocking Conditions

Publication SHALL be blocked where:

```text
mandatory evidence missing
rights unresolved
critical evidence stale
provenance broken
required review incomplete
```

according to product policy.

---

# 176. Non-Blocking Warnings

Other conditions may produce warnings:

```text
limited competition data
one source only
partial geography
historical gap
```

while permitting publication with disclosure.

---

# 177. Evidence Completeness

Pulse SHOULD calculate evidence completeness against the ResearchMission's EvidencePlan.

---

# 178. Method Completeness

A methodology SHOULD declare required inputs.

---

# 179. Data Sufficiency

Before executing certain analyses Pulse SHOULD validate:

```text
minimum observations
time span
sample coverage
source types
```

---

# 180. Failed Reproducibility

If a historical result cannot be reproduced, Pulse SHALL record why.

Possible reasons:

```text
SOURCE_NOT_RETAINED
LICENCE_RESTRICTION
MODEL_PROVIDER_UNAVAILABLE
MISSING_DEPENDENCY
CORRUPT_ARTEFACT
NON_DETERMINISTIC_OUTPUT
INSUFFICIENT_METADATA
```

---

# 181. Reproducibility Score

Pulse MAY eventually assess research reproducibility.

This SHALL not become a meaningless vanity percentage.

Any score must be based on defined criteria.

---

# 182. Audit Trail

Significant actions SHALL be auditable.

Examples:

```text
evidence approved
evidence rejected
mapping changed
claim approved
report published
report corrected
report retracted
```

---

# 183. Audit Record Is Not Provenance Record

Audit answers:

> Who changed or approved something?

Provenance answers:

> From what was this derived?

Both are required.

---

# 184. Event Log Is Not Audit Log

Domain events and audit records MAY overlap but SHALL not be treated as identical abstractions.

---

# 185. Research Lineage Retention

Lineage supporting published commercial products SHOULD generally have longer retention than transient operational logs.

---

# 186. Operational Logs

Operational logs MAY expire without affecting research reproducibility if the relevant evidence, provenance and audit records remain.

---

# 187. Evidence Immutability Does Not Mean Storage Immutability Everywhere

Mutable operational metadata is allowed.

The immutable requirement applies to semantic source content and historical publication evidence.

---

# 188. Write-Once Principle

Where infrastructure permits, Raw Evidence Vault controls SHOULD approximate:

```text
write once
read many
```

for preserved artefacts.

---

# 189. Administrative Override

Exceptional administrative correction SHALL require:

```text
authorisation
reason
audit
```

---

# 190. No Silent Mutation

There SHALL be no privileged shortcut that silently rewrites historical evidence.

---

# 191. Rejected Alternative — Store Only Canonical Data

Rejected.

Reason:

When a parser, mapping or source interpretation is later questioned, the source material would no longer be available.

---

# 192. Rejected Alternative — Keep Only the Latest Source Version

Rejected.

Reason:

Historical research becomes impossible to reconstruct after revisions.

---

# 193. Rejected Alternative — Archive Only Published PDFs

Rejected.

Reason:

A PDF records the output but not the complete evidence and methodology chain.

---

# 194. Rejected Alternative — Full Event Sourcing for Everything

Rejected for the initial architecture.

Reason:

Event sourcing would add significant implementation complexity beyond what is required to obtain robust provenance and version history.

---

# 195. Rejected Alternative — Blockchain as Evidence Store

Rejected as the default approach.

A distributed ledger is unnecessary for establishing internal evidence integrity.

Cryptographic hashes, immutable artefacts, audit history and controlled storage are sufficient.

A future ledger integration MAY notarise hashes or publication manifests if a concrete trust model justifies it.

---

# 196. Rejected Alternative — Trust LLM Citations

Rejected.

Citations SHALL resolve to stored source/evidence identities.

---

# 197. Rejected Alternative — Recreate Historical Analysis with Current Data

Rejected.

This creates historical hindsight and destroys research validity.

---

# 198. Governing Invariants

**EVD-PULSE-001**  
Provider-native source content SHALL be preserved where rights permit.

**EVD-PULSE-002**  
Preserved SourceArtefacts SHALL be immutable.

**EVD-PULSE-003**  
Every SourceArtefact SHALL have integrity metadata.

**EVD-PULSE-004**  
RawRecord content SHALL not be destructively overwritten.

**EVD-PULSE-005**  
Canonical Observations SHALL retain lineage to source evidence.

**EVD-PULSE-006**  
Material transformations SHALL identify versioned methods.

**EVD-PULSE-007**  
Published EvidenceSets SHALL be frozen.

**EVD-PULSE-008**  
Published Claims SHALL reference frozen evidence.

**EVD-PULSE-009**  
Historical source revisions SHALL remain reconstructable where rights permit.

**EVD-PULSE-010**  
Source revision and Pulse correction SHALL remain distinguishable.

**EVD-PULSE-011**  
Research publications SHALL have frozen ResearchSnapshots.

**EVD-PULSE-012**  
Reproduce-as-published SHALL never substitute current evidence for historical evidence.

**EVD-PULSE-013**  
Backtesting SHALL prevent look-ahead bias.

**EVD-PULSE-014**  
Licensing and retention rights SHALL govern raw evidence preservation.

**EVD-PULSE-015**  
Evidence deletion SHALL not silently break lineage.

**EVD-PULSE-016**  
Restricted evidence SHALL not become broadly accessible merely because a derived observation exists.

**EVD-PULSE-017**  
Citations SHALL resolve to actual evidence objects.

**EVD-PULSE-018**  
Model-generated output SHALL retain model/run provenance.

**EVD-PULSE-019**  
Human-authored analysis SHALL remain attributable.

**EVD-PULSE-020**  
Historical methodologies SHALL remain identifiable.

**EVD-PULSE-021**  
Mapping revisions SHALL not invisibly rewrite historical research.

**EVD-PULSE-022**  
Research corrections SHALL preserve the original publication state.

**EVD-PULSE-023**  
Material upstream revisions SHALL support downstream impact analysis.

**EVD-PULSE-024**  
Data staleness SHALL be visible.

**EVD-PULSE-025**  
A report SHALL not appear current beyond its evidence validity without explicit refresh.

---

# 199. Consequences

## Positive

This decision provides:

```text
research defensibility
historical reproducibility
client trust
correction capability
publication integrity
backtesting
method validation
source-revision awareness
impact analysis
long-lived institutional memory
```

It also creates a major commercial differentiator.

Pulse reports can be backed by a durable evidentiary chain rather than being disposable generated documents.

## Negative

The approach requires:

```text
additional storage
version management
retention policies
provenance metadata
snapshot management
rights governance
```

It is operationally more complex than retaining only latest canonical values.

That complexity is intentional because research integrity is a core product capability.

---

# 200. Strategic Commercial Consequence

This architecture permits Nabhold to evolve from:

```text
"We produced a market report."
```

to:

```text
"We maintain a continuously versioned evidence base
for this market and can show exactly what changed
since the report was issued."
```

That enables stronger recurring products.

For example:

```text
Initial Market Report
        ↓
Evidence Monitoring
        ↓
Material Change Detected
        ↓
Client Alert
        ↓
Updated Analysis
        ↓
Report Revision
```

The report becomes the visible output of a deeper intelligence service.

---

# 201. Evidence as a Compounding Asset

Each preserved research cycle adds:

```text
source artefacts
historical vintages
normalised records
mapping history
methodology history
claims
outcomes
```

to Pulse's institutional memory.

This means historical work does not disappear when a consulting engagement ends.

---

# 202. Research Time Machine

The mature Pulse platform should eventually behave as a **research time machine**.

An analyst should be able to ask:

```text
What did we know about this market in June 2026?

What sources supported that view?

Which data were later revised?

Which conclusions changed?

Would our current methodology have detected
the opportunity earlier?

Which signals were false positives?
```

This capability would be unusually valuable for:

```text
strategy
investment
risk
forecasting
methodology improvement
client trust
```

---

# 203. Commercial Evidence Monitoring

A premium product MAY monitor the evidence behind an existing client decision.

Example:

```text
CLIENT DECISION:
enter market X

PULSE MONITORS:
trade growth
currency
tariffs
competitors
regulation
macro conditions
logistics
```

If material evidence changes:

```text
Decision Assumption Changed
```

can be emitted.

---

# 204. Decision Assumption Register

A future high-value ResearchProduct SHOULD be capable of declaring:

```text
DecisionAssumption
 ├── assumption
 ├── evidence
 ├── validity
 ├── sensitivity
 └── monitoring rule
```

This turns a one-off advisory recommendation into a monitored strategic position.

---

# 205. From Report Monitoring to Decision Monitoring

The highest commercial evolution may therefore be:

```text
DATA MONITORING
      ↓
REPORT MONITORING
      ↓
ASSUMPTION MONITORING
      ↓
DECISION MONITORING
```

At that point Pulse is no longer merely selling documents.

It is helping clients monitor the continuing validity of important decisions.

---

# 206. Final Decision Statement

Baobab Pulse SHALL preserve a **versioned, immutable and provenance-rich evidence chain** sufficient to reconstruct consequential research and intelligence historically.

The canonical evidentiary path SHALL remain:

```text
SOURCE
   ↓
SOURCE ARTEFACT
   ↓
RAW RECORD
   ↓
NORMALISED RECORD
   ↓
CANONICAL OBSERVATION
   ↓
EVIDENCE
   ↓
EVIDENCE SET
   ↓
ANALYSIS
   ↓
CLAIM / INSIGHT
   ↓
RECOMMENDATION
   ↓
RESEARCH SNAPSHOT
   ↓
PUBLICATION
```

At every material stage Pulse SHALL know:

```text
what
from where
when
under which source version
under which transformation
under which mapping
under which methodology
under which model
under which licence
under which classification
```

This architecture shall make it possible for Nabhold to produce intelligence that can be:

```text
challenged
verified
corrected
reproduced
updated
backtested
defended
```

rather than merely generated.

For Baobab Pulse, **evidence history is not archival overhead**.

It is part of the product.