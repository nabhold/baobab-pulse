# ADR-PULSE-001 — Engine Mission, Authority and System Boundary

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-001`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001 — Baobab Pulse Intelligence Engine Parent Architecture Specification`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001 — Baobab Pulse Canonical Intelligence Model`  
**Decision Type:** Foundational Architecture Decision

## Context

Baobab Pulse is being introduced alongside three mature headless engines:

- Payload CMS as the content system of record;
- MedusaJS as the commerce system of record;
- iDempiere as the ERP system of record.

The Baobab Platform therefore requires a clear architectural definition of what Pulse is authorised to own, what it may derive, what it may influence, and what it must never directly control.

Without a strict boundary, an intelligence engine tends to expand into several problematic roles at once:

```text id="r5a4gh"
analytics service
+
reporting system
+
AI assistant
+
integration service
+
automation layer
+
shadow ERP
+
shadow data warehouse
```

This would destroy the engine boundaries already established across the Baobab platform.

The foundational decision must therefore separate:

```text id="5di3xk"
operational truth
```

from:

```text id="2w3gz4"
analytical interpretation
```

and from:

```text id="9ec2ds"
decision authority
```

---

# Decision

Baobab Pulse SHALL be defined as the **Baobab Platform System of Intelligence**.

Its authoritative responsibility is limited to:

```text id="a91cve"
observations
evidence
signals
analyses
insights
opportunities
risks
forecasts
recommendations
decision-support records
outcomes
feedback
model metadata
intelligence products
```

Pulse SHALL NOT become authoritative for business transactions owned by another engine.

---

# Authoritative Domain Boundary

The authoritative domain ownership is:

| Domain | Authoritative Engine |
|---|---|
| Content | Payload CMS |
| Commerce | MedusaJS |
| ERP / Accounting / Operations | iDempiere |
| Platform identity and engine context | Baobab Control Plane |
| Cross-engine canonical contracts | `nabhold/shared` |
| Intelligence and decision support | Baobab Pulse |

The guiding rule is:

> **Pulse may observe, interpret, forecast and recommend. It does not silently become the transactional owner of the operational domains it analyses.**

---

# System-of-Record versus System-of-Intelligence

The distinction SHALL be explicit.

```text id="k64hcs"
SYSTEM OF RECORD
    ↓
records what happened operationally

SYSTEM OF INTELLIGENCE
    ↓
interprets what those records may mean
```

Examples:

```text id="v84jj1"
Medusa:
    order.total = 25,000

Pulse:
    sales volume is accelerating
```

```text id="9zkdqc"
iDempiere:
    supplier invoice posted

Pulse:
    supplier cost concentration is increasing
```

```text id="qgv2uz"
Payload:
    campaign content published

Pulse:
    campaign activity correlates with increased demand
```

---

# Pulse Authority

Pulse SHALL be authoritative for its own canonical intelligence entities.

These include:

```text id="f5lqt6"
Observation
Evidence
EvidenceSet
Signal
Trend
Anomaly
Analysis
Insight
Opportunity
Risk
Forecast
Recommendation
DecisionRecord
Outcome
Feedback
Model
ModelVersion
ModelRun
IntelligenceJob
IntelligenceProduct
```

The phrase **DecisionRecord** is significant.

Pulse may record and preserve a decision, but the authority to make that decision belongs to an authorised human, policy or external workflow.

---

# Decision Authority

Pulse SHALL distinguish between:

```text id="ziyzg4"
intelligence authority
```

and:

```text id="616mhm"
business authority
```

Pulse can legitimately state:

```text id="yms7uo"
Evidence indicates a high probability of
margin compression over the next 30 days.
```

Pulse cannot independently decide:

```text id="vq356o"
Increase all retail prices by 12%.
```

unless a separately authorised automation policy explicitly grants that capability.

---

# Default Decision Model

The default decision model SHALL be:

```text id="j5z8vg"
Evidence
   ↓
