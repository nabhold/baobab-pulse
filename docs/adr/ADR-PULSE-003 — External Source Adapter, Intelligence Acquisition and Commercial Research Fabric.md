# ADR-PULSE-003 — External Source Adapter, Intelligence Acquisition and Commercial Research Fabric

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-003`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:**  
`ADR-PULSE-001 — Engine Mission, Authority and System Boundary`  
`ADR-PULSE-002 — Canonical Intelligence Domain Model and Aggregate Boundaries`  
**Decision Type:** Foundational Data Acquisition and Commercial Intelligence Architecture Decision

---

# 1. Context

Baobab Pulse is intended to become considerably more than an internal analytics capability.

It should enable Nabhold to build a durable intelligence business around a simple proposition:

> **The world produces enormous quantities of useful information, but decision-makers rarely suffer from a shortage of information. They suffer from fragmented evidence, uncertain provenance, inconsistent classifications, incompatible geographies, delayed interpretation and an inability to convert information into a defensible decision.**

This represents an architectural and commercial opportunity.

Governments publish statistics.

Central banks publish monetary and foreign-exchange information.

Customs authorities publish tariffs and trade notices.

International institutions publish macroeconomic and trade datasets.

Commodity exchanges publish market observations.

Weather and earth-observation systems publish environmental data.

Corporate registries publish company information.

Ports, logistics providers and maritime sources publish movement information.

News organisations publish events.

Legislatures and regulators publish rules.

Companies themselves generate commercial and operational data.

Yet these sources rarely arrive:

```text
in the same format
with the same identifiers
at the same frequency
under the same licence
using the same units
using the same currencies
using the same geographic definitions
using the same product classifications
or describing the same point in time
```

The resulting fragmentation is precisely where an intelligence engine can create value.

Current public infrastructure already demonstrates the scale of the opportunity. The World Bank Indicators API exposes nearly 16,000 time-series indicators across more than 45 databases; the IMF exposes data through SDMX APIs; the WTO provides programmatic access to trade, services, tariff and market-access indicators; and WTO's Tariff and Trade Data dataset brings together official tariff schedules and merchandise-trade statistics covering more than 150 economies.

Likewise, GLEIF exposes legal-entity and corporate-relationship data, including fuzzy searches over entity names and addresses and parent-child relationships, while Copernicus provides programmatic access to substantial climate and environmental datasets.

The architectural opportunity is therefore not:

```text
build another dashboard
```

nor:

```text
connect to a few APIs
```

nor:

```text
ask an LLM to search the internet
```

The opportunity is to construct a **commercial-grade intelligence acquisition fabric** capable of continuously turning heterogeneous external and internal evidence into reproducible intelligence products.

---

# 2. Decision

Baobab Pulse SHALL implement an **External Intelligence Acquisition Fabric**, hereafter the **Pulse Source Mesh**.

The Source Mesh SHALL consist conceptually of:

```text
SOURCE DISCOVERY
      ↓
SOURCE REGISTRY
      ↓
LICENSING & ACCESS POLICY
      ↓
ADAPTER
      ↓
ACQUISITION ORCHESTRATION
      ↓
RAW EVIDENCE VAULT
      ↓
STRUCTURAL VALIDATION
      ↓
CANONICAL NORMALISATION
      ↓
ENTITY & CLASSIFICATION RESOLUTION
      ↓
QUALITY ASSESSMENT
      ↓
PROVENANCE
      ↓
OBSERVATION STORE
      ↓
EVIDENCE GRAPH
      ↓
ANALYSIS
      ↓
COMMERCIAL INTELLIGENCE PRODUCTS
```

External providers SHALL remain replaceable.

Provider schemas SHALL never become Pulse's canonical domain model.

Every acquired datum SHALL retain sufficient provenance, temporal meaning, classification and licensing metadata to support defensible downstream research.

---

# 3. Commercial Architectural Thesis

The primary commercial asset SHALL NOT be raw public data.

Raw public data can often be obtained elsewhere.

The commercial asset SHALL be the **transformation from fragmented evidence into decision-grade intelligence**.

The economic value chain is:

```text
DATA
    low differentiation

↓

CLEAN DATA
    useful

↓

NORMALISED DATA
    more useful

↓

LINKED EVIDENCE
    scarce

↓

CONTEXTUAL ANALYSIS
    valuable

↓

OPPORTUNITY / RISK
    commercially meaningful

↓

RECOMMENDATION
    decision-relevant

↓

CONTINUOUS INTELLIGENCE
    recurring revenue
```

This distinction is foundational.

Nabhold should not aspire merely to sell data that clients could download themselves.

It should sell:

```text
interpretation
comparability
timeliness
context
traceability
cross-source synthesis
commercial relevance
decision support
```

---

# 4. The Intelligence Scarcity Thesis

Pulse SHALL be particularly optimised for environments where information exists but is difficult to assemble.

This is especially relevant across many African markets, where useful evidence may be distributed across:

```text
national statistics offices
central banks
customs agencies
ministries
government gazettes
port authorities
agricultural boards
commodity exchanges
PDF publications
regional organisations
international institutions
news sources
commercial databases
industry associations
company filings
local market bulletins
```

The scarcity is often not absolute lack of data.

The scarcity is:

```text
discoverability
standardisation
machine readability
historical continuity
cross-country comparability
timely interpretation
```

Pulse SHALL be architected to monetise the reduction of those frictions.

---

# 5. Intelligence Product Factory

The Source Mesh SHALL feed a reusable **Intelligence Product Factory**.

Conceptually:

```text
QUESTION
   ↓
RESEARCH MISSION
   ↓
SOURCE PLAN
   ↓
EVIDENCE ACQUISITION
   ↓
NORMALISATION
   ↓
CORRELATION
   ↓
ANALYSIS
   ↓
CLAIMS
   ↓
INSIGHTS
   ↓
OPPORTUNITIES / RISKS
   ↓
EDITORIAL REVIEW
   ↓
INTELLIGENCE PRODUCT
```

The same underlying evidence infrastructure should support many commercial products.

---

# 6. Potential Intelligence Products

The architecture SHALL support products including, but not limited to:

| Product | Commercial Question |
|---|---|
| Market Entry Report | Should a company enter this market? |
| Export Opportunity Report | Which countries appear promising for this product? |
| Import Opportunity Report | Where can this product be competitively sourced? |
| Trade Corridor Report | Which route offers the strongest commercial combination? |
| Commodity Outlook | What forces are likely to affect price and supply? |
| Regulatory Impact Paper | What does a regulatory change mean commercially? |
| Country Intelligence Report | What commercial conditions characterize this country? |
| Sector Intelligence Paper | Where is a sector expanding or contracting? |
| Supplier Discovery Report | Which suppliers merit commercial investigation? |
| Buyer Discovery Report | Where might credible demand exist? |
| Competitor Landscape | Who appears active in the target market? |
| Pricing Intelligence | What price structure appears commercially defensible? |
| Landed Cost Intelligence | What does the product really cost after border and logistics effects? |
| Climate Exposure Report | Which locations or supply chains face climate-related exposure? |
| Investment Opportunity Paper | Which opportunities deserve deeper investment diligence? |
| Import Substitution Report | Which imports might support domestic production opportunities? |
| Export Diversification Report | Which markets could reduce dependence on existing destinations? |
| Regulatory Radar | Which upcoming rules may create risks or openings? |
| Opportunity Radar | What new commercial opportunities are emerging? |
| Executive Intelligence Brief | What has materially changed and why does it matter? |

---

# 7. The Research Mission

Pulse SHALL introduce the concept of a `ResearchMission`.

A ResearchMission represents a bounded commercial intelligence question.

Examples:

```text
Which African countries offer the strongest
five-year opportunity for specialty coffee processing?
```

```text
Could Ugandan green coffee be competitively landed
in South Africa relative to current supply origins?
```

```text
Which East African markets show evidence of
underdeveloped cold-chain infrastructure and rising demand?
```

```text
Which Southern African economies present plausible
import-substitution opportunities in fertiliser?
```

---

# 8. ResearchMission Structure

Conceptually:

```text
ResearchMission
 ├── id
 ├── title
 ├── research_question
 ├── client_scope
 ├── tenant_scope
 ├── geography_scope
 ├── market_scope
 ├── sector_scope
 ├── commodity_scope
 ├── time_horizon
 ├── decision_context
 ├── evidence_requirements
 ├── confidence_requirement
 ├── deadline
 ├── publication_profile
 ├── classification
 └── status
```

---

# 9. Research Mission Is Not a Prompt

A ResearchMission SHALL NOT be represented merely as:

```text
LLM prompt text
```

It is a structured intelligence object.

An LLM may assist execution, but the mission survives replacement of any model.

---

# 10. ResearchMission Lifecycle

```text
PROPOSED
   ↓
SCOPED
   ↓
SOURCE_PLANNED
   ↓
ACQUIRING
   ↓
ANALYSING
   ↓
REVIEW
   ↓
PUBLISHED
```

Alternative states:

```text
SUSPENDED
CANCELLED
INSUFFICIENT_EVIDENCE
SUPERSEDED
```

---

# 11. Research Question Decomposition

Pulse SHOULD decompose a commercial question into evidence questions.

Example:

```text
Should Nabhold source coffee from Uganda?
```

becomes:

```text
What volumes does Uganda export?

Which destinations currently buy?

Which coffee classifications dominate?

How have export prices moved?

What is production doing?

What are weather conditions?

What exchange-rate conditions apply?

What duties apply in South Africa?

What transport corridors exist?

What is the approximate landed cost?

Which companies appear capable of supplying?

What regulatory constraints apply?

