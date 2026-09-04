# ADR-PULSE-008 — Canonical Entity Resolution, Identity Matching and Cross-Source Reconciliation

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-008`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:** `ADR-PULSE-001` through `ADR-PULSE-007`  
**Decision Type:** Entity Resolution, Identity Matching and Cross-Source Reconciliation Architecture Decision

---

# 1. Context

Baobab Pulse will consume evidence from heterogeneous sources including:

```text
company registries
customs records
trade statistics
procurement datasets
government open data
news
regulatory publications
geospatial datasets
market data
Payload CMS
MedusaJS
iDempiere
Baobab Control Plane
manual research
commercial data providers
```

The same real-world entity may appear differently in each.

For example:

```text
NABHOLD GROUP AFRICA (PTY) LTD
Nabhold Group Africa
NABHOLD
Nabhold (Pty) Ltd
Nabhold Group
registration-number-X
tax-number-Y
supplier-reference-Z
domain-name
```

Some may refer to the same entity.

Some may not.

A name similarity algorithm cannot safely decide.

This problem becomes considerably harder with:

```text
subsidiaries
trading names
brands
branches
business units
joint ventures
former names
corporate restructurings
mergers
acquisitions
directors
beneficial owners
addresses
farms
warehouses
ports
products
commodities
government agencies
geographic places
```

and multilingual or transliterated names.

Pulse requires entity resolution to correlate evidence.

But canonical identity authority already belongs to the Baobab platform model represented through:

```text
CanonicalEntity
ExternalReference
Mapping
MappingScope
Context
Market
DigitalEstate
Engine
EngineInstance
```

and governed by `nabhold/baobab-cp` and organisation-wide contracts in `nabhold/shared`.

Pulse SHALL therefore perform sophisticated entity resolution without becoming a second Control Plane.

---

# 2. Decision

Baobab Pulse SHALL implement a **multi-stage, evidence-backed entity resolution architecture** that separates:

```text
SOURCE IDENTITY
        ↓
NORMALISED IDENTITY
        ↓
CANDIDATE MATCHING
        ↓
MATCH ASSESSMENT
        ↓
RESOLUTION
        ↓
CANONICAL MAPPING
```

Pulse SHALL be permitted to:

```text
discover candidates
calculate similarity
collect identity evidence
score candidates
reject candidates
flag ambiguity
recommend mappings
request human review
```

but SHALL NOT silently create authoritative platform mappings from probabilistic matches.

Authoritative cross-platform mappings SHALL remain governed through the Baobab Control Plane and canonical contracts.

---

# 3. Foundational Principle

> **Similarity is not identity.**

---

# 4. Second Principle

> **An entity resolution conclusion is itself an evidence-backed assertion.**

---

# 5. Third Principle

> **Unknown identity is preferable to false identity.**

False entity merging can corrupt:

```text
market analysis
customer intelligence
supplier risk
company research
trade analysis
ownership analysis
opportunity discovery
sanctions screening
regulatory intelligence
financial analysis
```

across the entire intelligence graph.

---

# 6. Canonical Identity Authority

The following remain platform concepts:

```text
CanonicalEntity
ExternalReference
Mapping
MappingScope
```

Pulse SHALL consume these concepts.

Pulse SHALL NOT redefine them locally as competing canonical authorities.

---

# 7. Identity Layers

Pulse SHALL distinguish at least five identity layers:

```text
1. Source Identity
2. Observed Identity
3. Candidate Identity
4. Resolved Identity
5. Canonical Identity
```

---

# 8. Source Identity

A Source Identity is the identifier or representation supplied by the originating system.

Examples:

```text
company registration number
customs trader identifier
supplier number
Medusa customer ID
iDempiere business-partner ID
Payload author/reference ID
government dataset identifier
LEI
domain name
news-mentioned name
```

---

# 9. Source Identity Preservation

Source identities SHALL be preserved exactly enough to reconstruct the original source assertion.

---

# 10. ExternalReference

Stable provider identifiers SHOULD be represented through the platform `ExternalReference` contract where appropriate.

---

# 11. Observed Identity

An `ObservedIdentity` represents identity-bearing evidence extracted from a source.

Conceptually:

```text
ObservedIdentity
 ├── observed_identity_id
 ├── entity_type
 ├── source_id
 ├── raw_name
 ├── normalised_name
 ├── external_identifiers
 ├── addresses
 ├── domains
 ├── phones
 ├── emails
 ├── jurisdictions
 ├── locations
 ├── associated_people
 ├── attributes
 ├── temporal_context
 ├── provenance
 ├── classification
 └── tenant_context
```

It is evidence.

It is not automatically a CanonicalEntity.

---

# 12. Candidate Identity

A `ResolutionCandidate` represents the proposition:

```text
ObservedIdentity A
MAY REFER TO
CanonicalEntity B
```

or:

```text
ObservedIdentity A
MAY REFER TO
ObservedIdentity B
```

---

# 13. Candidate Status

Candidate states SHOULD include:

```text
DISCOVERED
ASSESSING
LIKELY
AMBIGUOUS
UNLIKELY
REJECTED
CONFIRMED
SUPERSEDED
```

---

# 14. Resolved Identity

A `ResolvedIdentity` represents a resolution conclusion within Pulse's analytical process.

It SHALL indicate its authority.

Possible authority:

```text
SOURCE_DECLARED
DETERMINISTIC
CANONICAL_MAPPING
HUMAN_CONFIRMED
PROBABILISTIC
TEMPORARY
```

---

# 15. Canonical Identity

A `CanonicalEntity` is the Baobab platform identity used across engines.

Pulse SHALL reference its canonical ID rather than create a competing identity.

---

# 16. Entity Types

Resolution SHALL be type-aware.

Initial classes may include:

```text
ORGANISATION
LEGAL_ENTITY
PERSON
GOVERNMENT_BODY
FACILITY
LOCATION
GEOGRAPHY
PRODUCT
COMMODITY
BRAND
VESSEL
PORT
AIRPORT
MARKET
REGULATORY_INSTRUMENT
```

The canonical taxonomy SHALL be governed through shared contracts.

---

# 17. Legal Entity versus Organisation

Pulse SHALL preserve the distinction between:

```text
organisation
```

and:

```text
legal entity.
```

A group, division, brand or business unit SHALL not automatically be resolved as the legal entity that owns it.

---

# 18. Tenant Is Not Entity Identity

Tenant identity SHALL remain distinct from legal-entity identity.

A tenant may correspond to a legal entity in many deployments, but this SHALL not become an entity-resolution assumption.

---

# 19. Brand Is Not Company

Example:

```text
Brand X
```

may be owned by:

```text
Company Y.
```

The relationship:

```text
Brand X
OWNED_BY
Company Y
```

is not equivalent to:

```text
Brand X = Company Y.
```

---

# 20. Branch Is Not Parent

Branches SHALL remain separately identifiable where the source/domain requires them.

---

# 21. Facility Is Not Company

A:

```text
warehouse
factory
farm
office
store
```

may belong to an organisation without being the organisation.

---

# 22. Product Is Not Producer

Similarly:

```text
product
brand
producer
distributor
retailer
```

SHALL remain separate entities.

---

# 23. Entity Resolution Pipeline

The canonical pipeline SHALL be:

```text
RAW IDENTITY
     ↓