Pulse Analysis
   ↓
Recommendation
   ↓
Human / Policy Authority
   ↓
Decision
   ↓
Owning Engine
   ↓
Operational Action
```

Not:

```text id="3hjmc9"
Pulse
   ↓
direct transactional mutation
```

---

# Read Authority

Pulse MAY read authorised information from:

```text id="gwhpdd"
Payload CMS
MedusaJS
iDempiere
Baobab Control Plane
external sources
```

through approved:

```text id="ekj1ex"
APIs
events
webhooks
exports
source adapters
```

Pulse SHALL NOT rely on direct cross-engine database access.

---

# Write Authority

Pulse MAY directly write only to:

```text id="qwi0ro"
its own persistence layer
its own evidence store
its own analytical indexes
its own caches
its own event outbox
its own model registry
```

Operational modifications to another engine MUST occur through that engine's supported contract.

---

# Mutation Boundary

For example:

```text id="2f96ck"
Pulse Opportunity:
    reorder coffee inventory
```

may result in:

```text id="pj1pvs"
Recommendation
    ↓
Approval
    ↓
canonical command / API request
    ↓
iDempiere procurement workflow
```

Pulse SHALL NOT execute:

```text id="r9l27b"
UPDATE idempiere.purchase_order ...
```

under any circumstance.

---

# External Data Authority

Pulse does not become the authoritative origin of externally sourced data merely because it stores a canonicalised representation.

For example:

```text id="b8ksoz"
World Bank GDP observation
```

remains attributable to the World Bank source.

Pulse owns:

```text id="l4k3m9"
its canonical observation
provenance
quality assessment
interpretation
```

but not the original economic fact as a source authority.

---

# Derived Authority

Pulse SHALL be authoritative for derived intelligence produced by Pulse.

Example:

```text id="20g461"
External observations
+
Medusa demand
+
iDempiere procurement cost
      ↓
Pulse Insight
```

The Insight is a Pulse-owned intelligence object.

Its underlying observations retain their original authority.

---

# Boundary with Payload CMS

Payload CMS owns:

```text id="5r140p"
content documents
publication state
editorial workflow
content taxonomy
digital composition
```

Pulse may:

```text id="4r36vh"
analyse content
classify content
extract entities
measure publication trends
generate candidate narratives
suggest content opportunities
```

Pulse SHALL NOT:

```text id="plwkyw"
become the primary CMS
silently publish content
overwrite editorial decisions
```

unless the publication workflow explicitly authorises automation.

---

# Boundary with MedusaJS

MedusaJS owns:

```text id="vahad1"
products
variants
prices
customers
carts
orders
sales channels
commerce regions
promotions
returns
```

Pulse may derive:

```text id="fnkwra"
demand signals
pricing opportunities
customer trends
market insights
inventory-risk indicators
```

Pulse SHALL NOT duplicate Medusa's commerce domain.

---

# Boundary with iDempiere

iDempiere owns:

```text id="19jbfu"
general ledger
accounting
procurement
accounts payable
accounts receivable
inventory operations
assets
business partners
financial posting
ERP workflow
```

Pulse may derive:

```text id="q8mw4a"
working-capital insight
supplier concentration risk
margin trends
procurement opportunities
cash-flow forecasts
inventory signals
```

Pulse SHALL NOT:

```text id="cr3ec5"
post accounting transactions
own journals
replace ERP controls
maintain a shadow general ledger
```

---

# Boundary with Baobab Control Plane

The Control Plane owns:

```text id="h40wuj"
CanonicalEntity
ExternalReference
Mapping
MappingScope
Market
DigitalEstate
Engine
EngineInstance
Capability
CapabilityBinding
Context
IsolationProfile
```

Pulse SHALL reference these identities.

It SHALL NOT independently redefine platform control metadata.

---

# Boundary with `nabhold/shared`

`nabhold/shared` owns organisation-wide canonical contracts.

Pulse-specific implementation MUST conform to shared definitions for:

```text id="04b1yy"
tenant identity
context identity
canonical references
event envelopes
schema versions
error contracts
classification
correlation
causation
```

Pulse MAY propose new canonical contracts, but once promoted to organisational standard they belong in `nabhold/shared`.

---

# Boundary with External Intelligence Sources

Pulse MAY integrate with sources for:

```text id="zmyie0"
FX
commodity prices
weather
trade statistics
customs
macroeconomics
market prices
company registries
geospatial data
government open data
news
regulatory data
```

Source adapters form an anti-corruption layer.

The provider's domain model SHALL stop at the adapter boundary.

---

# Anti-Corruption Layer

The model SHALL be:

```text id="7dephh"
External Provider
      ↓