What risks could disrupt supply?

How does this compare with competing origins?
```

This decomposition is where repeatable commercial research begins.

---

# 12. Evidence Requirements

Each ResearchMission SHALL define an EvidencePlan.

Example:

```text
EvidencePlan
 ├── mandatory domains
 ├── desirable domains
 ├── minimum independent sources
 ├── required time coverage
 ├── geography coverage
 ├── freshness requirements
 ├── source authority requirements
 ├── contradiction policy
 └── missing-evidence policy
```

---

# 13. Source Mesh

The Source Mesh SHALL be the logical collection of all registered intelligence sources available to Pulse.

It SHALL NOT imply a peer-to-peer infrastructure network.

Conceptually:

```text
                PULSE SOURCE MESH

 ┌───────────────────────────────────────────┐
 │ OFFICIAL STATISTICS                       │
 │ World Bank · IMF · NSOs · central banks  │
 ├───────────────────────────────────────────┤
 │ TRADE & CUSTOMS                           │
 │ WTO · customs · tariff sources           │
 ├───────────────────────────────────────────┤
 │ COMMODITIES & MARKETS                     │
 │ exchanges · boards · price feeds         │
 ├───────────────────────────────────────────┤
 │ WEATHER & EARTH OBSERVATION               │
 │ climate · rainfall · satellite            │
 ├───────────────────────────────────────────┤
 │ COMPANY & OWNERSHIP                       │
 │ registries · LEI · filings               │
 ├───────────────────────────────────────────┤
 │ GEOSPATIAL & INFRASTRUCTURE               │
 │ roads · ports · borders · facilities     │
 ├───────────────────────────────────────────┤
 │ NEWS & EVENTS                             │
 │ publishers · feeds · event sources       │
 ├───────────────────────────────────────────┤
 │ REGULATION                                │
 │ gazettes · ministries · regulators       │
 ├───────────────────────────────────────────┤
 │ BAOBAB INTERNAL                           │
 │ Medusa · iDempiere · Payload             │
 └───────────────────────────────────────────┘
```

---

# 14. Source Classes

Every DataSource SHALL be assigned a source class.

Canonical classes SHOULD include:

```text
OFFICIAL_PRIMARY
OFFICIAL_SECONDARY
INTERGOVERNMENTAL
REGULATED_MARKET
COMMERCIAL_DATA
INDUSTRY_ASSOCIATION
ACADEMIC
NEWS_PRIMARY
NEWS_SECONDARY
OPEN_COMMUNITY
COMPANY_DISCLOSURE
BAOBAB_INTERNAL
TENANT_INTERNAL
HUMAN_RESEARCH
OTHER
```

---

# 15. Primary versus Secondary Evidence

Pulse SHALL distinguish primary from secondary information.

Example:

```text
government gazette
```

may be primary evidence of regulation.

A news article describing the gazette is secondary evidence.

Both may be useful.

They SHALL not be treated identically.

---

# 16. Source Authority Does Not Equal Accuracy

Official status increases contextual authority.

It does not eliminate:

```text
revision
error
delay
methodological change
incompleteness
political or institutional limitations
```

Pulse SHALL preserve independent quality assessment.

---

# 17. Source Registry

All production sources SHALL be registered.

A `DataSource` SHALL have a SourceRegistry entry before production ingestion.

Conceptual fields:

```text
source_id
data_source_id
name
provider
domain
jurisdiction
authority_class
access_method
endpoint
authentication
licence
commercial_use_right
redistribution_right
attribution_requirement
retention_right
refresh_frequency
expected_latency
data_format
schema_version
classification
quality_profile
credential_reference
rate_limit
terms_version
status
```

---

# 18. Commercial-Use Gate

This is a mandatory architectural control.

Before source data may participate in a **commercially sold IntelligenceProduct**, Pulse SHALL determine whether use is compatible with the relevant:

```text
licence
terms of service
copyright
database right
contract
attribution requirement
redistribution restriction
```

---

# 19. Raw Data Is Not Automatically Resellable

The fact that Pulse can technically acquire data SHALL NOT imply that Nabhold can commercially redistribute it.

The architecture therefore SHALL distinguish:

```text
CAN_ACQUIRE
CAN_STORE
CAN_TRANSFORM
CAN_ANALYSE
CAN_QUOTE
CAN_DISPLAY
CAN_REDISTRIBUTE
CAN_SELL_DERIVED_WORK
```

These are separate rights.

---

# 20. LicenceProfile

Every commercial source SHALL carry a `LicenceProfile`.

Conceptually:

```text
LicenceProfile
 ├── licence_type
 ├── commercial_use
 ├── transformation_allowed
 ├── redistribution_allowed
 ├── attribution_required
 ├── share_alike
 ├── retention_allowed
 ├── derivative_database_rules
 ├── geographic_restrictions
 ├── expiry
 ├── evidence_reference
 └── reviewed_at
```

---

# 21. Licence Is Part of Provenance

Licensing information SHALL travel with source provenance.

This avoids producing a commercially valuable report and only afterward discovering that source material cannot lawfully be redistributed in the intended form.

---

# 22. Open Data Does Not Mean No Obligations

For example, OpenStreetMap makes its database available under ODbL and requires attribution; derivative-database obligations may also matter depending on the form of use. Pulse therefore SHALL treat licence obligations as machine-readable policy rather than merely a URL saved in documentation.

---

# 23. Source Commercial Classification

Pulse SHOULD classify source commercial rights as:

```text
OPEN_COMMERCIAL
OPEN_WITH_ATTRIBUTION
OPEN_SHARE_ALIKE
PUBLIC_ACCESS_RESTRICTED_REUSE
COMMERCIAL_LICENSE
INTERNAL_ONLY
CLIENT_LICENSED
UNKNOWN
PROHIBITED
```

`UNKNOWN` SHALL be treated conservatively.

---

# 24. Adapter Architecture

Every external integration SHALL implement a standard Source Adapter Contract.

Conceptually:

```text
SourceAdapter
 ├── describe()
 ├── discover_datasets()
 ├── validate_configuration()
 ├── validate_credentials()
 ├── plan_acquisition()
 ├── acquire()
 ├── checkpoint()
 ├── resume()
 ├── report_rate_limit()
 ├── report_source_health()
 └── close()
```

The exact Python interface will be defined in a later implementation specification.

---

# 25. Adapter Responsibility

Adapters own:

```text
provider authentication
request construction
pagination
provider-specific rate limiting
provider-specific cursoring
transport retries
response decoding
source schema validation
provider errors
source metadata capture
```

Adapters SHALL NOT own:

```text
canonical business interpretation
cross-source entity resolution
opportunity scoring
risk scoring
report writing
tenant decisions
```

---

# 26. Anti-Corruption Boundary

Every adapter SHALL terminate provider semantics before canonicalisation.

```text
Provider Model
     ↓
Provider Adapter
     ↓
Source Record
     ↓
Canonical Normaliser
     ↓
Pulse Observation
```

---

# 27. Provider Replaceability

A commercial capability SHALL not depend exclusively on one provider where a reasonable alternative exists.

Example:

```text
FX Capability
    ├── Provider A
    ├── Provider B
    └── Central Bank
```

The research question asks:

```text
give me the appropriate FX observation
```

not:

```text
call Vendor X
```

---

# 28. Capability-Based Acquisition

Sources SHALL expose capabilities.

Examples:

```text
FX_REFERENCE_RATE
FX_INTRADAY_RATE

COMMODITY_SPOT_PRICE
COMMODITY_FUTURES_PRICE

TRADE_BILATERAL_FLOW
TRADE_PRODUCT_FLOW

TARIFF_APPLIED
TARIFF_BOUND

WEATHER_HISTORICAL
WEATHER_FORECAST

COMPANY_IDENTITY
COMPANY_OWNERSHIP

NEWS_SEARCH
REGULATION_PUBLICATION

ROAD_NETWORK
PORT_LOCATION
```

---

# 29. Source Selection Resolver

Pulse SHALL implement a SourceSelectionPolicy capable of choosing between alternative sources.

Selection criteria MAY include:

```text
authority
freshness
historical coverage
geography
cost
quality
licence
commercial rights
latency
availability
precision
client requirement
```

---

# 30. Source Substitution

If a preferred source fails, a permitted substitute MAY be used.

Substitution SHALL be recorded in provenance.

Pulse SHALL never silently pretend that:

```text
Source B
```

was:

```text
Source A
```

---

# 31. Source Tiers

A useful operational hierarchy SHALL be:

```text
TIER 1 — FOUNDATIONAL
critical recurring sources

TIER 2 — ENRICHMENT
valuable but substitutable sources

TIER 3 — SPECIALIST
sector-specific or niche providers

TIER 4 — INVESTIGATIVE
sources discovered for individual research missions
```

---

# 32. Data Access Modes

Adapters SHALL support, where applicable:

```text
REST
GraphQL
SOAP
SDMX
WebSocket
SFTP
FTP
RSS
Atom
CSV
JSON
XML
XLSX
Parquet
GeoJSON
Shapefile
GeoPackage
event streams
webhooks
bulk download
manual upload
```

---

# 33. Authorised Web Extraction

Some commercially important information will not have APIs.

Pulse MAY support authorised web extraction where:

```text
terms permit
robots/access policy permits where applicable
legal review permits
source stability justifies it
```

Scraping SHALL be a last-mile adapter concern, not a primary architecture.

---

# 34. PDF and Publication Sources

Many governments and regulators publish crucial information in:

```text
PDF
gazette
circular
bulletin
notice
report
```

Pulse SHALL support document acquisition as a first-class source mode.

The original document SHALL remain available as evidence where legally permitted.

---

# 35. Source Document Model

Acquired publications SHOULD create:

```text
SourceDocument
 ├── source
 ├── title
 ├── publication_date
 ├── retrieved_at
 ├── jurisdiction
 ├── language
 ├── media_type
 ├── content_hash
 ├── storage_reference
 ├── licence
 └── provenance