EXTRACTION
     ↓
NORMALISATION
     ↓
BLOCKING
     ↓
CANDIDATE GENERATION
     ↓
FEATURE EXTRACTION
     ↓
MATCH ASSESSMENT
     ↓
CONTRADICTION CHECK
     ↓
RESOLUTION POLICY
     ↓
CONFIRM / REJECT / REVIEW
     ↓
CANONICAL MAPPING
```

---

# 24. Extraction

Identity-bearing information MAY be extracted from:

```text
structured fields
semi-structured records
documents
web pages
news articles
PDFs
tables
API responses
events
manual research
```

Extraction SHALL retain provenance.

---

# 25. AI Extraction

LLMs or ML models MAY assist with entity extraction.

Their outputs SHALL be treated as candidate observations.

They SHALL not become canonical identity merely because a model generated them.

---

# 26. Name Normalisation

Pulse MAY normalise names for comparison.

Possible transformations include:

```text
case normalisation
Unicode normalisation
whitespace normalisation
punctuation handling
legal-suffix normalisation
abbreviation expansion
diacritic handling
transliteration
```

---

# 27. Raw Name Preservation

The original source name SHALL always remain recoverable.

---

# 28. Legal Suffixes

Examples:

```text
(Pty) Ltd
Ltd
Limited
LLC
PLC
Inc.
GmbH
S.A.
SARL
BV
AG
```

MAY be normalised for matching.

They SHALL not necessarily be discarded from legal identity.

---

# 29. Jurisdiction-Aware Normalisation

Legal suffix interpretation SHALL be jurisdiction-aware.

---

# 30. Transliteration

Pulse MAY generate transliterated comparison forms for multilingual names.

The transliteration SHALL be derived data.

The original script SHALL remain authoritative source evidence.

---

# 31. Alias

Aliases MAY include:

```text
former name
trading name
abbreviation
acronym
brand name
common name
transliteration
```

Alias type SHALL be explicit.

---

# 32. Former Name

A former legal name SHALL carry temporal validity.

Example:

```text
Company A
formerly known as
Company B
```

does not imply both names were simultaneously legally valid.

---

# 33. Candidate Generation

Pulse SHALL avoid comparing every identity with every canonical entity.

Candidate generation SHALL use blocking strategies.

---

# 34. Blocking

Possible blocking dimensions include:

```text
jurisdiction
entity type
registration identifier
name token
geography
postal code
domain
industry
address
phone prefix
```

---

# 35. Blocking Is Recall-Sensitive

Blocking SHALL minimise accidental exclusion of legitimate candidates.

---

# 36. Multiple Blocking Strategies

Pulse MAY combine multiple candidate-generation strategies.

---

# 37. Deterministic Matching

Certain evidence MAY provide deterministic resolution.

Examples may include:

```text
verified canonical mapping
verified registry identifier
engine mapping already approved by CP
```

provided the identifier's scope and authority are understood.

---

# 38. Identifier Scope

An identifier SHALL never be assumed globally unique unless its governing scheme guarantees appropriate uniqueness.

---

# 39. Composite Identity

Some identifiers require:

```text
identifier
+
scheme
+
jurisdiction
```

to be meaningful.

---

# 40. Registration Number

A company registration number SHALL be interpreted with:

```text
jurisdiction
registry
identifier scheme
```

where necessary.

---

# 41. Tax Identifier

Tax numbers MAY be sensitive.

Their ingestion, display and matching SHALL respect data-classification and lawful-use policies.

---

# 42. Domain Name

A verified corporate domain is strong evidence.

It is not universally definitive evidence of legal identity.

---

# 43. Email Domain

Email-domain matching SHALL be treated cautiously.

Shared mail providers and delegated domains can create false matches.

---

# 44. Address Matching

Addresses MAY contribute identity evidence.

They SHALL not be treated as universally unique identifiers.

---

# 45. Shared Addresses

Many entities may legitimately share:

```text
office buildings
registered-agent addresses
incubators
law firms
virtual offices
industrial parks
```

---

# 46. Phone Matching

Phone numbers MAY contribute evidence but require:

```text
normalisation
country code
temporal validity
source quality
```

---

# 47. Geospatial Matching

Coordinates MAY support facility/location resolution.

Distance thresholds SHALL be context-sensitive.

---

# 48. Name Matching

Name similarity is one feature.

It SHALL NOT be the entire resolution methodology.

---

# 49. Candidate Features

Organisation-resolution features MAY include:

```text
name similarity
registration identifier
jurisdiction
address similarity
domain match
phone match
industry compatibility
director overlap
ownership relationship
geographic proximity
source authority
temporal compatibility
```

---

# 50. Person Resolution

Person resolution is higher risk.

Features MAY include:

```text
name
date of birth
nationality
organisation affiliation
role
address
verified identifier
```

subject to privacy and lawful-processing requirements.

---

# 51. Person Resolution Restrictions

Pulse SHALL NOT unnecessarily build identity profiles of private individuals.

Person resolution SHALL require legitimate analytical purpose and policy.

---

# 52. Commodity Resolution

Commodity resolution SHALL account for:

```text
commodity family
grade
variety
HS classification
contract specification
origin
processing state
```

---

# 53. Example

```text
Arabica coffee
```

is not automatically equivalent to:

```text
Uganda Bugisu AA
```

even though the latter may belong to the former category.

This is classification, not identity.

---

# 54. Classification versus Identity

Pulse SHALL distinguish:

```text
IS_SAME_AS
```

from:

```text
IS_A
BELONGS_TO
CLASSIFIED_AS
```

---

# 55. Geography Resolution

Geography SHALL account for:

```text
country
administrative level
boundary version
historical name
code scheme
```

---

# 56. Place Name Ambiguity

Names such as:

```text
Victoria
Congo
Georgia
Springfield
```

illustrate why textual equality is insufficient.

---

# 57. Geographic Codes

Codes SHOULD include scheme/version.

Example:

```text
ISO
UN/LOCODE
administrative code
customs code
provider code
```

---

# 58. Port Resolution

Port identity SHALL distinguish:

```text
port
terminal
city
customs office
border post
```

where the domain requires it.

---

# 59. Product Resolution

Products may have:

```text
SKU
GTIN
manufacturer code
supplier code
Medusa product ID
ERP product ID
```

Resolution SHALL respect identifier scope.

---

# 60. Internal Engine Identity

Internal Baobab engines SHALL expose canonical or mapped identifiers through approved contracts.

Pulse SHALL prefer those mappings over probabilistic reconstruction.

---

# 61. Medusa Identity

Pulse SHALL not infer that:

```text
Medusa customer X
```

equals:

```text
iDempiere Business Partner Y
```

merely from matching names.

The Control Plane mapping SHALL be preferred.

---

# 62. ERP Identity

iDempiere identifiers remain ERP-local identities unless mapped canonically.

---

# 63. Payload Identity

Payload content references remain content-engine identities unless canonical mappings exist.

---

# 64. Control Plane Resolution

Where a canonical mapping already exists in `baobab-cp`, Pulse SHALL use it.

---

# 65. Mapping Precedence

Resolution SHOULD apply precedence approximately as:

```text
ACTIVE CANONICAL MAPPING
        ↓