Provider Adapter
      ↓
Raw Source Representation
      ↓
Canonicalisation
      ↓
Pulse Canonical Model
```

Never:

```text id="xry3ou"
Provider API schema
      ↓
Pulse domain model
```

directly.

---

# Boundary with Reporting

Pulse MAY generate intelligence reports.

However, static reporting is not its principal architecture.

Reporting should be viewed as:

```text id="ktwnlw"
projection of intelligence
```

rather than:

```text id="2o66mk"
core intelligence storage
```

---

# Boundary with Business Intelligence Tools

External BI tools MAY consume Pulse projections.

Pulse SHALL not attempt to replace every dashboarding or visualisation product.

It should provide:

```text id="i7i5t8"
stable APIs
query models
export contracts
analytical projections
```

that downstream presentation tools may use.

---

# Boundary with Data Warehousing

Pulse MAY eventually require analytical storage.

However:

> Pulse is not defined as a data warehouse.

Storage technologies are implementation choices.

Its architectural identity is derived from its intelligence model and authority, not from whether it uses:

```text id="3gh5up"
PostgreSQL
object storage
lakehouse
warehouse
```

---

# Boundary with Machine Learning

ML capabilities are subordinate to the intelligence domain.

A machine-learning model is:

```text id="fvq16n"
one analytical method
```

not:

```text id="n1n09r"
the engine itself
```

---

# Boundary with LLMs

LLMs MAY support:

```text id="g2p8ay"
classification
summarisation
entity extraction
semantic analysis
hypothesis generation
narrative synthesis
research assistance
```

but Pulse SHALL remain functional for deterministic intelligence workloads without an LLM.

---

# Boundary with Agents

Agents SHALL be considered application-layer orchestrators.

They may invoke approved Pulse capabilities.

They SHALL NOT define core domain semantics.

The canonical model must remain valid even if every agent implementation is replaced.

---

# Intelligence Authority Hierarchy

Pulse intelligence SHALL recognise increasingly consequential authority levels:

```text id="r6jc8z"
LEVEL 0
Observation

LEVEL 1
Signal

LEVEL 2
Insight

LEVEL 3
Opportunity / Risk / Forecast

LEVEL 4
Recommendation

LEVEL 5
Decision

LEVEL 6
Operational Action
```

Pulse owns levels 0–4.

Level 5 belongs to the authorised decision authority, though Pulse may record it.

Level 6 belongs to the operational engine or approved external process.

---

# Automation Authority Levels

Automation policy SHALL distinguish:

```text id="0m1cvd"
OBSERVE
ANALYSE
RECOMMEND
PROPOSE
APPROVE_BY_POLICY
EXECUTE
```

No capability may jump between authority levels without an explicit policy.

---

# Low-Risk Automation

Some operational responses MAY eventually be automatically executed.

Examples might include:

```text id="78z49f"
refreshing a report
triggering a new analysis
creating an internal notification
requesting another data acquisition
```

These do not necessarily require business approval.

---

# High-Impact Automation

Actions affecting:

```text id="2dbb5f"
money
contracts
customers
employees
suppliers
accounting
legal obligations
pricing
inventory commitments
```

SHOULD require strong explicit policy and ordinarily human approval.

---

# Human-in-the-Loop Principle

Pulse SHALL support meaningful human oversight.

A human reviewer should be able to inspect:

```text id="35ae9x"
recommendation
supporting evidence
contradicting evidence
sources
confidence
method
assumptions
potential impact
```

before acting.

---

# Evidence Boundary

Pulse SHALL not publish consequential intelligence without traceable evidence except where explicitly classified as:

```text id="um1er4"
hypothesis
scenario
human opinion
experimental
```

Such outputs must remain distinguishable from evidence-backed intelligence.

---

# Hypothesis Boundary

A hypothesis is not an Insight until sufficient evidence and analysis support promotion.

```text id="rtvsf8"
Hypothesis
   ↓