```

---

# 36. Structural Extraction

A SourceDocument MAY produce:

```text
text blocks
tables
headings
dates
named entities
regulatory clauses
measurements
```

through versioned extraction methods.

The extracted representation SHALL never replace the original evidence object.

---

# 37. The Raw Evidence Vault

Raw acquired artefacts SHALL be preserved in a logically distinct **Raw Evidence Vault** where licensing and retention rules allow.

The vault's purpose is:

```text
reproducibility
audit
reprocessing
source-change detection
dispute resolution
future extraction
```

---

# 38. Raw Evidence Immutability

Raw evidence SHALL be append-oriented.

A provider correction creates a new artefact.

It does not silently rewrite the prior artefact.

---

# 39. Content Hashing

Every preservable artefact SHOULD receive a cryptographic content hash.

This provides:

```text
duplicate detection
change detection
integrity verification
provenance support
```

---

# 40. Acquisition Envelope

Every acquired artefact SHALL carry an AcquisitionEnvelope.

Conceptually:

```text
AcquisitionEnvelope
 ├── source_id
 ├── dataset_id
 ├── acquisition_id
 ├── adapter_version
 ├── source_external_id
 ├── requested_at
 ├── retrieved_at
 ├── source_published_at
 ├── source_modified_at
 ├── HTTP/source metadata
 ├── content_hash
 ├── licence_profile
 └── classification
```

---

# 41. Acquisition Modes

The Source Mesh SHALL support:

```text
LIVE
SCHEDULED
EVENT_DRIVEN
BACKFILL
REPROCESS
CORRECTION
MANUAL_RESEARCH
ON_DEMAND
```

---

# 42. Scheduling

Scheduling SHALL be source-specific.

Examples:

```text
FX                  minutes / hours
news                minutes
weather forecasts   hours
commodity data      market-dependent
regulatory feeds    hours / event-driven
trade statistics    monthly / annual
GDP                  quarterly / annual
company registry    daily / on-demand
```

There SHALL be no universal "refresh every hour" policy.

---

# 43. Freshness Policy

Each Dataset SHALL define:

```text
expected_publication_frequency
target_ingestion_latency
freshness_window
stale_after
critical_stale_after
```

---

# 44. Data Vintage

Economic and statistical sources SHALL support `data_vintage`.

Pulse must be capable of distinguishing:

```text
GDP estimate published March
```

from:

```text
revised GDP estimate published June
```

even if both concern the same quarter.

---

# 45. Revision Awareness

Revised source values SHALL generate new canonical versions.

A research paper published in March must remain reproducible using the March evidence vintage.

---

# 46. Provider Schema Drift

Adapters SHALL detect schema change.

The adapter SHALL distinguish:

```text
new optional field
renamed field
removed field
changed type
changed meaning
new enumeration
```

---

# 47. Schema Quarantine

Unexpected schema changes SHOULD result in:

```text
QUARANTINED acquisition
```

rather than silently producing malformed canonical observations.

---

# 48. Adapter Certification

Production adapters SHOULD have certification tests containing:

```text
known provider fixtures
schema validation
pagination behaviour
error behaviour
rate-limit behaviour
idempotency
normalisation examples
```

---

# 49. Source Health

Each DataSource SHALL expose health indicators.

Examples:

```text
availability
latest successful acquisition
latency
error rate
schema drift
freshness
record count anomaly
rate-limit state
credential expiry
```

---

# 50. Source Reliability History

Pulse SHOULD maintain historical reliability statistics.

This enables the engine to learn:

```text
which sources are frequently late
which frequently revise data
which frequently fail
which produce contradictory values
```

---

# 51. Source Cost

Commercial sources SHALL expose acquisition cost metadata.

Conceptually:

```text
subscription_cost
request_cost
record_cost
compute_cost
storage_cost
```

where applicable.

---

# 52. Intelligence Unit Economics

Research execution SHOULD eventually be able to estimate:

```text
data acquisition cost
+
model cost
+
compute cost
+
analyst effort
+
editorial effort
=
production cost
```

against:

```text
product revenue
```

This permits commercial product profitability to become measurable rather than anecdotal.

---

# 53. Normalisation Layer

Provider data SHALL pass through normalisation before becoming canonical Observations.

Normalisation MAY include:

```text
field mapping
unit conversion
currency representation
date conversion
geographic mapping
product classification
entity resolution
missing-value semantics
text encoding
precision handling
```

---

# 54. Preserve Source and Canonical Values

For material transformations Pulse SHALL preserve:

```text
source_value
source_unit
canonical_value
canonical_unit
transformation_reference
```

---

# 55. No False Precision

If a source reports:

```text
1.2 million tonnes
```

Pulse SHALL not transform this into:

```text
1,200,000.000000 tonnes
```

and imply nonexistent precision.

---

# 56. Currency Normalisation

Monetary comparisons SHALL retain source currency.

Any conversion SHALL record:

```text
conversion currency
FX observation
conversion timestamp
conversion method
```

---

# 57. Commodity Normalisation

Commodity observations SHALL preserve:

```text
commodity
grade
variety
contract
benchmark
delivery basis
origin
unit
currency
market
```

A coffee price without grade/origin/basis may be analytically misleading.

---

# 58. Trade Classification

Trade data SHALL preserve:

```text
classification system
classification revision
commodity code
reporter
partner
flow
period
value
quantity
net weight
```

HS codes SHALL always be interpreted together with their HS revision.

---

# 59. Classification Concordance

Pulse SHOULD support concordances such as:

```text
HS2017 ↔ HS2022
ISIC ↔ national classifications
provider commodity codes ↔ canonical commodities
```

Mapping uncertainty SHALL remain explicit.

---

# 60. Geographic Resolution

Provider geographies SHALL resolve against canonical geography.

Examples:

```text
ZA
ZAF
South Africa
Republic of South Africa
```

may resolve to one canonical country.

But:

```text
Congo
```

must not be guessed without sufficient context.

---

# 61. Geographic Hierarchy

Pulse SHOULD support:

```text
continent
regional bloc
country
province/state
district
municipality
locality
facility/site
coordinates
```

---

# 62. Regional Economic Groupings

Research may require groupings such as:

```text
SADC
EAC
COMESA
AfCFTA
EU
BRICS
```

Membership SHALL be time-aware where historically relevant.

---

# 63. Entity Resolution

External company identities SHALL be resolved through:

```text
exact identifiers
registry numbers
LEI
tax IDs where lawful
names
addresses
domain names
ownership relationships
```

Canonical platform mapping authority remains with the Control Plane.

GLEIF, for example, exposes LEI reference and ownership information and supports fuzzy matching of names and addresses, making it a useful source in the entity-resolution fabric without making GLEIF identifiers Baobab canonical IDs.

---

# 64. Candidate Resolution

Uncertain entity matches SHALL create:

```text
CandidateResolution
```

not an authoritative mapping.

---

# 65. Resolution Confidence

CandidateResolution SHALL include:

```text
candidate
method
features
confidence
status
```

A probable match is not a confirmed identity.

---

# 66. Internal Data Integration

Pulse SHALL consume authorised data from:

```text
Payload CMS
MedusaJS
iDempiere
```

through the same evidence philosophy.

Internal data is not exempt from provenance.

---

# 67. Internal Source Advantage

External evidence becomes more commercially valuable when connected to private operational context.

Example:

```text
public coffee benchmark
+
public FX
+
public tariff
+
tenant freight cost
+
tenant sales demand
+
tenant inventory
```

can produce intelligence unavailable from public sources alone.

---

# 68. Public Commercial Products versus Private Advisory Products

The architecture SHALL distinguish:

```text
PUBLISHED INTELLIGENCE
```

based predominantly on reusable evidence,

from:

```text
PRIVATE CLIENT INTELLIGENCE
```

that may combine public sources with confidential client data.

---

# 69. Product Isolation

Confidential evidence used in one client's advisory report SHALL not leak into another client's product.

---

# 70. The Claim Registry

Pulse SHALL introduce a canonical `Claim` concept for formal research publication.

A Claim represents a proposition intended to appear in an intelligence product.

Example:

```text
Uganda's coffee exports to market X
have grown over the last five reported years.
```

---

# 71. Claim Structure

```text
Claim
 ├── statement
 ├── claim_type
 ├── evidence_set
 ├── analysis_reference
 ├── confidence
 ├── temporal_scope
 ├── geographic_scope
 ├── limitations
 ├── status
 └── publication_reference
```

---

# 72. Claim Lifecycle

```text
DRAFT
 ↓
EVIDENCED
 ↓
REVIEWED
 ↓
APPROVED
 ↓
PUBLISHED
```

or:

```text
REJECTED
RETRACTED
SUPERSEDED
```

---

# 73. Why Claims Matter

Commercial research must distinguish:

```text
narrative prose
```

from:

```text
evidence-bearing assertions
```

A report paragraph may contain five claims.

Each important claim should be independently traceable.

---

# 74. Citation Graph

Pulse SHALL be capable of producing a CitationGraph:

```text
Report
  ↓
Section
  ↓
Claim
  ↓
EvidenceSet
  ↓
Observation / Document
  ↓