VERIFIED AUTHORITATIVE IDENTIFIER
        ↓
HUMAN-CONFIRMED RESOLUTION
        ↓
DETERMINISTIC RULE
        ↓
PROBABILISTIC RESOLUTION
        ↓
UNRESOLVED
```

Exact policies may vary by entity class.

---

# 66. Mapping Scope

Mappings SHALL respect `MappingScope`.

A mapping valid for one:

```text
provider
market
tenant
context
engine
dataset
```

SHALL not automatically become globally valid.

---

# 67. Temporal Mapping

Mappings MAY be temporally bounded.

---

# 68. Example

A supplier identifier may refer to:

```text
Company A
```

until a corporate restructuring and later refer to:

```text
Company B.
```

Historical resolution SHALL preserve the correct period.

---

# 69. Resolution Evidence

Every material resolution conclusion SHOULD identify supporting evidence.

Conceptually:

```text
ResolutionEvidence
 ├── evidence_type
 ├── value
 ├── source
 ├── direction
 ├── weight
 ├── confidence
 └── temporal_context
```

---

# 70. Supporting Evidence

Examples:

```text
same registration number
same verified domain
same address
same directors
same official registry entry
```

---

# 71. Contradictory Evidence

Examples:

```text
different jurisdictions
different registration numbers
incompatible incorporation dates
different verified domains
simultaneously active separate legal entities
```

Contradictory evidence SHALL be preserved.

---

# 72. Contradiction Before Score

Resolution SHALL evaluate contradictions rather than blindly average positive similarities.

---

# 73. Hard Contradictions

Certain contradictions MAY prohibit automatic matching.

Example:

```text
verified registration IDs differ
```

for two simultaneously active legal entities within the same registry scheme.

---

# 74. Soft Contradictions

Other differences may merely reduce confidence.

Example:

```text
different office addresses
```

because companies move.

---

# 75. Match Score

Pulse MAY calculate:

```text
match_score
```

but SHALL NOT treat a score as universal truth.

---

# 76. Entity-Specific Models

Matching methodologies SHOULD differ by entity type.

A company matcher is not necessarily suitable for:

```text
people
locations
products
commodities
```

---

# 77. Match Probability

Where probabilistic models are calibrated, Pulse MAY expose estimated match probability.

The model and calibration version SHALL be recorded.

---

# 78. Confidence versus Probability

Resolution confidence MAY incorporate factors beyond raw model probability, such as:

```text
source authority
contradictions
mapping history
human review
```

Therefore probability and resolution confidence SHALL remain distinct.

---

# 79. Thresholds

Resolution policy MAY define thresholds such as:

```text
AUTO_CONFIRM
HUMAN_REVIEW
AUTO_REJECT
```

---

# 80. Consequential Identity Threshold

For consequential use, automatic confirmation SHALL require stronger evidence than exploratory research.

---

# 81. Cost-Asymmetric Resolution

False positives and false negatives have different costs.

For many legal-entity contexts:

```text
false merge
```

is considerably more dangerous than:

```text
temporary unresolved identity.
```

Thresholds SHALL reflect this.

---

# 82. Resolution Policy

Conceptually:

```text
ResolutionPolicy
 ├── entity_type
 ├── context
 ├── method
 ├── auto_confirm_threshold
 ├── review_threshold
 ├── contradiction_rules
 ├── evidence_requirements
 └── version
```

---

# 83. Policy Versioning

Every automatic resolution SHALL identify the ResolutionPolicy version used.

---

# 84. Method Versioning

Every algorithmic resolution SHALL identify:

```text
method
model
version
parameters
```

where material.

---

# 85. Candidate Set Preservation

For important resolutions, Pulse SHOULD preserve the serious candidates considered.

---

# 86. Rejected Candidate Preservation

Rejected candidates MAY be useful later if new evidence arrives.

---

# 87. Negative Match

Pulse SHALL support explicit:

```text
NOT_SAME_AS
```

or equivalent resolution evidence.

---

# 88. Negative Knowledge

This prevents repeatedly reconsidering known false matches.

---

# 89. Negative Mapping Scope

A negative match SHALL also be scoped and temporal where necessary.

---

# 90. Ambiguity

Pulse SHALL treat ambiguity as a valid outcome.

Example:

```text
three companies with identical names
```

may result in:

```text
AMBIGUOUS
```

rather than forced resolution.

---

# 91. Unresolved Identity

`UNRESOLVED` SHALL be a legitimate canonical analytical state.

---

# 92. Partial Resolution

Pulse MAY resolve:

```text
organisation family
```

without resolving the exact legal entity.

This SHALL remain explicit.

---

# 93. Hierarchical Resolution

Example:

```text
Known:
belongs to Company Group X

Unknown:
which subsidiary
```

Pulse SHALL preserve this distinction.

---

# 94. Human Review

High-impact ambiguous cases SHALL support human review.

---

# 95. Resolution Review Record

Conceptually:

```text
ResolutionReview
 ├── review_id
 ├── candidate_id
 ├── reviewer
 ├── decision
 ├── rationale
 ├── evidence_considered
 ├── reviewed_at
 └── policy_version