investigation
   ↓
Evidence
   ↓
Analysis
   ↓
Insight
```

---

# Scenario Boundary

Scenario analysis represents:

```text id="vabuzn"
what might happen if...
```

not:

```text id="vqfk92"
what Pulse predicts will happen
```

Scenarios and forecasts SHALL remain semantically distinct.

---

# Prediction Boundary

A Forecast must identify:

```text id="n0ojmb"
forecast origin
target
horizon
model/method
uncertainty
```

A narrative expectation without these semantics is not a canonical Forecast.

---

# Risk Boundary

A Risk SHALL not automatically be created merely because a negative Signal exists.

The progression should be:

```text id="lhnexy"
Signal
   ↓
Analysis
   ↓
Insight
   ↓
Risk Assessment
```

where appropriate.

---

# Opportunity Boundary

Likewise:

```text id="835vvh"
market movement
```

does not automatically imply:

```text id="4bt04s"
business opportunity
```

without tenant, market, feasibility and strategic context.

---

# Canonical Tenant Boundary

Pulse SHALL remain fully tenant-aware.

Tenant context SHALL govern:

```text id="1fuwjy"
visibility
evidence access
analysis access
derived intelligence
recommendations
decision history
```

---

# Tenant is Not Legal Entity

Pulse SHALL preserve the platform rule:

> A legal entity is commonly a default tenant boundary, but tenant and legal entity are not synonyms.

Therefore intelligence may be scoped to:

```text id="7lglpk"
tenant
legal entity
business unit
market
digital estate
```

independently.

---

# Public Intelligence Boundary

Publicly sourced evidence MAY belong to platform-level shared intelligence.

Example:

```text id="089jfu"
SARB reference rate
World Bank GDP
government tariff schedule
```

may be globally reusable according to licensing.

---

# Tenant Intelligence Boundary

Derived intelligence involving private tenant evidence SHALL remain tenant-scoped unless explicit policy permits broader use.

---

# Cross-Tenant Aggregation

Cross-tenant aggregation MAY occur only where:

```text id="tzxrtx"
governance permits
+
privacy is preserved
+
source restrictions permit
+
re-identification risk is controlled
```

---

# Confidentiality Propagation

Classification SHALL normally propagate according to the most restrictive input.

```text id="2k82fc"
PUBLIC
+
TENANT CONFIDENTIAL
=
TENANT CONFIDENTIAL
```

---

# Geographic Boundary

Pulse intelligence may be scoped independently by:

```text id="uxrsyd"
country
region
economic bloc
market
trade corridor
physical location
```

Geography SHALL not be inferred solely from tenant identity.

---

# Market Boundary

A single tenant may participate in multiple markets.

Therefore:

```text id="gzhyn2"
tenant = Thamani
```

cannot imply:

```text id="0zsaqb"
market = South Africa
```

forever.

This allows future expansion.

---

# Regional Expansion

Pulse SHALL support tenants operating independently in:

```text id="xjns4l"
South Africa
Uganda
Kenya
Tanzania
other African markets
European markets
other jurisdictions
```

without redesigning the intelligence model.

---

# Currency Boundary

Currency SHALL remain explicit.

Pulse SHALL not assume the tenant's base currency for external observations.

---

# Temporal Boundary

Pulse intelligence SHALL distinguish:

```text id="juvpeo"
past fact
current state
future forecast
proposed future scenario
```

These must never collapse into one generic time field.

---

# Historical Truth Boundary

When a source revises historical data, Pulse SHALL preserve:

```text id="q4v3pe"
what was originally published
```

and:

```text id="uhf4yd"
what is currently considered correct
```

where available.

---

# Provenance Boundary

Every material transformation SHALL create or preserve lineage.

No analytical convenience may justify destroying provenance.

---

# Source Credibility Boundary

Pulse SHALL not treat source authority as absolute truth.

Official sources may still contain:

```text id="xuu6o6"
revision
methodological limitations
publication delay
missing values
inconsistent reporting
```

---

# News Boundary

News may provide early signals.

News SHALL not be treated identically to official statistical observations.

Its evidence role, freshness and corroboration requirements differ.

---

# Regulatory Boundary

Pulse SHALL distinguish regulatory states such as:

```text id="1z5xhe"
PROPOSED
PUBLISHED
ADOPTED
EFFECTIVE
SUSPENDED
REPEALED
```

A proposed law cannot be treated as an effective obligation.

---

# Company Registry Boundary

Pulse MAY maintain canonical references to external organisations.

The Control Plane remains authoritative for Baobab canonical entities.

Pulse SHALL not create contradictory organisational identity systems.

---

# Geospatial Boundary

Spatial analysis belongs within Pulse intelligence capabilities.

Operational asset ownership remains with the appropriate system of record.

---

# Search Boundary

Search indexes are derived representations.

They are disposable and reconstructable.

They SHALL NOT become canonical stores.

---

# Vector Search Boundary

Embeddings and vector stores are indexes.

They SHALL not own:

```text id="q8c1sk"
source truth
documents
evidence
insights
```

---

# Cache Boundary

Caches are non-authoritative.

All critical intelligence must remain reconstructable without cache state.

---

# Event Boundary

Events represent changes or occurrences.

They are not themselves necessarily the complete system state.

Pulse SHALL use events for:

```text id="ar5k6u"
notification
integration
correlation
pipeline activation
```

while retaining authoritative state in its own domain store.

---

# Event Consumption

Pulse SHALL assume duplicate delivery is possible.

Therefore consumers MUST be idempotent.

---

# Event Publication

Pulse SHALL publish canonical intelligence events only after authoritative Pulse state has been persisted.

---

# Transaction Boundary

A transaction inside Pulse SHALL not span databases owned by other engines.

Distributed business consistency SHALL be achieved through:

```text id="mgn5no"
events
workflows
compensation
idempotency
```

rather than cross-engine database transactions.

---

# Failure Boundary

Failure of an external intelligence provider SHALL not cause failure of unrelated Pulse domains.

For example:

```text id="s5r195"
weather API unavailable
```

must not prevent:

```text id="cftslk"
FX ingestion
trade-statistics analysis
ERP signal processing
```

---

# Adapter Failure Isolation

Each external source adapter SHALL have its own:

```text id="wq2650"
retry policy
rate-limit handling
failure metrics
circuit state
credentials
```

---

# Intelligence Freshness Boundary

Pulse SHALL communicate degraded freshness.

If the latest source data cannot be retrieved, it must not quietly present old data as current.

---

# Security Boundary

Externally acquired data is untrusted.

Pulse SHALL validate and sanitise:

```text id="2b1syp"
documents
API payloads
HTML
CSV
JSON
XML
news text
uploaded files
```

before downstream processing.

---

# AI Trust Boundary

Untrusted source content SHALL not be allowed to alter:

```text id="6pavks"
system instructions
authorisation
tenant scope
tool access
security policy
```

through prompt injection or similar mechanisms.

---

# Model Boundary

Models SHALL operate through defined interfaces.

A model must not directly query arbitrary operational databases.

---

# Model Replacement

The architecture SHALL allow:

```text id="rh3arg"
Model A
```

to be replaced with:

```text id="0fr27z"
Model B
```

without changing canonical intelligence semantics.

---

# Vendor Boundary

Similarly:

```text id="lnq01t"
OpenAI
Anthropic
local model
future provider
```

must remain infrastructure choices rather than canonical domain concepts.

---

# Infrastructure Boundary

Pulse SHALL not depend architecturally on:

```text id="kab17p"
Kafka
Kubernetes
OpenSearch
vector databases
distributed compute
```

for its identity.

Such technologies may be introduced later.

---

# Runtime Boundary

The initial logical runtime may consist of:

```text id="re2kw7"
Pulse API
Pulse workers
Pulse scheduler
PostgreSQL
object storage
optional Redis
```

These are deployment components, not separate business domains.

---

# Microservice Boundary

Internal logical modules SHALL NOT automatically become network services.

Pulse should first be a well-structured modular engine.

Deployment decomposition shall follow demonstrated scaling or isolation needs.

---

# API Boundary

Pulse APIs SHALL expose intelligence resources.

They SHALL not attempt to replicate entire Payload, Medusa or iDempiere APIs.

---

# UI Boundary

Pulse is headless.

Any future:

```text id="jsc1nb"
Pulse Console
dashboard
executive interface
mobile experience
```

shall consume Pulse contracts and remain a separate presentation concern.

---

# Intelligence Product Boundary

An IntelligenceProduct composes Pulse capabilities.

It does not own source records or rewrite canonical intelligence.

For example:

```text id="jowstj"
Executive Brief
```

may aggregate:

```text id="bt3euu"
Insights
Opportunities
Risks
Forecasts
Recommendations
```

---

# Reporting Boundary

Reports are projections and delivery artefacts.

They SHALL be reproducible from canonical intelligence where possible.

---

# Audit Boundary

Pulse SHALL preserve sufficient history to reconstruct why a decision-support recommendation existed at a particular point in time.

---

# Deletion Boundary

Hard deletion of material provenance or decision-support history SHALL be exceptional.

Where removal is required by policy or law, the deletion process itself SHOULD be auditable.

---

# Observability Boundary

Telemetry SHALL observe system behaviour.

Telemetry SHALL NOT become an alternative business-audit store.

---

# Audit versus Logging

```text id="my0r6r"
LOG
    operational diagnostic