Source
```

This is essential to professional-grade commercial research.

---

# 75. Research Reproducibility

Every commercial paper SHOULD be capable of recording a `ResearchSnapshot`.

```text
ResearchSnapshot
 ├── mission
 ├── source versions
 ├── dataset vintages
 ├── evidence sets
 ├── methods
 ├── model versions
 ├── analyst revisions
 └── publication date
```

---

# 76. Re-running Historical Research

Pulse SHOULD eventually support:

```text
REPRODUCE AS PUBLISHED
```

and:

```text
RE-RUN WITH LATEST DATA
```

as separate operations.

This would become a powerful commercial feature.

---

# 77. Living Reports

A major strategic capability SHALL be the **Living Intelligence Product**.

Instead of selling only:

```text
PDF once
```

Pulse should support:

```text
initial report
+
continuous evidence refresh
+
change detection
+
updated conclusions
+
alerts
+
periodic revised paper
```

---

# 78. From Consulting Revenue to Recurring Revenue

The commercial evolution can therefore be:

```text
ONE-OFF REPORT
      ↓
QUARTERLY UPDATE
      ↓
SUBSCRIPTION INTELLIGENCE
      ↓
CONTINUOUS MONITORING
      ↓
CLIENT-SPECIFIC DECISION SUPPORT
```

The architecture SHALL permit this progression without replacing the canonical model.

---

# 79. Report as Versioned Intelligence Product

A report SHALL have:

```text
Report
 ├── report_id
 ├── IntelligenceProduct
 ├── version
 ├── ResearchMission
 ├── ResearchSnapshot
 ├── claims
 ├── publication_date
 ├── author/reviewer
 ├── audience
 ├── classification
 ├── citation manifest
 └── licence notices
```

---

# 80. Editorial Workflow

Automation alone SHALL NOT determine publication quality.

Commercial papers SHOULD support:

```text
machine analysis
      ↓
analyst review
      ↓
subject-matter review
      ↓
editorial review
      ↓
publication approval
```

depending on product class.

---

# 81. Payload CMS Relationship

Where Payload CMS is used for publication, Pulse SHALL provide structured research outputs to Payload.

Payload remains authoritative for:

```text
publication
editorial state
presentation
web content
```

Pulse remains authoritative for:

```text
claims
evidence
analysis
intelligence
```

---

# 82. Report Templates

Commercial templates MAY include:

```text
Executive Summary
Market Definition
Evidence Base
Historical Context
Demand Analysis
Supply Analysis
Trade Structure
Pricing
Competition
Regulation
Logistics
Macroeconomic Context
Risk
Opportunity
Scenarios
Recommendation
Methodology
Sources
Limitations
```

---

# 83. Machine-Readable Report

The report SHALL not exist only as prose.

A report SHOULD have a structured machine-readable representation so that:

```text
charts
tables
citations
claims
insights
risks
recommendations
```

can be re-rendered into different formats.

---

# 84. Publication Formats

Potential outputs include:

```text
HTML
PDF
web article
API
dashboard
presentation
email brief
data appendix
machine-readable JSON
```

---

# 85. Commercial Product Tiers

Pulse SHOULD eventually support a commercial hierarchy such as:

```text
PULSE SNAPSHOT
low-cost concise intelligence

PULSE BRIEF
focused analytical paper

PULSE REPORT
full market intelligence report

PULSE DEEP DIVE
sector/country/product investigation

PULSE ADVISORY
client-specific intelligence

PULSE MONITOR
recurring intelligence subscription

PULSE SIGNAL
event/alert subscription

PULSE DATA
licensed derived datasets where permitted
```

Names remain commercial proposals rather than binding product brands.

---

# 86. Opportunity Radar

One flagship product SHOULD be `Opportunity Radar`.

Conceptually:

```text
TRADE GROWTH
      +
MARKET SIZE
      +
PRICE SPREAD
      +
SUPPLY AVAILABILITY
      +
MACRO CONDITIONS
      +
REGULATORY CONDITIONS
      +
LOGISTICS
      +
COMPETITION
      ↓
OPPORTUNITY CANDIDATE
```

---

# 87. Opportunity Candidate

An Opportunity Candidate is not yet an Opportunity.

It represents a screening result requiring deeper investigation.

This prevents simplistic scoring from becoming commercial advice.

---

# 88. Opportunity Funnel

```text
UNIVERSE
  ↓
SCREEN
  ↓
CANDIDATES
  ↓
EVIDENCE ENRICHMENT
  ↓
QUALIFICATION
  ↓
OPPORTUNITY
  ↓
RECOMMENDATION
```

---

# 89. Market Opportunity Scoring

An illustrative scoring framework MAY combine:

```text
market_growth
market_size
import_dependency
price_attractiveness
competitive_intensity
logistics_accessibility
currency_stability
regulatory_friction
political/economic risk
supplier availability
strategic fit
```

No universal scoring formula SHALL be hard-coded as truth.

Scoring methodology SHALL be product-specific and versioned.

---

# 90. Import Substitution Radar

Pulse SHOULD support detection of situations where:

```text
high recurring imports
+
available domestic/regional capability
+
significant landed cost
+
policy incentives
```

suggest possible local production opportunity.

This could be commercially valuable to:

```text
investors
manufacturers
development agencies
governments
banks
```

---

# 91. Export Discovery Radar

Possible logic:

```text
domestic production capability
+
foreign import growth
+
favourable tariffs
+
manageable logistics
+
competitive pricing
+
low current exporter penetration
```

↓

```text
potential export opportunity
```

---

# 92. Trade Corridor Intelligence

Pulse SHOULD treat the trade corridor itself as an analytical object.

Example:

```text
Kampala
 → Mombasa
 → Durban/Cape Town
```

or alternative corridors.

Potential factors:

```text
distance
ports
border crossings
transit times
freight rates
customs complexity
weather disruption
security
infrastructure
historical reliability
```

---

# 93. Corridor Comparison

A commercial report could compare:

```text
CORRIDOR A
vs
CORRIDOR B
vs
CORRIDOR C
```

using a versioned methodology.

This moves Pulse beyond generic macroeconomic reports into operational commercial intelligence.

---

# 94. Landed Cost Intelligence

Pulse SHOULD ultimately support:

```text
supplier price
+
packaging
+
inland freight
+
export fees
+
port costs
+
ocean/road freight
+
insurance
+
tariff
+
tax
+
brokerage
+
FX
+
destination transport
```

↓

```text
estimated landed cost
```

Every component must carry its own source and validity.

---

# 95. Regulation-to-Opportunity Pipeline

Regulation should not be treated only as compliance burden.

Pulse SHOULD detect:

```text
new incentive
new tariff
new localisation rule
new standard
new subsidy
new procurement preference
new import restriction
```

that may create commercial openings.

---

# 96. Regulatory Delta

Pulse SHOULD represent:

```text
OLD RULE
   ↓
CHANGE
   ↓
NEW RULE
```

rather than only storing the latest document.

---

# 97. Regulatory Impact Mapping

A RegulatoryChange MAY be mapped to:

```text
countries
markets
sectors
commodities
products
companies
supply chains
```

to determine potentially affected intelligence products.

---

# 98. Regulatory Alert Product

This enables a commercial product:

```text
REGULATORY PULSE
```

that answers:

> What changed, who may be affected, when does it take effect, and what commercial consequence might follow?

---

# 99. Company Intelligence

Company registry and legal-entity data SHOULD feed:

```text
supplier discovery
buyer discovery
counterparty research
ownership analysis
competitor landscape
market concentration analysis
```

---

# 100. Company Evidence Caution

Registry existence SHALL not automatically imply:

```text
creditworthiness
operational capability
trustworthiness
```

Those require additional evidence.

---

# 101. Supplier Discovery Funnel

```text
REGISTRY
   ↓
identity candidates
   ↓
industry/product evidence
   ↓
trade evidence
   ↓
location evidence
   ↓
activity evidence
   ↓
risk evidence
   ↓
supplier candidate
   ↓
human due diligence
```

---

# 102. News Intelligence

News SHALL serve primarily as:

```text
event detection
early warning
narrative context
entity activity evidence
```

rather than sole factual authority for consequential claims.

---

# 103. Event Clustering

Pulse SHOULD cluster multiple articles referring to the same event.

This avoids interpreting:

```text
50 articles
```

as:

```text
50 independent events
```

---

# 104. News Corroboration

News-derived claims SHOULD track:

```text
independent publishers
original source
syndication relationships
publication times
```

where determinable.

---

# 105. Narrative versus Evidence

A widespread media narrative can itself be analytically relevant.

However:

```text
people are talking about X
```

and:

```text
X is objectively true
```

are different claims.

---

# 106. Climate Intelligence

Weather and climate data SHALL support:

```text
agricultural supply risk
transport disruption
energy demand
water stress
location analysis
insurance context
infrastructure exposure
```

Copernicus' Climate Data Store already provides programmatic retrieval mechanisms and dataset-oriented processing, demonstrating the feasibility of treating environmental information as a structured source class.

---

# 107. Weather versus Climate

Pulse SHALL distinguish:

```text
WEATHER
short-term conditions

CLIMATE
long-term statistical conditions

FORECAST
future model output

REANALYSIS
historically reconstructed atmospheric state
```

---

# 108. Geospatial Intelligence

Geospatial evidence can answer:

```text
where demand is located
where production occurs
where roads exist
where ports exist
where border crossings occur
where infrastructure is absent
where climate exposure overlaps assets
```

---

# 109. Spatial Join

Pulse SHOULD eventually support analyses such as:

```text
warehouse locations
     ∩
road network
     ∩
population density
     ∩
market demand
```

and:

```text
farms
     ∩
rainfall anomaly
     ∩