```

---

# 96. Review Decisions

Possible decisions:

```text
CONFIRM
REJECT
DEFER
REQUEST_MORE_EVIDENCE
ESCALATE
```

---

# 97. Reviewer Authority

Not every analyst SHALL have authority to create organisation-wide canonical mappings.

---

# 98. Mapping Proposal

Pulse SHOULD therefore produce:

```text
CanonicalMappingProposal
```

for mappings requiring Control Plane authority.

---

# 99. Mapping Proposal

Conceptually:

```text
CanonicalMappingProposal
 ├── proposal_id
 ├── observed_identity
 ├── proposed_canonical_entity
 ├── mapping_scope
 ├── evidence
 ├── confidence
 ├── resolution_method
 ├── proposed_by
 ├── status
 └── created_at
```

---

# 100. Proposal Lifecycle

```text
DRAFT
  ↓
SUBMITTED
  ↓
UNDER_REVIEW
  ↓
APPROVED
or
REJECTED
or
DEFERRED
or
SUPERSEDED
```

---

# 101. Canonical Promotion

Only after authorised approval SHALL a candidate become an authoritative platform mapping where such approval is required.

---

# 102. No Shadow Canonical Registry

Pulse SHALL NOT maintain a hidden authoritative mapping database that competes with the Control Plane.

---

# 103. Temporary Analytical Resolution

Pulse MAY use temporary analytical resolutions when necessary.

They SHALL be marked:

```text
TEMPORARY
PROBABILISTIC
```

and SHALL not escape their permitted scope as canonical facts.

---

# 104. Temporary Resolution Isolation

A temporary resolution used in one ResearchMission SHALL not automatically contaminate unrelated research.

---

# 105. Resolution Context

Resolution SHALL therefore include:

```text
tenant
research mission
dataset
market
jurisdiction
time
```

where relevant.

---

# 106. Cross-Tenant Resolution

Public entity identities MAY be reused across tenants where policy permits.

Tenant-private identities SHALL remain isolated.

---

# 107. Tenant-Private Supplier

A tenant's private supplier record SHALL not automatically reveal that supplier relationship to another tenant.

---

# 108. Identity versus Relationship Privacy

The legal identity of a company may be public.

Its relationship with a tenant may be confidential.

Pulse SHALL distinguish the two.

---

# 109. Cross-Tenant Learning

Resolution algorithms MAY learn from cross-tenant patterns only under approved governance.

They SHALL not leak tenant-private evidence.

---

# 110. Evidence Classification

Resolution evidence SHALL inherit appropriate classification.

---

# 111. Derived Classification

A ResolutionCandidate using confidential evidence may itself require confidential classification.

---

# 112. Public Mapping

A canonical mapping derived exclusively from public authoritative evidence MAY qualify for broader reuse according to policy.

---

# 113. Source Authority

Resolution SHALL consider source authority.

Example hierarchy might distinguish:

```text
official registry
authoritative internal mapping
commercial provider
company website
news
directory
machine extraction
```

but no universal ranking SHALL be assumed across every entity type and jurisdiction.

---

# 114. Source Authority Is Not Absolute Truth

Official sources may be:

```text
late
incorrect
incomplete
outdated
```

Pulse SHALL preserve contradictory evidence.

---

# 115. Temporal Compatibility

Candidate resolution SHALL evaluate whether identity evidence is temporally compatible.

---

# 116. Example

```text
Company X incorporated in 2024
```

cannot normally be the same legal entity as a company officially dissolved in 2017 with no succession relationship merely because the names match.

---

# 117. Corporate Succession

Pulse SHALL distinguish:

```text
SAME_ENTITY
SUCCESSOR_OF
PREDECESSOR_OF
ACQUIRED_BY
MERGED_INTO
RENAMED_TO
```

where evidence supports such relationships.

---

# 118. Merger

A merger SHALL not be represented as historical identity equality when distinct legal entities previously existed.

---

# 119. Acquisition

Ownership change SHALL not merge acquired and acquiring entities.

---

# 120. Corporate Rename

A verified legal rename MAY preserve canonical entity identity across names.

---

# 121. Reincorporation

Reincorporation may create a new legal entity despite continuity of:

```text
brand
staff
business
website
```

Pulse SHALL not assume continuity of legal identity.

---

# 122. Group Identity

Corporate groups MAY have canonical identities separate from constituent legal entities.

---

# 123. Ownership Graph

Entity resolution SHALL integrate with, but remain distinct from, ownership relationships.

---

# 124. Beneficial Ownership

Beneficial-ownership evidence may be uncertain, restricted or jurisdiction-specific.

Pulse SHALL preserve provenance and temporal validity.

---

# 125. Entity Resolution versus Knowledge Graph

Entity resolution answers:

```text
Are these references the same entity?
```

The broader knowledge graph answers:

```text
How are these different entities related?
```

These problems SHALL remain distinct.

---

# 126. Identity Graph

Pulse MAY maintain a logical identity graph containing:

```text
ObservedIdentity
ResolutionCandidate
CanonicalEntity reference
Alias
ExternalReference
MappingProposal
```

---

# 127. Evidence Graph Integration

Resolution conclusions SHALL integrate with `ADR-PULSE-006`.

Example:

```text
News Mention
     ↓
ObservedIdentity
     ↓
ResolutionCandidate
     ↓
CanonicalEntity
```

---

# 128. Resolution Lineage

An Insight relying on entity resolution SHALL remain traceable to the exact resolution version used.

---

# 129. Mapping Revision Impact

If an identity mapping changes:

```text
Company A
→ Company B
```

Pulse SHALL use lineage to identify affected:

```text
Observations
EvidenceSets
Analyses
Insights
Risks
Opportunities
Reports
Recommendations
```

---

# 130. Resolution Is Versioned

A resolution conclusion SHALL not be silently rewritten.

---

# 131. Resolution Supersession

A corrected resolution SHALL supersede the earlier one.

---

# 132. Historical Reconstruction

Pulse SHALL be able to answer:

> Which entity did this report believe the source record referred to when the report was published?

---

# 133. Bitemporal Identity Resolution

Where material, resolution SHALL support:

```text
valid time
system/knowledge time
```

consistent with `ADR-PULSE-007`.

---

# 134. Example

Pulse may believe in March:

```text
Record A → Company X
```

and discover in June:

```text
Record A → Company Y.
```

The June correction SHALL not make the historical March analytical state unreconstructable.

---

# 135. Canonical Merge

If the Control Plane merges duplicate canonical entities, Pulse SHALL consume the authoritative merge/succession semantics.

---

# 136. Merge Impact

Canonical merges SHALL trigger downstream impact analysis.

---

# 137. Canonical Split

If one mistakenly merged canonical entity is later split, Pulse SHALL support reassessment of affected evidence.

---

# 138. Entity Resolution Debt

Ambiguous unresolved identities SHALL be measurable.

---

# 139. Resolution Queue

Pulse SHOULD maintain prioritised resolution work.

Priority MAY consider:

```text
commercial value
number of dependent observations
number of reports affected
client importance
risk severity
resolution ambiguity
```

---

# 140. Resolution Materiality

Not every ambiguous identity requires immediate human investigation.

---

# 141. Commercial Materiality

An identity appearing in:

```text
one low-value news article
```

may remain unresolved.

An identity appearing as:

```text
largest importer in a target market
```

may justify immediate research.

---

# 142. Resolution Priority Score

Pulse MAY derive:

```text
ResolutionPriority
```

from:

```text
analytical materiality
×
uncertainty
×
downstream dependency
```

---

# 143. Entity Dossier

Pulse MAY build an analytical `EntityDossier`.

This is not a canonical identity record.

---

# 144. Entity Dossier

Conceptually:

```text
EntityDossier
 ├── canonical_entity_ref
 ├── known aliases
 ├── external references
 ├── public registry evidence
 ├── locations
 ├── ownership evidence
 ├── officers
 ├── sectors
 ├── trade evidence
 ├── news evidence
 ├── risks
 ├── opportunities
 └── provenance