AUDIT
    controlled record of significant action

PROVENANCE
    derivation history of intelligence
```

These are distinct concerns.

---

# Model Monitoring Boundary

Model monitoring MAY contribute to intelligence quality but SHALL remain separate from business-result measurement.

---

# Outcome Boundary

Pulse owns the canonical intelligence Outcome record.

The actual operational fact supporting the Outcome may belong to:

```text id="paswf8"
Medusa
iDempiere
Payload
external source
human process
```

---

# Feedback Boundary

Feedback informs:

```text id="p5owkn"
model performance
signal quality
recommendation usefulness
confidence calibration
```

but SHALL not retroactively alter historical recommendations.

---

# Historical Integrity

If a recommendation was wrong, Pulse records:

```text id="8f3ks4"
recommendation
+
decision
+
outcome
+
feedback
```

It does not erase the recommendation.

---

# Governing Invariants

The following invariants are mandatory.

**INV-PULSE-001**

Pulse SHALL never be authoritative for accounting entries.

**INV-PULSE-002**

Pulse SHALL never be authoritative for commerce orders.

**INV-PULSE-003**

Pulse SHALL never be authoritative for CMS publication state.

**INV-PULSE-004**

Pulse SHALL never redefine Control Plane canonical identities.

**INV-PULSE-005**

Pulse SHALL not directly couple to another engine's database.

**INV-PULSE-006**

Pulse SHALL preserve evidence provenance.

**INV-PULSE-007**

Pulse SHALL distinguish observation from interpretation.

**INV-PULSE-008**

Pulse SHALL distinguish recommendation from decision.

**INV-PULSE-009**

Pulse SHALL distinguish decision from operational action.

**INV-PULSE-010**

Pulse SHALL not silently broaden tenant scope.

**INV-PULSE-011**

Pulse SHALL not downgrade data classification without authorised policy.

**INV-PULSE-012**

Pulse SHALL not treat LLM output as independent evidence.

**INV-PULSE-013**

Pulse SHALL preserve historical analytical state.

**INV-PULSE-014**

Pulse SHALL retain source-specific identity outside canonical identity.

**INV-PULSE-015**

Pulse SHALL remain independently deployable.

---

# Consequences

## Positive

This boundary:

- prevents Pulse from becoming a shadow ERP;
- protects Medusa and Payload ownership;
- preserves replaceability of engines;
- prevents database coupling;
- keeps AI subordinate to evidence;
- supports human oversight;
- enables clean tenant isolation;
- preserves auditability;
- makes external source replacement feasible;
- allows future automation without granting blanket authority.

---

# Trade-Offs

This architecture introduces intentional complexity.

A recommendation may require several steps:

```text id="y2uqdv"
Pulse
→ event
→ approval
→ engine API
→ operational workflow
```

rather than one database mutation.

This is deliberate.

The additional indirection provides:

```text id="np704h"
audit
security
replaceability
domain ownership
failure isolation
```

---

# Rejected Alternative — Pulse as Central Operational Brain

Rejected:

```text id="4s2dhx"
Pulse
  ↓