commodity supply
```

---

# 110. Infrastructure Gap Intelligence

Combining:

```text
population
economic activity
trade
roads
ports
energy
warehousing
cold-chain
```

may reveal infrastructure gaps.

This creates potential research products for:

```text
developers
investors
banks
governments
logistics companies
development institutions
```

---

# 111. Government Open-Data Intelligence

Government open data SHALL not merely be warehoused.

Pulse SHOULD detect:

```text
procurement
budget allocation
infrastructure project
licence issuance
planning changes
tender activity
agricultural statistics
investment programmes
```

where lawful and available.

---

# 112. Public Procurement Intelligence

A future specialist product MAY identify:

```text
recurring procurement demand
procurement concentration
supplier patterns
regional purchasing gaps
upcoming tenders
```

subject to source quality and applicable procurement rules.

---

# 113. Project Pipeline Intelligence

Combining:

```text
development-bank projects
government capital budgets
public tenders
construction permits
company activity
```

may reveal emerging project pipelines before their commercial effect becomes obvious.

---

# 114. Foreign Exchange Intelligence

FX data SHALL support more than displaying current rates.

Pulse SHOULD derive:

```text
volatility
trend
drawdown
currency exposure
landed-cost effect
margin sensitivity
scenario analysis
```

---

# 115. Commodity Intelligence

Commodity data SHOULD support:

```text
benchmark movement
basis comparisons
origin differentials
seasonality
volatility
supply-demand context
```

---

# 116. Commodity-to-Company Intelligence

A particularly valuable capability is mapping commodity movements to businesses.

Example:

```text
fertiliser price rises
       ↓
affected agricultural sectors
       ↓
affected markets
       ↓
companies exposed
       ↓
potential procurement opportunity / risk
```

---

# 117. Macroeconomic Intelligence

The macro layer SHALL provide context rather than dominate every conclusion.

World Bank and IMF datasets are appropriate examples of machine-readable macroeconomic foundations; World Bank's API provides metadata such as indicator codes, names, source organisations and topics, which supports evidence-aware canonicalisation rather than treating numbers as anonymous values.

---

# 118. Macro-to-Micro Translation

The commercially interesting question is not merely:

```text
inflation is 7%
```

but:

```text
what does this inflation environment
mean for this sector,
this market,
this company,
this product,
this procurement decision?
```

Pulse SHALL be designed for this translation.

---

# 119. Country Intelligence Graph

Pulse SHOULD eventually maintain a dynamic evidence graph for each country:

```text
COUNTRY
 ├── macroeconomics
 ├── trade
 ├── currency
 ├── regulation
 ├── companies
 ├── infrastructure
 ├── commodities
 ├── climate
 ├── politics/events
 ├── logistics
 └── market opportunities
```

---

# 120. Sector Intelligence Graph

Likewise:

```text
SECTOR
 ├── production
 ├── demand
 ├── imports
 ├── exports
 ├── companies
 ├── prices
 ├── regulation
 ├── supply chain
 ├── capital flows
 └── opportunities
```

---

# 121. The Opportunity Graph

Longer term, Pulse should be capable of asking:

```text
Which Market
imports which Product
from which Country
at what Price
through which Corridor
under which Tariff
from which Suppliers
while which Regulations
and which Risks
are changing?
```

That graph is potentially far more valuable than any individual source API.

---

# 122. Evidence Graph

The underlying structure can be conceptualised as:

```text
ENTITY
  │
  ├── OBSERVATION
  │       │
  │       └── SOURCE
  │
  ├── EVENT
  │       │
  │       └── SOURCE DOCUMENT
  │
  ├── SIGNAL
  │
  ├── INSIGHT
  │
  ├── RISK
  │
  └── OPPORTUNITY
```

A dedicated graph database is NOT required by this ADR.

The graph is semantic before it is technological.

---

# 123. Data Moat

Pulse's durable moat should accumulate in:

```text
source integrations
+
source reliability history
+
normalisation mappings
+
entity mappings
+
classification concordances
+
historical vintages
+
quality assessments
+
research methods
+
validated claims
+
analyst feedback
+
outcome feedback
```

No single component is sufficient.

Together, they become difficult to reproduce quickly.

---

# 124. Methodology Library

Commercial research SHALL build a reusable `MethodologyLibrary`.

Examples:

```text
MarketAttractivenessMethod
ExportOpportunityMethod
ImportSubstitutionMethod
SupplierScreeningMethod
CountryRiskMethod
RegulatoryImpactMethod
CorridorComparisonMethod
LandedCostMethod
CommodityExposureMethod
```

---

# 125. Method Versioning

Every published score or ranking SHALL identify the methodology version.

If Nabhold improves the methodology:

```text
v1
→
v2
```

historical reports remain reproducible under v1.

---

# 126. Methodology as Intellectual Property

The implementation code may be software.

But the commercially valuable intellectual property increasingly becomes:

```text
which evidence matters
how it is cleaned
how signals are defined
how factors are weighted
how uncertainty is represented
how conclusions are reviewed
```

Pulse SHALL preserve methodology as a first-class asset.

---

# 127. Research Corpus

Published and internal approved research SHALL create a reusable ResearchCorpus.

The corpus may support:

```text
historical comparison
cross-country comparison
method evaluation
LLM retrieval
institutional memory
analyst onboarding
client continuity
```

---

# 128. Research Memory

Pulse SHALL distinguish durable research memory from model conversational memory.

Research memory is:

```text
structured
versioned
citable
authorised
persistent
```

---

# 129. Evidence Reuse

The same Observation may support multiple ResearchMissions.

This dramatically reduces marginal research cost.

---

# 130. Incremental Intelligence Economics

Once foundational datasets are continuously maintained:

```text
Report 1
requires major source establishment

Report 10
reuses much of the evidence infrastructure

Report 100
may require primarily new analysis and review
```

This is one of the principal economic arguments for building Pulse as infrastructure rather than repeatedly producing research manually.

---

# 131. Human Analyst Leverage

Pulse SHALL seek to amplify analysts rather than remove them.

A skilled analyst should spend less time:

```text
downloading
copying
cleaning
renaming columns
reformatting charts
finding yesterday's source
```

and more time:

```text
questioning
interpreting
challenging
validating
writing
advising
```

---

# 132. Analyst Workbench

A future Analyst Workbench MAY expose:

```text
Research Missions
Evidence Plans
source status
observations
charts
contradictions
claims
citations
insights
draft sections
methodology
review comments
```

It SHALL consume Pulse APIs rather than define canonical truth.

---

# 133. LLM Research Assistant

An LLM MAY assist an analyst by:

```text
suggesting sources
summarising evidence
extracting tables
identifying contradictions
drafting claims
generating questions
drafting prose
```

but every consequential claim SHALL resolve back to evidence.

---

# 134. The LLM Must Be Able to Say "Insufficient Evidence"

This is a requirement, not a failure.

Pulse SHALL allow:

```text
INSUFFICIENT_EVIDENCE
```

as a legitimate research conclusion.

---

# 135. No Synthetic Citation

LLMs SHALL NEVER fabricate citations.

Citation references MUST resolve to objects in the Evidence/Citation graph.

---

# 136. No Model-Memory Evidence

A model's pretrained knowledge SHALL not itself be treated as publishable evidence for a commercial research claim.

It may guide investigation.

It does not replace sourcing.

---

# 137. Source Discovery Agent

A future Source Discovery Agent MAY search for new candidate sources.

Its results SHALL enter:

```text
CANDIDATE_SOURCE
```

state.

They SHALL require validation before production acquisition.

---

# 138. Source Onboarding Lifecycle

```text
DISCOVERED
   ↓
ASSESSED
   ↓
LICENCE_REVIEW
   ↓
TECHNICALLY_VALIDATED
   ↓
QUALITY_VALIDATED
   ↓
APPROVED
   ↓
ACTIVE
```

Possible exits:

```text
REJECTED
SUSPENDED
RETIRED
```

---

# 139. Source Scorecard

Every candidate source MAY be scored on:

```text
authority
coverage
freshness
continuity
accessibility
machine readability
historical depth
geographic coverage
commercial rights
cost
reliability
```

---

# 140. Source Portfolio Management

Source acquisition is a portfolio.

Pulse SHOULD know:

```text
which capability has one source
which has three
which has no fallback
which relies on fragile scraping
which has expensive licensing
```

---

# 141. Source Concentration Risk

Dependence on one commercial provider is itself an operational risk.

Pulse SHOULD generate internal source-risk signals.

---

# 142. Provider Lock-In Rule

Provider-specific identifiers and schemas SHALL be confined to adapter and mapping layers.

---

# 143. Paid Data Sources

Commercial sources MAY be introduced when:

```text
quality
timeliness
coverage
legal rights
or client willingness to pay
```

justify the cost.

The architecture SHALL not assume all intelligence can or should be built exclusively from free sources.

---

# 144. Open-First, Not Open-Only

The preferred acquisition strategy SHALL be:

> **Open-first where quality and rights are adequate; commercial where commercial value justifies it.**

---

# 145. Client-Provided Data

Clients MAY contribute proprietary datasets.

Such datasets SHALL be represented as DataSources with:

```text
CLIENT_LICENSED
```

rights and appropriate tenant isolation.

---

# 146. Bring-Your-Own-Data Intelligence

A valuable future advisory service could allow a client to provide:

```text
sales
procurement
inventory
supplier
customer
financial
location
```

data and combine it with the Pulse external evidence universe.

---

# 147. Intelligence Without Data Exfiltration

Client-private data SHALL remain isolated.

Only authorised derived intelligence may leave that context.

---

# 148. Research Marketplace Possibility

Longer term, the architecture MAY support an intelligence catalogue where clients purchase:

```text
existing reports
updated reports
data appendices
custom research
monitoring subscriptions
sector alerts
```

This is not required for the first implementation but SHOULD remain architecturally possible.

---

# 149. Report Reuse and Customisation

A base report may be reused as:

```text
PUBLIC BASELINE
       +