```

---

# 145. Dossier Is Intelligence

The dossier is a Pulse intelligence projection assembled around canonical identity.

It SHALL not become the Control Plane entity registry.

---

# 146. Company Intelligence

This architecture enables Pulse to aggregate:

```text
registry records
trade activity
procurement
news
regulation
geography
ownership
internal commercial evidence
```

around one correctly resolved entity.

---

# 147. Supplier Intelligence

A tenant may ask:

> What do we know about this supplier?

Pulse may correlate the tenant's supplier identity with permitted external evidence while preserving tenant confidentiality.

---

# 148. Buyer Discovery

Pulse may identify:

```text
potential buyers
importers
distributors
processors
retailers
manufacturers
```

from fragmented sources and reconcile them into candidate entities.

---

# 149. Commercial Opportunity

This creates the basis for commercial products such as:

```text
Buyer Discovery Reports
Supplier Intelligence Reports
Competitor Intelligence
Corporate Due Diligence
Market Participant Mapping
Distributor Discovery
Trade Counterparty Research
```

---

# 150. Buyer Discovery Example

Suppose Pulse observes:

```text
Importer name in customs data
+
similar company in registry
+
matching website
+
industry directory listing
+
trade-fair exhibitor profile
+
recent news article
```

Pulse may construct:

```text
Observed Identities
        ↓
Candidate Resolution
        ↓
Evidence Assessment
        ↓
Resolved Company
        ↓
Company Dossier
        ↓
Buyer Opportunity
```

---

# 151. Resolution Confidence in Reports

Commercial reports SHOULD distinguish:

```text
VERIFIED ENTITY
HIGH-CONFIDENCE MATCH
PROBABLE MATCH
UNRESOLVED
```

where relevant.

---

# 152. No False Certainty

Pulse SHALL never present:

```text
Probable Company X
```

as:

```text
Company X
```

without appropriate qualification.

---

# 153. Network Intelligence

Once identities are resolved, Pulse may analyse networks such as:

```text
Company
   ↓
Directors
   ↓
Other Companies
   ↓
Suppliers
   ↓
Markets
   ↓
Trade Flows
```

subject to lawful data use.

---

# 154. Relationship Does Not Imply Misconduct

Shared:

```text
director
address
supplier
customer
```

relationships SHALL not automatically imply improper affiliation.

---

# 155. Risk of Over-Inference

Pulse SHALL separate:

```text
observed relationship
```

from:

```text
interpretation of relationship.
```

---

# 156. Corporate Family Resolution

Pulse MAY identify candidate corporate families.

Family membership SHALL remain distinct from legal identity.

---

# 157. Market Participant Mapping

A MarketParticipant projection MAY organise resolved entities by:

```text
role
sector
geography
trade activity
size
products
```

---

# 158. Role Is Contextual

A company may simultaneously be:

```text
importer
processor
distributor
exporter
retailer
```

depending upon product and market.

---

# 159. Entity Role Temporal Semantics

Roles MAY vary over time.

---

# 160. Entity Resolution Service

Pulse SHALL expose a logical:

```text
EntityResolutionService
```

---

# 161. Responsibilities

The service SHALL conceptually support:

```text
normalise_identity()
generate_candidates()
extract_features()
assess_candidate()
detect_contradictions()
resolve()
request_review()
propose_mapping()
explain_resolution()
```

---

# 162. Resolution Explanation

Every consequential resolution SHOULD support:

```text
EXPLAIN_RESOLUTION(resolution_id)
```

---

# 163. Explanation

The result SHOULD include:

```text
candidate
supporting evidence
contradictory evidence
method
score/probability
confidence
policy
decision
review history
```

subject to access controls.

---

# 164. Repository Boundaries

Pulse MAY maintain repositories for:

```text
ObservedIdentity
ResolutionCandidate
ResolutionAssessment
ResolutionReview
MappingProposal
```

These are Pulse analytical objects.

CanonicalEntity and authoritative Mapping remain Control Plane concepts.

---

# 165. CP Integration

Pulse SHALL communicate mapping proposals through an explicit Control Plane contract.

---

# 166. No Direct CP Database Mutation

Pulse SHALL never directly write Control Plane mapping tables.

---

# 167. Shared Contracts

Cross-engine contracts for:

```text
CanonicalEntity reference
ExternalReference
Mapping
MappingProposal events
```

SHALL reside in `nabhold/shared`.

---

# 168. Canonical Events

Potential events include:

```text
pulse.identity.candidate.discovered
pulse.identity.resolution.confirmed
pulse.identity.resolution.rejected
pulse.identity.resolution.superseded
pulse.mapping.proposed
cp.mapping.approved
cp.mapping.rejected
cp.canonical-entity.merged
cp.canonical-entity.split
```

Exact schemas belong in `nabhold/shared`.

---

# 169. Idempotency

Repeated ingestion of the same identity evidence SHALL not create uncontrolled duplicate candidates.

---

# 170. Candidate Deduplication

Candidate identity SHOULD consider:

```text
observed identity
candidate target
scope
method version
```

where appropriate.

---

# 171. Resolution Cache

Resolution results MAY be cached.

The canonical resolution record remains authoritative.

---

# 172. Cache Invalidation

Mapping changes SHALL invalidate affected caches.

---

# 173. Search Index

Search MAY accelerate candidate generation.

Search SHALL not become identity authority.

---

# 174. Vector Similarity

Embeddings MAY assist candidate discovery for:

```text
names
descriptions
addresses
organisation profiles
```

but vector similarity SHALL remain candidate-generation evidence.

---

# 175. Vector Match Is Not Identity

High embedding similarity SHALL never alone create an authoritative mapping.

---

# 176. LLM Resolution

LLMs MAY assist with:

```text
alias interpretation
multilingual names
address parsing
relationship extraction
candidate explanation
```

---

# 177. LLM Constraint

An LLM SHALL not autonomously approve consequential canonical mappings solely from its own reasoning.

---

# 178. External Search

Research workflows MAY seek additional public evidence when resolution remains ambiguous.

---

# 179. Research Escalation

Conceptually:

```text
AMBIGUOUS
   ↓