directly controls all engines
```

Reason:

This creates excessive coupling and would turn Pulse into a platform monolith.

---

# Rejected Alternative — Pulse as Reporting Database

Rejected:

```text id="kpvqxv"
copy all engine data
→ warehouse
→ dashboards
```

as the definition of Pulse.

Reason:

Reporting alone does not provide the semantic intelligence model required for evidence, signals, recommendations and feedback.

---

# Rejected Alternative — Pulse as LLM Agent Platform

Rejected:

```text id="25lrwf"
LLM
+
tools
+
agents
=
Pulse
```

Reason:

Models and agents change rapidly.

The engine requires a durable evidence and intelligence architecture independent of model fashion.

---

# Rejected Alternative — Shared Operational Database

Rejected:

```text id="1zibsg"
Medusa
iDempiere
Payload
Pulse
      ↓
same logical database model
```

Reason:

This destroys system ownership and engine independence.

---

# Accepted Mental Model

The accepted model is:

```text id="oxdnib"
                REAL WORLD
                    │
                    ▼
             EXTERNAL SOURCES
                    │
                    │
                    ▼
PAYLOAD ─────┐
MEDUSA ──────┼────→ EVIDENCE
IDEMPIERE ───┤          │
CONTROL PLANE┘          ▼
                       PULSE
                         │
                         ▼
                    UNDERSTANDING
                         │
                         ▼
                    RECOMMENDATION
                         │
                         ▼
                 AUTHORISED DECISION
                         │
                         ▼
                   OWNING ENGINE
                         │
                         ▼
                      OUTCOME
                         │
                         ▼
                      FEEDBACK
```

---

# Final Decision Statement

Baobab Pulse SHALL be implemented as a **bounded, headless System of Intelligence**.

It is authoritative for:

```text id="78l6af"
what Pulse observed
what evidence Pulse retained
what signals Pulse detected
what analysis Pulse performed
what insight Pulse derived
what opportunity or risk Pulse identified
what Pulse forecast
what Pulse recommended
what decision was recorded
what outcome was observed
what feedback was learned
```

It is not automatically authoritative for:

```text id="w5bmn2"
commerce
accounting
content
platform control
business approval
operational execution
```

This boundary is foundational and SHALL govern every subsequent Pulse architecture decision.