CLIENT-SPECIFIC ANALYSIS
       ↓
PRIVATE ADVISORY REPORT
```

without contaminating the public baseline with private client evidence.

---

# 150. Product Lineage

A derived client product SHALL preserve which base IntelligenceProduct/version it extended.

---

# 151. Research Quality Gate

A commercial publication SHOULD not reach `PUBLISHED` unless it satisfies product-specific gates such as:

```text
required evidence present
critical claims cited
methodology recorded
contradictions reviewed
licensing cleared
classification reviewed
freshness acceptable
analyst approval
editorial approval
```

---

# 152. Evidence Coverage

Pulse SHOULD calculate evidence coverage for a ResearchMission.

Example:

```text
Demand           100%
Supply            90%
Pricing           75%
Regulation       100%
Logistics         60%
Competition       40%
```

This is more useful than pretending every report has equal certainty.

---

# 153. Report Confidence

A report SHALL not reduce all uncertainty to one arbitrary percentage.

Confidence SHOULD be communicated by section, claim or methodology.

---

# 154. Unknowns Section

Commercial research SHOULD explicitly record:

```text
known unknowns
missing datasets
unverified assumptions
source limitations
```

This increases credibility rather than weakening the report.

---

# 155. Contradiction Register

Each ResearchMission SHOULD maintain:

```text
ContradictionRegister
```

for material source disagreement.

---

# 156. Example Contradiction

```text
National statistics office:
    production = X

International dataset:
    production = Y
```

Pulse SHALL preserve both and explain methodological or timing differences where known.

---

# 157. Research Audit Package

A high-value client engagement MAY optionally produce an audit package containing:

```text
methodology
source manifest
data vintages
claim register
quality notes
limitations
```

This creates differentiation from generic AI-generated market reports.

---

# 158. Confidential Research Rooms

For sensitive engagements Pulse MAY support isolated research contexts containing:

```text
client documents
private observations
restricted reports
research notes
```

under tenant-specific controls.

---

# 159. Commercial API Possibility

Certain derived intelligence MAY eventually be exposed through subscription APIs.

Examples:

```text
country opportunity scores
trade signals
regulatory change feed
commodity risk signals
market attractiveness
```

provided licensing permits derived redistribution.

---

# 160. Intelligence-as-a-Service

The long-term architectural direction therefore supports:

```text
REPORTS
+
SUBSCRIPTIONS
+
ALERTS
+
APIs
+
CUSTOM RESEARCH
+
ADVISORY
```

from one underlying evidence platform.

---

# 161. Verticalisation

Pulse SHALL be horizontally reusable but commercially verticalisable.

Potential vertical intelligence packs include:

```text
Agri & Food
Trade & Logistics
Real Estate
Infrastructure
Energy
Manufacturing
Mining
Financial Services
Retail
Tourism
Climate & Green Industry
Public Procurement
```

---

# 162. Vertical Packs

A VerticalPack MAY define:

```text
sources
indicators
taxonomies
methods
signals
report templates
opportunity rules
risk rules
```

without forking the Pulse engine.

---

# 163. Example — Coffee Intelligence Pack

```text
CoffeePack
 ├── production statistics
 ├── export flows
 ├── import flows
 ├── commodity benchmarks
 ├── grades
 ├── weather
 ├── harvest calendars
 ├── FX
 ├── ports
 ├── tariffs
 ├── buyers
 ├── suppliers
 └── regulatory requirements
```

---

# 164. Example Commercial Question

> Which African origin offers the strongest risk-adjusted green-coffee sourcing opportunity for a South African buyer over the coming twelve months?

Pulse can systematically combine:

```text
price
quality proxy
export capacity
seasonality
weather
FX
transport
tariff
supplier density
political/regulatory risk
historical reliability
```

---

# 165. Example — Green Industry Opportunity Pack

Potential evidence:

```text
energy prices
renewable resources
climate
trade
imports
carbon regulation
industrial activity
public incentives
infrastructure
company registrations
investment projects
```

Potential outputs:

```text
solar opportunity report
battery supply-chain paper
waste-processing opportunity report
green-building materials report
circular-economy opportunity radar
```

---

# 166. Example — Real Estate Intelligence Pack

Sources might combine:

```text
population
income
construction activity
land use
transport
amenities
business formation
rents
property transactions
interest rates
building permits
infrastructure projects
```

to detect:

```text
growth corridors
commercial nodes
undersupplied housing markets
warehouse demand
retail catchments
```

where credible source data exists.

---

# 167. Example — Infrastructure Intelligence

```text
trade volumes
population growth
roads
ports
industrial locations
power access
public projects
logistics bottlenecks
```

may reveal:

```text
warehouse demand
cold-chain gaps
logistics hubs
industrial parks
energy infrastructure opportunities
```

---

# 168. "Prophecy" Boundary

Pulse MAY attempt to identify weak signals before an opportunity becomes obvious.

But it SHALL never claim supernatural foresight.

The architectural analogue of prophecy is:

```text
many weak observations
+
historical patterns
+
cross-domain correlation
+
timely interpretation
+
explicit uncertainty
```

---

# 169. Weak Signal Detection

A WeakSignal MAY emerge from:

```text
small but persistent trade growth
new company registrations
regulatory consultation
planned infrastructure
unusual procurement
news activity
price divergence
weather shifts
```

No single observation need be decisive.

---

# 170. Emerging Opportunity Detection

```text
WeakSignal A
+
WeakSignal B
+
WeakSignal C
+
supporting context
       ↓
EmergingOpportunityCandidate
```

---

# 171. Time Advantage

Commercial advantage frequently comes from:

```text
seeing a meaningful pattern
earlier than competitors
```

rather than predicting an unknowable future perfectly.

Pulse SHALL therefore optimise for **time-to-detection**.

---

# 172. Detection Latency

Pulse SHOULD measure:

```text
source publication
→ acquisition
→ signal detection
→ analyst validation
→ client notification
```

---

# 173. Signal Half-Life

Some opportunities decay quickly.

Pulse SHOULD support:

```text
urgency
valid_until
decay policy
```

---

# 174. Opportunity Shelf Life

An opportunity identified from temporary:

```text
FX movement
price spread
regulatory window
supply disruption
```

may expire quickly.

The system SHALL not continue selling it as current intelligence after its validity expires.

---

# 175. Intelligence Integrity Is Commercial Strategy

Trust SHALL be regarded as a revenue capability.

Clients who make consequential decisions require confidence that:

```text
numbers are sourced
methods are explained
updates are tracked
assumptions are visible
errors can be corrected
```

---

# 176. Correction Policy

Published intelligence SHALL support formal corrections.

```text
Report v1
     ↓
Correction
     ↓
Report v1.1
```

The correction history remains visible.

---

# 177. Retraction

Materially invalid research MAY be retracted.

Retraction SHALL preserve the record that it existed and explain why it was withdrawn, subject to legal policy.

---

# 178. Commercial Research Ethics

Pulse SHALL not intentionally manufacture certainty to make reports more commercially attractive.

Marketing must not overrule evidence.

---

# 179. Source Diversity

For high-impact claims Pulse SHOULD favour independent corroboration where feasible.

Three websites repeating the same syndicated source are not necessarily three independent sources.

---

# 180. Research Independence Metadata

Sources MAY record relationships such as:

```text
SYNDICATES_FROM
DERIVES_FROM
REPUBLISHES
CITES
```

where known.

---

# 181. Source Conflict Resolution

Pulse SHALL not automatically average incompatible statistics.

Resolution requires understanding:

```text
definition
methodology
period
geography
classification
revision
```

---

# 182. Data Quality Pipeline

Every canonical Observation SHOULD pass through quality assessment:

```text
STRUCTURAL VALIDITY
      ↓
SEMANTIC VALIDITY
      ↓
TEMPORAL VALIDITY
      ↓
RANGE CHECK
      ↓
CONSISTENCY CHECK
      ↓
DUPLICATE CHECK
      ↓
SOURCE QUALITY
      ↓