SEARCH FOR ADDITIONAL EVIDENCE
   ↓
REASSESS
   ↓
CONFIRM / REJECT / REMAIN AMBIGUOUS
```

---

# 180. Cost-Aware Resolution

External research MAY incur:

```text
API cost
commercial dataset cost
analyst time
```

Pulse SHOULD allow materiality-based escalation.

---

# 181. Resolution Budget

A ResearchMission MAY define an entity-resolution research budget.

---

# 182. Commercial Research Implication

For premium research, spending additional resources to correctly identify a strategically important company may be economically justified.

---

# 183. Identity Confidence Decay

Identity confidence MAY require reassessment when:

```text
company restructures
domain changes
registry status changes
ownership changes
mapping is challenged
```

---

# 184. Stable Legal Identity

Ordinary changes in:

```text
address
directors
website
```

SHALL not automatically imply a new legal entity.

---

# 185. Identity Change Event

Where evidence suggests an actual identity transition, Pulse SHALL distinguish:

```text
ATTRIBUTE_CHANGED
```

from:

```text
ENTITY_CHANGED.
```

---

# 186. Company Closure

Dissolution changes entity state.

It does not erase historical identity.

---

# 187. Historical Entity

Resolved entities SHALL remain usable for historical analysis after closure.

---

# 188. Entity Relevance

Pulse MAY maintain an analytical relevance score for research prioritisation.

It SHALL not be part of canonical identity.

---

# 189. Entity Resolution Metrics

Operational metrics SHOULD include:

```text
candidate volume
auto-resolution rate
human-review rate
ambiguous rate
false-match corrections
resolution latency
canonical proposal acceptance
```

---

# 190. Accuracy Metrics

Where labelled truth sets exist, Pulse SHOULD measure:

```text
precision
recall
false-positive rate
false-negative rate
```

by entity class and resolution policy.

---

# 191. Precision Priority

For high-impact legal-entity matching, Pulse SHOULD generally optimise strongly against false-positive merges.

---

# 192. Drift Monitoring

Resolution performance SHALL be monitored for drift.

---

# 193. Provider Drift

A provider changing:

```text
identifier format
name format
address representation
schema
```

may affect resolution performance.

---

# 194. Language Drift

Expansion into new markets may introduce:

```text
new languages
scripts
legal suffixes
address conventions
```

requiring updated resolution policies.

---

# 195. Regional Extensibility

Resolution SHALL therefore avoid assumptions specific only to South Africa.

---

# 196. African Market Requirements

The architecture SHALL accommodate:

```text
inconsistent digitisation
multiple naming conventions
partial registries
informal trading names
weak identifiers
cross-border entities
multilingual records
changing administrative boundaries
```

without lowering evidence standards.

---

# 197. Missing Identifier

Absence of a registration identifier SHALL not automatically imply low legitimacy.

It may instead imply incomplete source coverage.

---

# 198. Informal Enterprise

Pulse MAY represent observed economic actors that are not registered legal entities.

They SHALL not be falsely promoted to `LEGAL_ENTITY`.

---

# 199. Unknown Entity Type

Where entity type cannot be determined, Pulse SHALL permit:

```text
UNKNOWN
```

or an equivalent unresolved type.

---

# 200. No Premature Classification

A news mention such as:

```text
"ABC Coffee"
```

may initially be:

```text
ObservedIdentity(entity_type=UNKNOWN)
```

until evidence clarifies whether it is:

```text
company
brand
product
farm
cooperative
```

---

# 201. Cooperatives

Cooperatives SHALL be treated according to their actual legal/organisational form, not forced into ordinary corporate assumptions.

---

# 202. Government Bodies

Government ministries, departments, agencies, authorities and state-owned enterprises SHALL remain distinguishable.

---

# 203. Government Restructuring

Renamed or reorganised government agencies MAY require:

```text
SUCCESSOR_OF
PREDECESSOR_OF
```

rather than simple aliasing.

---

# 204. Regulatory Authority Resolution

Correct regulator identity is important for regulatory intelligence.

---

# 205. Source Organisation Resolution

Even data providers themselves MAY require canonical entity resolution.

---

# 206. Source Provenance Preservation

Resolving a source organisation SHALL not erase the exact source name appearing on the acquired artefact.

---

# 207. Research Entity Universe

Each ResearchMission MAY define an entity universe relevant to its purpose.

---

# 208. Entity Universe

Examples:

```text
coffee importers in Germany
solar equipment distributors in East Africa
fertiliser manufacturers serving Uganda
cold-chain operators in Southern Africa
```

---

# 209. Universe Membership

Membership SHALL be evidence-backed and temporally scoped.

---

# 210. Entity Discovery

Pulse MAY discover entities not previously known to the platform.

---

# 211. Discovery Does Not Equal Canonical Creation

Newly discovered entities SHALL initially enter the resolution workflow.

---

# 212. Canonical Creation Proposal

If no existing CanonicalEntity matches and the entity is sufficiently material, Pulse MAY propose creation of a new canonical entity through the Control Plane.

---

# 213. Creation Evidence

Such a proposal SHOULD include:

```text
entity type
authoritative identifiers
name
jurisdiction
supporting sources
confidence
provenance
```

---

# 214. Duplicate Prevention

Canonical creation workflows SHOULD perform duplicate checks before approval.

---

# 215. Entity Resolution and Opportunity Discovery

Accurate identity resolution enables Pulse to recognise:

```text
the same buyer
appearing across
multiple import datasets
+
registry filings
+
trade fairs
+
procurement awards
+
news
```

rather than counting each appearance as a different organisation.

---

# 216. Commercial Signal

Repeated cross-source appearance MAY become an analytical signal.

It SHALL not itself prove identity; identity must first be resolved.

---

# 217. Emerging Company Signal

Pulse MAY detect a company whose:

```text
imports are increasing
hiring is increasing
facilities are expanding
procurement awards are increasing
news presence is increasing
```

across independently sourced evidence.

---

# 218. Entity-Centric Opportunity Radar

This enables:

```text
ENTITY
   ↓