CROSS-SOURCE CHECK
```

---

# 183. Anomaly versus Error

An unusual value SHALL not automatically be discarded.

It may represent:

```text
source error
```

or:

```text
real-world anomaly
```

Pulse must preserve that distinction.

---

# 184. Quarantine

Suspicious records MAY enter:

```text
QUARANTINED
```

state for review.

---

# 185. Manual Validation

Human-reviewed corrections SHALL preserve:

```text
original value
reviewer
reason
corrective action
timestamp
```

---

# 186. Acquisition Failure Model

Failures SHALL be classified.

Examples:

```text
NETWORK
AUTHENTICATION
RATE_LIMIT
PROVIDER_OUTAGE
SCHEMA_CHANGE
INVALID_RESPONSE
LICENCE_BLOCK
QUALITY_FAILURE
STORAGE_FAILURE
UNKNOWN
```

---

# 187. Retry Policy

Retry SHALL depend on failure class.

A schema change should not be retried indefinitely as if it were a transient timeout.

---

# 188. Circuit Breakers

Adapters MAY use circuit breakers where repeated provider failure would otherwise waste resources.

---

# 189. Rate Limits

Rate limits SHALL be represented as source metadata.

Adapters SHALL not evade provider restrictions.

---

# 190. Credential Isolation

API keys and credentials SHALL be externalised through approved secrets infrastructure.

Credentials SHALL never appear in:

```text
source code
report artefacts
logs
raw evidence
```

---

# 191. Security of External Content

External content SHALL be treated as hostile input.

Protection is required against:

```text
malformed archives
oversized documents
malicious HTML
spreadsheet formula injection
XML attacks
prompt injection
unexpected encodings
```

---

# 192. Research Prompt Injection

Documents may contain instructions intended to manipulate an AI system.

External document text SHALL never be allowed to override:

```text
system policy
tenant policy
research mission
tool permissions
source policy
```

---

# 193. Adapter Sandboxing

High-risk extraction tasks MAY be executed in isolated worker environments.

---

# 194. Data Residency

Source data and client evidence SHALL be capable of residency-aware storage according to policy.

The Source Mesh SHALL not assume every source artefact can be replicated into every region.

---

# 195. Personally Identifiable Information

Company and registry research may involve information relating to individuals.

Acquisition SHALL be:

```text
purpose-bound
lawful
minimised
classified
retained appropriately
```

---

# 196. Intelligence Product Rights Manifest

Every published product SHOULD carry an internal `RightsManifest` identifying:

```text
sources
licence obligations
required attribution
quotation limits
redistribution restrictions
commercial permissions
```

---

# 197. Attribution Automation

Where source attribution is required, Pulse SHOULD generate attribution automatically from the RightsManifest.

---

# 198. Source Removal

If a source licence expires or access is revoked:

```text
future acquisition stops
```

Historical storage/use SHALL follow the applicable licence and contract.

---

# 199. Reprocessing

When a normalisation method improves, Pulse MAY reprocess historical raw evidence.

This SHALL produce a new canonical processing lineage.

It SHALL not rewrite historical publication snapshots.

---

# 200. Adapter Versions

Every acquisition SHALL identify:

```text
adapter_name
adapter_version
```

so interpretation can be reconstructed after adapter changes.

---

# 201. Canonical Schema Versions

Every resulting canonical record SHALL identify its canonical schema version.

---

# 202. Ingestion Idempotency

Repeated retrieval of the same source artefact SHALL not create duplicate canonical facts.

---

# 203. Independent Corroboration Preservation

However:

```text
Source A says X
Source B says X
```

must remain two independent evidence paths.

Deduplication SHALL not erase corroboration.

---

# 204. Observability

Every acquisition pipeline SHALL expose telemetry for:

```text
source
dataset
adapter
job
records
latency
freshness
errors
quarantine
cost
```

---

# 205. Research Operations Dashboard

Operational staff SHOULD eventually see:

```text
sources healthy
sources stale
licences expiring
adapters broken
research missions blocked
datasets delayed
reports awaiting review
```

---

# 206. Source SLA

Critical sources MAY receive internal SLAs.

Example:

```text
FX source stale > 2 hours
→ degradation alert
```

while:

```text
annual GDP dataset
```

obviously receives a different policy.

---

# 207. Commercial Product SLA

Subscription products MAY define:

```text
update frequency
delivery time
alert latency
source coverage
```

which the Source Mesh must support.

---

# 208. Graceful Degradation

A report MAY proceed with a missing noncritical source if:

```text
the missing evidence is disclosed
confidence is adjusted
methodology permits
```

A mandatory-source failure SHALL block publication.

---

# 209. Evidence Debt

Pulse SHOULD recognise `EvidenceDebt`.

EvidenceDebt occurs when intelligence relies on:

```text
stale
weak
single-source
proxy
incomplete
```

evidence pending improvement.

---

# 210. Evidence Debt Register

A ResearchMission SHOULD expose unresolved EvidenceDebt before publication.

---

# 211. Source Discovery Backlog

Pulse SHOULD maintain a backlog of missing source capabilities.

Example:

```text
COUNTRY X:
    customs data missing

SECTOR Y:
    reliable pricing missing
```

This backlog can guide business-development investment.

---

# 212. Commercial Demand Drives Source Investment

New source integrations SHOULD be prioritised where they support:

```text
paying client demand
reusable report families
strategic verticals
high-value recurring intelligence
```

rather than merely increasing connector count.

---

# 213. Connector Count Is Not a KPI

The KPI is not:

```text
we have 500 connectors
```

The meaningful measures are:

```text
coverage
reliability
reuse
freshness
commercial product support
intelligence quality
revenue contribution
```

---

# 214. Product Coverage Matrix

Pulse SHOULD maintain:

```text
                 FX TRADE REG WEATHER COMPANY GEO NEWS INTERNAL

Market Entry      ✓    ✓    ✓    ✓       ✓      ✓   ✓      ✓

Supplier Report   ✓    ✓    ✓    ✓       ✓      ✓   ✓      ✓

Macro Brief       ✓    ✓    ✓                           

Regulatory        ✓         ✓                    ✓

Corridor           ✓   ✓    ✓    ✓              ✓   ✓
```

This identifies commercial product dependencies.

---

# 215. Foundational Source Priorities

The first Source Mesh implementation SHOULD prioritise the highest-reuse categories:

```text
FX
trade statistics
tariffs
commodity prices
macroeconomic indicators
news/regulatory publications
country/geographic reference data
```

Then expand into:

```text
weather/climate
company registry
logistics
geospatial infrastructure
government open data
specialist market prices
```

based on commercial use cases.

---

# 216. Why Trade Should Be a Flagship Domain

Trade data is particularly suitable for Pulse because it naturally connects:

```text
country
product
time
value
volume
origin
destination
tariff
price proxy
```

to commercial questions.

The WTO currently provides programmatic access to trade and tariff indicators, while its Tariff and Trade Data dataset includes detailed applied and bound tariff information and trade statistics.

---

# 217. Trade Intelligence Flywheel

```text
TRADE FLOWS
     ↓
PRODUCT-MARKET PAIRS
     ↓
GROWTH SIGNALS
     ↓
OPPORTUNITY SCREEN
     ↓
ENRICH WITH
FX + REGULATION + PRICE + COMPANY + LOGISTICS
     ↓
COMMERCIAL OPPORTUNITY
```

This can become one of Pulse's first repeatable commercial engines.

---

# 218. The Product-Market Pair

Pulse SHOULD recognise:

```text
Product × Market
```

as a central analytical dimension.

For example:

```text
HS090111
×
South Africa
```

may be analysed independently from the same product in another market.

---

# 219. Product-Market-Origin Triangle

Even more valuable:

```text
PRODUCT
   ×
DESTINATION MARKET
   ×
ORIGIN
```

This allows Pulse to identify:

```text
growing origin
declining incumbent
price differences
trade concentration
new supplier possibilities
```

---

# 220. Market Whitespace

Pulse MAY identify:

```text
high demand
+
low supplier diversity
```

as potential whitespace.

It remains a candidate, not automatic opportunity.

---

# 221. Trade Concentration

Metrics such as supplier concentration MAY enrich risk/opportunity analysis.

The exact metric SHALL be methodology-versioned.

---

# 222. Price-Demand Divergence

Interesting candidates may appear where:

```text
import volume rises
while
unit-value trends diverge
```

from comparable markets.

Such anomalies deserve research rather than automatic conclusions.

---

# 223. Cross-Border Arbitrage Intelligence

Pulse MAY detect apparent:

```text
price differentials
FX effects
tariff differences
```

but SHALL distinguish:

```text
apparent arbitrage
```

from genuinely executable arbitrage after:

```text
freight
quality
timing
regulation
tax
capacity
```

are considered.

---

# 224. Emerging Supplier Intelligence

Possible indicators:

```text
rapid export growth
new destination penetration
increased production
improving infrastructure
favourable pricing
new company activity
```

may surface emerging origins or suppliers.

---

# 225. Emerging Market Intelligence

Likewise:

```text
population/income growth
rising imports
infrastructure expansion
company formation
regulatory liberalisation
```

may indicate emerging demand.

---

# 226. "Why Now?" Requirement

Every high-value Opportunity SHOULD answer:

> Why is this opportunity relevant **now**?

A report that describes only long-established facts has lower commercial differentiation.

---

# 227. Change Detection

Pulse SHOULD therefore prioritise:

```text
what changed?
```

alongside:

```text
what is true?
```

---

# 228. Delta-First Intelligence

For recurring clients the primary output may increasingly become:

```text
since your last report,
these five things materially changed.
```

This supports subscription economics.

---

# 229. Change Significance

Not every change deserves attention.

Pulse SHALL calculate or assess:

```text
magnitude
persistence
relevance
confidence
commercial impact
```

before escalating.

---

# 230. Intelligence Event

A significant external change MAY generate:

```text
IntelligenceEvent
```

which can trigger affected ResearchMissions and IntelligenceProducts.

---

# 231. Dependency Graph

Example:

```text
Tariff changed
      ↓
Coffee Market Report
      ↓
Supplier Opportunity Report
      ↓
Landed Cost Monitor
```

All affected products can be marked for reassessment.

---

# 232. Continuous Research

This transforms research from:

```text
document creation
```

into:

```text
managed intelligence lifecycle
```

---

# 233. The Long-Term Vision

The long-term goal is a Pulse engine capable of continuously asking:

```text
What changed?

Where?

For whom?

Compared with what?

Supported by which evidence?

How unusual is it?

What could it mean commercially?

How long might it matter?

Who should know?

What decision deserves consideration?
```

---

# 234. What Pulse Must Never Become

The Source Mesh SHALL NOT become:

```text
an uncontrolled data lake

a copyright infringement mechanism

a scraping farm

a pile of API wrappers

an LLM browsing bot

a vendor-specific market-data terminal clone