ACTIVITY
   ↓
CHANGE
   ↓
SIGNAL
   ↓
OPPORTUNITY / RISK
```

---

# 219. Buyer Intent Intelligence

With sufficient lawful evidence, Pulse may infer probable commercial intent from patterns such as:

```text
increasing imports
new warehouse
new procurement
new licence
new market entry
new product registration
```

Such intent SHALL be an Insight or Signal, never an identity fact.

---

# 220. Competitive Intelligence

Resolved company identities enable comparisons of:

```text
market presence
trade activity
geographic expansion
product portfolio
regulatory exposure
news momentum
```

subject to evidence availability.

---

# 221. Market Structure Mapping

Pulse may identify:

```text
major buyers
major sellers
intermediaries
processors
distributors
logistics nodes
```

within a market.

---

# 222. Entity Concentration

Entity resolution is necessary before calculating market concentration.

Otherwise duplicate names can materially distort results.

---

# 223. Supply-Chain Graph

Resolved identities may support:

```text
Producer
   ↓
Exporter
   ↓
Importer
   ↓
Distributor
   ↓
Retailer
```

where evidence lawfully supports those relationships.

---

# 224. Relationship Confidence

Supply-chain relationships SHALL carry their own evidence/confidence.

Correct entity resolution does not automatically prove a business relationship.

---

# 225. Due Diligence Product

Pulse may assemble:

```text
identity verification
registry evidence
ownership
directors
trade activity
news
regulatory exposure
geographic presence
commercial signals
```

into evidence-backed due-diligence intelligence.

---

# 226. Resolution Transparency

Premium due-diligence products SHOULD be capable of exposing why Pulse believes different source records refer to the same entity.

---

# 227. Confidence Disclosure

Where identity materially affects conclusions, reports SHOULD disclose material identity uncertainty.

---

# 228. Identity Risk

A high-value analysis depending upon uncertain entity resolution MAY itself carry an:

```text
IDENTITY_RISK
```

limitation.

---

# 229. Resolution Quality and Intelligence Quality

Poor identity resolution can produce excellent-looking but false analytics.

Entity resolution SHALL therefore be treated as part of intelligence quality.

---

# 230. Rejected Alternative — Name Equality

Rejected.

Names are not unique identities.

---

# 231. Rejected Alternative — Fuzzy Name Matching Alone

Rejected.

It creates unacceptable false merges.

---

# 232. Rejected Alternative — LLM Decides Identity

Rejected.

LLMs may assist but SHALL not become canonical identity authority.

---

# 233. Rejected Alternative — Pulse Owns Canonical Registry

Rejected.

Canonical platform identity remains a Control Plane responsibility.

---

# 234. Rejected Alternative — Provider IDs as Canonical IDs

Rejected.

Provider identities remain external references.

---

# 235. Rejected Alternative — Merge First, Correct Later

Rejected.

False merges contaminate downstream intelligence and may be expensive to unwind.

---

# 236. Rejected Alternative — Never Resolve Automatically

Rejected.

Deterministic and sufficiently high-confidence policy-controlled resolution is necessary at scale.

---

# 237. Rejected Alternative — One Universal Matching Model

Rejected.

Entity classes have materially different identity semantics.

---

# 238. Rejected Alternative — Delete Wrong Resolutions

Rejected.

Incorrect historical resolutions SHALL be superseded so historical analytical state remains reconstructable.

---

# 239. Governing Invariants

**ENTITY-PULSE-001**  
Similarity SHALL NOT be treated as identity.

**ENTITY-PULSE-002**  
Source identity SHALL remain recoverable.

**ENTITY-PULSE-003**  
Provider identifiers SHALL remain external references unless canonically mapped.

**ENTITY-PULSE-004**  
Pulse SHALL NOT redefine `CanonicalEntity`.

**ENTITY-PULSE-005**  
Existing authoritative Control Plane mappings SHALL take precedence.

**ENTITY-PULSE-006**  
Probabilistic matches SHALL not silently become authoritative mappings.

**ENTITY-PULSE-007**  
Unresolved identity SHALL be a valid state.

**ENTITY-PULSE-008**  
Ambiguity SHALL not be resolved through fabricated certainty.

**ENTITY-PULSE-009**  
Resolution SHALL be entity-type aware.

**ENTITY-PULSE-010**  
Resolution SHALL preserve supporting and contradictory evidence.

**ENTITY-PULSE-011**  
Consequential resolutions SHALL identify their method/policy version.

**ENTITY-PULSE-012**  
Hard contradictions SHALL prevent automatic resolution where policy requires.

**ENTITY-PULSE-013**  
Canonical mapping scope SHALL be respected.

**ENTITY-PULSE-014**  
Tenant-private relationships SHALL not leak through identity resolution.

**ENTITY-PULSE-015**  
Legal entity, organisation, brand, branch and facility SHALL remain semantically distinct.

**ENTITY-PULSE-016**  
Ownership SHALL not imply identity.

**ENTITY-PULSE-017**  
Classification SHALL not imply identity.

**ENTITY-PULSE-018**  
Corporate succession SHALL not be represented as identity equality unless legally appropriate.

**ENTITY-PULSE-019**  
Historical resolution decisions SHALL remain reconstructable.

**ENTITY-PULSE-020**  
Corrected resolutions SHALL supersede rather than silently overwrite consequential history.

**ENTITY-PULSE-021**  
Mapping changes SHALL support downstream impact analysis.

**ENTITY-PULSE-022**  
LLM and vector similarity SHALL be candidate-generation capabilities, not identity authority.

**ENTITY-PULSE-023**  
Human review SHALL be available for material ambiguity.

**ENTITY-PULSE-024**  
Canonical creation and mapping proposals SHALL pass through authorised platform governance.

**ENTITY-PULSE-025**  
Pulse SHALL not directly mutate Control Plane persistence.

**ENTITY-PULSE-026**  
Resolution confidence and model probability SHALL remain distinct.

**ENTITY-PULSE-027**  
Identity uncertainty affecting conclusions SHALL be representable in intelligence quality.

**ENTITY-PULSE-028**  
False-positive merges SHALL be treated as a high-severity quality failure.

**ENTITY-PULSE-029**  
Cross-source resolution SHALL preserve source provenance.

**ENTITY-PULSE-030**  
Entity-resolution semantics SHALL remain independent of search, vector, graph or database technology.

---

# 240. Consequences

## Positive

This decision enables Pulse to safely correlate:

```text
company registries
customs data
trade records
procurement
news
government data
commerce
ERP
content
geospatial evidence
```

without destroying source identity or creating an uncontrolled shadow master-data system.

It creates a foundation for:

```text
company intelligence
buyer discovery
supplier intelligence
competitor intelligence
market participant mapping
due diligence
ownership research
trade-network analysis
opportunity discovery
risk detection
```

## Costs

The architecture requires:

```text
candidate indexes
resolution policies
matching algorithms
review workflows
resolution evidence
mapping governance
temporal resolution history
quality measurement
```

Entity resolution is therefore a substantial capability rather than a utility function.

That complexity is justified because cross-source intelligence is impossible to trust if the platform cannot reliably determine what its evidence is actually about.

---

# 241. Strategic Consequence — Pulse Can Discover Economic Actors

Most conventional research starts with a company name and searches for information about it.

Pulse can eventually work in the opposite direction:

```text
TRADE ACTIVITY
      +