a repository of uncited AI reports

a place where public and confidential data are mixed
without policy

an intelligence system that cannot reconstruct
why it reached a conclusion
```

---

# 235. Rejected Alternative — Manual Research as the Primary Model

Rejected:

```text
analyst
→ Google
→ spreadsheets
→ copy/paste
→ Word/PDF
```

Reason:

This may produce individual reports but does not accumulate reusable institutional intelligence.

---

# 236. Rejected Alternative — Direct LLM Web Research

Rejected as the production architecture.

Reason:

It is difficult to guarantee:

```text
source continuity
licensing
reproducibility
versioning
data quality
canonical identity
```

through ad-hoc model browsing alone.

LLM web research remains useful for discovery and exploratory investigation.

---

# 237. Rejected Alternative — Data Warehouse First

Rejected:

```text
collect everything
then decide what it is for
```

Reason:

This creates high acquisition and storage cost without demonstrating commercial value.

Pulse SHALL be **question-led and capability-led**.

---

# 238. Rejected Alternative — One Adapter per Commercial Product

Rejected.

Sources are shared capabilities.

A World Bank adapter should not be rebuilt independently for:

```text
Country Report
Market Report
Investment Report
```

---

# 239. Rejected Alternative — One Universal Data Model

Rejected.

The canonical Observation model provides common semantics while domain profiles preserve necessary detail.

FX, weather, trade and regulatory data SHOULD NOT be flattened until important meaning disappears.

---

# 240. Rejected Alternative — Free Data Only

Rejected.

Some commercially compelling products may require licensed premium data.

The architecture SHALL support both.

---

# 241. Rejected Alternative — Premium Data First

Also rejected.

Paying for expensive data before commercial demand exists can create unnecessary fixed costs.

---

# 242. Governing Invariants

**SRC-PULSE-001**  
Every production external data source SHALL be registered.

**SRC-PULSE-002**  
Every acquisition SHALL identify its source and adapter version.

**SRC-PULSE-003**  
Provider models SHALL terminate at the adapter boundary.

**SRC-PULSE-004**  
Raw source material SHALL remain recoverable where rights permit.

**SRC-PULSE-005**  
Canonicalisation SHALL preserve provenance.

**SRC-PULSE-006**  
Source data SHALL not be assumed commercially redistributable.

**SRC-PULSE-007**  
Commercial products SHALL pass applicable rights and licensing gates.

**SRC-PULSE-008**  
External source authority and data quality SHALL remain distinct concepts.

**SRC-PULSE-009**  
Schema drift SHALL not silently corrupt canonical observations.

**SRC-PULSE-010**  
Acquisition SHALL be idempotent.

**SRC-PULSE-011**  
Independent corroborating observations SHALL not be deduplicated into one source.

**SRC-PULSE-012**  
Every material transformation SHALL be versioned.

**SRC-PULSE-013**  
External IDs SHALL not become Baobab canonical IDs.

**SRC-PULSE-014**  
Uncertain entity matches SHALL remain candidates until resolved.

**SRC-PULSE-015**  
Provider substitution SHALL remain visible in provenance.

**SRC-PULSE-016**  
Client-private evidence SHALL remain tenant isolated.

**SRC-PULSE-017**  
A published research claim SHALL resolve to evidence.

**SRC-PULSE-018**  
No LLM-generated citation may exist without a real Evidence reference.

**SRC-PULSE-019**  
Research methodology SHALL be versioned.

**SRC-PULSE-020**  
Historical reports SHALL remain reproducible against their original evidence vintage where retention rights permit.

**SRC-PULSE-021**  
Source failure SHALL degrade affected capabilities rather than collapse unrelated Pulse domains.

**SRC-PULSE-022**  
Commercial demand, reuse and intelligence value SHALL guide source-integration priorities.

**SRC-PULSE-023**  
Connector count SHALL not be treated as a primary measure of platform value.

**SRC-PULSE-024**  
Every recurring IntelligenceProduct SHALL define freshness expectations.

**SRC-PULSE-025**  
Stale evidence SHALL not silently appear current.

**SRC-PULSE-026**  
Report confidence SHALL never conceal material evidence gaps.

**SRC-PULSE-027**  
Contradictory evidence SHALL remain visible.

**SRC-PULSE-028**  
Consequential commercial opportunities SHALL expose the evidence and methodology that generated them.

**SRC-PULSE-029**  
Pulse SHALL distinguish an OpportunityCandidate from a qualified Opportunity.

**SRC-PULSE-030**  
Pulse SHALL favour reusable evidence infrastructure over one-off manual data assembly.

---

# 243. Strategic Consequences

This decision means that `nabhold/baobab-pulse` is not merely being built as an internal software engine.

It establishes the technological foundation for a potential **Nabhold intelligence business**.

That business could ultimately operate at several economic levels:

```text
                     ┌──────────────────────────────┐
                     │      STRATEGIC ADVISORY      │
                     │ highest value / bespoke      │
                     ├──────────────────────────────┤
                     │      CUSTOM RESEARCH         │
                     ├──────────────────────────────┤
                     │    SUBSCRIPTION MONITORS     │
                     ├──────────────────────────────┤
                     │      PREMIUM REPORTS         │
                     ├──────────────────────────────┤
                     │       SHORT BRIEFS           │
                     ├──────────────────────────────┤
                     │   DERIVED DATA / APIs        │
                     │ where licensing permits      │
                     └──────────────────────────────┘

                              supported by

                     ┌──────────────────────────────┐
                     │   PULSE EVIDENCE PLATFORM    │
                     └──────────────────────────────┘
```

The higher commercial layers reuse the lower infrastructure.

---

# 244. Strategic Flywheel

The desired commercial flywheel is:

```text
CLIENT QUESTION
      ↓
NEW RESEARCH
      ↓
NEW SOURCES / MAPPINGS
      ↓
BETTER EVIDENCE GRAPH
      ↓
BETTER METHODS
      ↓
BETTER INTELLIGENCE PRODUCTS
      ↓
MORE CLIENTS
      ↓
MORE QUESTIONS
      ↓
MORE EVIDENCE
```

With each cycle, Pulse should become incrementally more capable.

---

# 245. Compounding Asset

The real compounding asset is therefore not merely software.

It is:

```text
CODE
+
DATA RELATIONSHIPS
+
SOURCE HISTORY
+
MAPPINGS
+
METHODOLOGY
+
RESEARCH CORPUS
+
CLIENT QUESTIONS
+
ANALYST KNOWLEDGE
+
OUTCOME FEEDBACK
```

---

# 246. Vision: From Report Writer to Opportunity Observatory

The mature state of Pulse should no longer begin only when someone asks for a report.

It should continuously watch the evidence environment.

```text
                 BAOBAB PULSE

                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      TRADE        MARKETS      REGULATION
        │            │            │
        ├────────────┼────────────┤
        ▼            ▼            ▼
      CLIMATE      COMPANIES      MACRO
        │            │            │
        └────────────┼────────────┘
                     ▼
                CHANGE DETECTION
                     │
                     ▼
                 WEAK SIGNALS
                     │
                     ▼
            OPPORTUNITY CANDIDATES
                     │
                     ▼
               DEEP RESEARCH
                     │
                     ▼
                 OPPORTUNITY
                     │
                     ▼
             COMMERCIAL PRODUCT
```

In other words:

> **Today we may ask Pulse to research an opportunity. Eventually Pulse should increasingly be able to tell us where an opportunity deserves to be researched.**

That is the strategic destination.

---

# 247. The Commercial Standard

A Nabhold intelligence paper produced through Pulse should eventually be recognisable for five characteristics:

```text
1. It knows exactly where its evidence came from.

2. It understands what the evidence means
   across incompatible sources.

3. It tells the reader what changed,
   not merely what exists.

4. It distinguishes fact,
   inference,
   forecast,
   scenario and recommendation.

5. It identifies why the evidence may matter
   commercially.
```

---

# 248. Final Decision Statement

Baobab Pulse SHALL implement its external-data capability as a **governed, provider-neutral, provenance-first Intelligence Acquisition and Commercial Research Fabric**.

The Source Mesh shall transform:

```text
WORLD BANK
IMF
WTO
CENTRAL BANKS
CUSTOMS
COMMODITY SOURCES
WEATHER & CLIMATE
COMPANY REGISTRIES
GEOSPATIAL DATA
GOVERNMENT OPEN DATA
NEWS
REGULATION
PAYLOAD
MEDUSA
IDEMPIERE
CLIENT DATA
```

into:

```text
CANONICAL OBSERVATIONS
        ↓
EVIDENCE
        ↓
SIGNALS
        ↓
CLAIMS
        ↓
INSIGHTS
        ↓
OPPORTUNITIES / RISKS
        ↓
RECOMMENDATIONS
        ↓
INTELLIGENCE PRODUCTS
```

The architecture shall be deliberately designed so that a source integrated once can support many investigations, a dataset normalised once can support many products, a methodology developed once can be repeatedly applied, and every completed research engagement strengthens the intelligence infrastructure available for the next engagement.

The strategic purpose of the Source Mesh is therefore not merely:

```text
to collect information.
```

It is:

```text
to convert dispersed evidence
into institutional knowledge,
institutional knowledge
into defensible intelligence,
and defensible intelligence
into commercially valuable decisions.
```

If Baobab Pulse succeeds at this boundary, Nabhold should not have to wait for every opportunity to arrive as an obvious business idea.

The engine should progressively become capable of finding the **changes, gaps, divergences, concentrations, constraints and emerging patterns from which opportunities can be investigated before they become obvious**.

That is the ambition governed by this ADR.