PROCUREMENT
      +
REGISTRY FILINGS
      +
NEWS
      +
FACILITY EXPANSION
      ↓
ENTITY RESOLUTION
      ↓
ECONOMIC ACTOR
      ↓
COMMERCIAL SIGNIFICANCE
```

This allows Pulse to discover potentially important companies before an analyst deliberately searches for them.

---

# 242. Strategic Consequence — Buyer Discovery Becomes a Product

Consider a producer seeking buyers for green coffee.

Instead of providing:

```text
a directory of coffee companies
```

Pulse may construct:

```text
IMPORT RECORDS
      ↓
identify importer names
      ↓
resolve legal entities
      ↓
registry verification
      ↓
website / product verification
      ↓
historical import behaviour
      ↓
market activity
      ↓
growth trajectory
      ↓
buyer qualification
      ↓
BUYER OPPORTUNITY REPORT
```

The output becomes more valuable than a contact list because it explains:

```text
who the buyer is
what they appear to buy
where they operate
how active they are
whether activity is growing
why they may be commercially relevant
how confident Pulse is in the identity
```

---

# 243. Strategic Consequence — The Company Dossier Compounds

Once Pulse has resolved an organisation correctly, future evidence can accumulate around the canonical entity:

```text
                       COMPANY
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     REGISTRY           TRADE              NEWS
        │                 │                 │
        ▼                 ▼                 ▼
    OWNERSHIP          ACTIVITY         EVENTS
        │                 │                 │
        └────────────┬────┴────────────┬────┘
                     ▼                 ▼
                   RISKS          OPPORTUNITIES
```

The dossier becomes richer each time Pulse encounters the entity.

Research investment therefore compounds rather than restarting from zero for each report.

---

# 244. Strategic Consequence — Identity Becomes Reusable Intellectual Capital

Suppose an analyst spends two hours proving that:

```text
ABC Trading Ltd
ABC Foods
ABC Imports
registry number X
domain abc.example
```

refer to one organisation.

That work SHOULD NOT disappear inside a single report.

Subject to governance, the resolution becomes reusable institutional knowledge.

The next research mission begins with a stronger evidence base.

---

# 245. Strategic Consequence — Cross-Market Opportunity Mapping

Entity resolution can eventually allow Pulse to recognise:

```text
Company X
imports coffee in Germany
+
Company X
opens office in Kenya
+
Company X
advertises East African sourcing role
+
Company X
registers new African subsidiary
```

as related evidence.

Pulse may then detect:

```text
POSSIBLE EAST AFRICAN SOURCING EXPANSION
```

before a conventional market report explicitly documents it.

That is the difference between merely collecting information and connecting evidence.

---

# 246. Strategic Consequence — Market Maps Can Become Living Assets

Instead of publishing:

```text
Top 50 Importers — 2026.pdf
```

Pulse can maintain:

```text
MARKET PARTICIPANT UNIVERSE
        │
        ├── identities
        ├── corporate families
        ├── locations
        ├── roles
        ├── trade behaviour
        ├── growth
        ├── risks
        └── opportunities
```

and continuously update it.

From the same underlying intelligence asset Nabhold could derive:

```text
market reports
buyer lists
supplier reports
competitor maps
due-diligence briefs
opportunity alerts
sector subscriptions
```

without rebuilding the research foundation for every product.

---

# 247. Strategic Consequence — Entity Resolution Is Revenue Infrastructure

The value of Pulse will not come only from algorithms that predict markets.

A significant part of its value may come from doing extremely well what real-world research repeatedly struggles with:

> **Figuring out who is actually who.**

Across fragmented African and international datasets, correctly reconciling:

```text
companies
brands
registries
trade records
facilities
ownership
products
locations
```

can itself create valuable proprietary research infrastructure.

The competitive asset is not the raw public record.

The competitive asset is the accumulated, evidence-backed understanding of how records across many sources relate to the real economy.

---

# 248. Final Decision Statement

Baobab Pulse SHALL implement entity resolution as a **versioned, evidence-backed, type-aware, temporally aware and governance-controlled analytical capability**.

The canonical resolution architecture SHALL be:

```text
                       SOURCE RECORD
                             │
                             ▼
                     OBSERVED IDENTITY
                             │
                             ▼
                       NORMALISATION
                             │
                             ▼
                    CANDIDATE GENERATION
                             │
                             ▼
                    EVIDENCE ASSESSMENT
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
          DETERMINISTIC  PROBABILISTIC  AMBIGUOUS
                │            │            │
                ▼            ▼            ▼
             CONFIRM       REVIEW       RESEARCH
                │            │            │
                └────────────┼────────────┘
                             ▼
                    RESOLUTION DECISION
                             │
                             ▼
                  CANONICAL MAPPING PROPOSAL
                             │
                             ▼
                     BAOBAB CONTROL PLANE
                             │
                             ▼
                     CANONICAL ENTITY
                             │
                             ▼
                 CROSS-SOURCE INTELLIGENCE
```

Pulse SHALL be sophisticated enough to discover identity relationships but disciplined enough to admit uncertainty.

It SHALL preserve the fundamental distinction:

```text
"We found two similar records."
```

is not the same statement as:

```text
"We have evidence that these records describe the same real-world entity."
```

And the latter is still not automatically the same as:

```text
"Baobab has accepted this as the canonical platform mapping."
```

Those boundaries are what allow entity intelligence to scale without contaminating the platform's identity model.

The result is not merely data cleaning.

It is the foundation upon which Pulse can build trustworthy **company intelligence, buyer discovery, supplier discovery, competitor mapping, due diligence, market structure analysis and cross-source opportunity detection**.