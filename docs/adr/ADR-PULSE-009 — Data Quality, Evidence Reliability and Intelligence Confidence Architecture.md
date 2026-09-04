# ADR-PULSE-009 — Data Quality, Evidence Reliability and Intelligence Confidence Architecture

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-009`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:** `ADR-PULSE-001` through `ADR-PULSE-008`  
**Decision Type:** Data Quality, Evidence Reliability, Uncertainty and Intelligence Confidence Architecture Decision

---

# 1. Context

Baobab Pulse will operate in an environment where evidence quality varies enormously.

A single ResearchMission may combine:

```text
official government statistics
customs declarations
company registry records
commercial datasets
market prices
commodity benchmarks
weather observations
forecasts
geospatial datasets
company disclosures
news
industry publications
academic research
tenant operational data
AI-extracted observations
human research
```

These sources cannot be assumed equally:

```text
accurate
complete
current
independent
authoritative
consistent
representative
precise
reliable
```

Nor does an authoritative source necessarily contain perfect data.

An official statistical agency may later revise GDP.

A customs dataset may omit informal trade.

A company registry may be legally authoritative but operationally stale.

A newspaper may correctly report an event before an official source acknowledges it.

A commercial provider may produce excellent estimates but obscure its methodology.

Two apparently independent news stories may originate from one press release.

Ten sources repeating the same claim do not necessarily constitute ten independent pieces of evidence.

Pulse therefore requires a quality architecture considerably richer than:

```text
confidence = 87%
```

The platform must preserve *why* evidence is considered trustworthy, where it is weak, what contradicts it, what remains unknown, and how uncertainty propagates into the resulting intelligence.

---

# 2. Decision

Baobab Pulse SHALL implement a **multidimensional, provenance-aware and methodology-governed quality and confidence architecture**.

Quality SHALL be evaluated independently at several levels:

```text
SOURCE
   ↓
DATASET
   ↓
ACQUISITION
   ↓
RAW RECORD
   ↓
OBSERVATION
   ↓
EVIDENCE SET
   ↓
ANALYSIS
   ↓
INSIGHT
   ↓
OPPORTUNITY / RISK / FORECAST
   ↓
RECOMMENDATION
   ↓
INTELLIGENCE PRODUCT
```

Pulse SHALL NOT collapse these assessments into a single universal quality score.

---

# 3. Foundational Principle

> **Confidence is a conclusion about evidence; it is not a substitute for evidence.**

---

# 4. Second Principle

> **Authority is not accuracy.**

---

# 5. Third Principle

> **Quantity of sources is not independence of sources.**

---

# 6. Fourth Principle

> **Missing evidence is not negative evidence.**

---

# 7. Fifth Principle

> **Contradiction is information.**

Pulse SHALL preserve disagreement rather than automatically eliminate it.

---

# 8. Sixth Principle

> **A useful intelligence system must know what it does not know.**

Unknown, uncertain, unavailable, contradictory and insufficient SHALL be legitimate analytical states.

---

# 9. Quality Model

Pulse SHALL distinguish at minimum:

```text
SourceQuality
DatasetQuality
ObservationQuality
EvidenceQuality
AnalysisQuality
IntelligenceConfidence
```

These concepts SHALL remain related but separate.

---

# 10. QualityProfile

The Canonical Intelligence Model's `QualityProfile` SHALL represent multidimensional quality.

Conceptually:

```text
QualityProfile
 ├── accuracy
 ├── completeness
 ├── timeliness
 ├── consistency
 ├── authority
 ├── corroboration
 ├── methodology_quality
 ├── representativeness
 ├── precision
 ├── traceability
 └── overall_assessment
```

Not every dimension SHALL apply to every object.

---

# 11. Quality Dimensions Are Not Probabilities

A quality dimension SHALL not automatically be represented as:

```text
0.87
```

unless the methodology gives that number defensible meaning.

Ordinal scales MAY often be more appropriate.

---

# 12. Standard Quality Scale

A canonical qualitative scale SHOULD support:

```text
UNKNOWN
VERY_LOW
LOW
MODERATE
HIGH
VERY_HIGH
```

with machine-readable methodology where necessary.

---

# 13. Source Quality

`SourceQuality` describes characteristics of the source itself.

Possible dimensions include:

```text
authority
institutional reliability
historical accuracy
transparency
methodology disclosure
revision behaviour
publication regularity
independence
coverage
access stability
```

---

# 14. Source Quality Is Contextual

A source may be excellent for one question and poor for another.

Example:

A central bank may be highly authoritative for:

```text
official policy rate
```

but not necessarily for:

```text
retail food prices in a remote district.
```

---

# 15. Source Authority

Authority describes the source's institutional standing with respect to a claim.

Possible classifications MAY include:

```text
PRIMARY_AUTHORITATIVE
PRIMARY_NON_AUTHORITATIVE
SECONDARY_AUTHORITATIVE
SPECIALIST
COMMERCIAL
ACADEMIC
JOURNALISTIC
COMMUNITY
INTERNAL
UNKNOWN
```

Exact shared vocabulary SHALL be governed in `nabhold/shared`.

---

# 16. Legal Authority

Legal authority SHALL be distinguished from empirical accuracy.

A government gazette may be legally authoritative concerning:

```text
whether a regulation was promulgated
```

even if it says nothing about:

```text
whether businesses will comply with it.
```

---

# 17. First-Party Source

A first-party source may be authoritative regarding:

```text
what the organisation claims
```

but not necessarily:

```text
whether the claim is objectively correct.
```

---

# 18. Company Disclosure

For example:

```text
Company X announces:
"We are the market leader."
```

The evidence proves strongly that:

```text
Company X made the claim.
```

It does not automatically prove:

```text
Company X is the market leader.
```

Pulse SHALL model this distinction.

---

# 19. Claim Scope

Evidence quality SHALL be evaluated relative to the exact claim being supported.

---

# 20. Dataset Quality

`DatasetQuality` evaluates the characteristics of a dataset or dataset version.

Possible dimensions include:

```text
coverage
completeness
methodology
revision frequency
schema stability
geographic coverage
temporal coverage
sampling quality
missingness
duplication
internal consistency
```

---

# 21. Dataset Version Quality

Quality SHALL be capable of varying between DatasetVersions and DataVintages.

---

# 22. Acquisition Quality

Pulse SHALL assess whether acquisition was complete and technically trustworthy.

Possible conditions:

```text
COMPLETE
PARTIAL
TRUNCATED
CORRUPT
SCHEMA_DRIFTED
RATE_LIMITED
CHECKSUM_FAILED
UNKNOWN
```

---

# 23. Acquisition Failure Is Not Source Failure

A poor acquisition does not imply that the underlying source is poor.

---

# 24. Observation Quality

Each canonical Observation MAY carry quality information derived from:

```text
source quality
dataset quality
raw-record validity
normalisation quality
temporal precision
unit precision
entity-resolution confidence
validation results
```

---

# 25. Observation Validation

Validation SHALL distinguish:

```text
syntactic validation
structural validation
semantic validation
domain validation
cross-source validation
```

---

# 26. Syntactic Validation

Examples:

```text
valid number
valid date
valid identifier syntax
valid encoding
```

---

# 27. Structural Validation

Examples:

```text
required fields present
expected columns present
schema valid
record cardinality valid
```

---

# 28. Semantic Validation

Examples:

```text
currency exists
country code exists
HS code valid for declared revision
unit understood
entity type compatible
```

---

# 29. Domain Validation

Examples:

```text
exchange rate > 0
quantity not physically impossible
tariff within expected representation
forecast target after forecast origin
```

Domain validation SHALL be conservative enough not to reject legitimate extreme observations merely because they are unusual.

---

# 30. Cross-Source Validation

Pulse MAY compare an Observation with other evidence.

Disagreement SHALL not automatically invalidate either observation.

---

# 31. Validation Result

Conceptually:

```text
ValidationResult
 ├── rule_id
 ├── rule_version
 ├── status
 ├── severity
 ├── message
 ├── observed_value
 ├── expected_condition
 ├── evaluated_at
 └── evidence
```

---

# 32. Validation Status

Possible states:

```text
PASS
WARN
FAIL
UNKNOWN
NOT_APPLICABLE
```

---

# 33. Severity

Possible severity:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

---

# 34. Validation Failure Policy

A failed validation MAY:

```text
reject
quarantine
accept-with-warning
require-review
```

according to policy.

---

# 35. Quality Rule

A `QualityRule` SHALL be versioned.

---

# 36. No Silent Cleaning

Pulse SHALL NOT silently transform obviously suspicious data into plausible values merely to make a dataset appear clean.

---

# 37. Source Value Preservation

The original value SHALL remain recoverable.

---

# 38. Corrected Value

A corrected or normalised value SHALL be explicitly derived.

---

# 39. Quality Issue

Pulse SHALL model significant problems as explicit `QualityIssue` objects or equivalent domain records.

Conceptually:

```text
QualityIssue
 ├── issue_id
 ├── subject_ref
 ├── issue_type
 ├── severity
 ├── detected_at
 ├── detector
 ├── description
 ├── evidence
 ├── status
 └── resolution
```

---

# 40. Quality Issue Types

Examples:

```text
MISSING_VALUE
DUPLICATE
OUTLIER
SCHEMA_DRIFT
TEMPORAL_GAP
INVALID_UNIT
ENTITY_AMBIGUITY
SOURCE_CONTRADICTION
STALE_DATA
PARTIAL_ACQUISITION
METHODOLOGY_CHANGE
REVISION
UNEXPECTED_VALUE
INSUFFICIENT_COVERAGE
```

---

# 41. Missingness

Pulse SHALL preserve missing-value semantics from the Canonical Intelligence Model:

```text
UNKNOWN
NOT_AVAILABLE
NOT_APPLICABLE
WITHHELD
NOT_COLLECTED
```

---

# 42. Missing Is Not Zero

This SHALL be a hard invariant.

---

# 43. Suppressed Data

Statistically suppressed values SHALL not be interpreted as zero.

---

# 44. Confidential Values

`WITHHELD` SHALL remain distinct from `NOT_AVAILABLE`.

---

# 45. Missingness Pattern

Patterns of missing data MAY themselves become analytically meaningful.

---

# 46. Completeness

Completeness SHALL be assessed relative to an expected universe.

Example:

```text
expected 54 countries
received 52
```

has a different meaning from:

```text
52 records received
expected universe unknown.
```

---

# 47. Coverage

Coverage SHALL distinguish dimensions such as:

```text
geographic
temporal
entity
product
population
market
```

---

# 48. Representativeness

A dataset may be complete relative to its own scope yet not represent the wider population.

---

# 49. Example

A survey of formal retailers may be complete but unrepresentative of a market where informal trade is substantial.

---

# 50. Precision

Pulse SHALL preserve measurement precision.

---

# 51. False Precision

A value estimated as:

```text
approximately USD 10 million
```

SHALL not become:

```text
USD 10,000,000.00
```

without retaining the uncertainty/precision semantics.

---

# 52. Measurement Uncertainty

Where a source supplies confidence intervals, margins of error or uncertainty ranges, Pulse SHALL preserve them.

---

# 53. Estimate versus Measurement

Pulse SHALL distinguish:

```text
MEASURED
REPORTED
ESTIMATED
MODELLED
IMPUTED
DERIVED
FORECAST
```

where relevant.

---

# 54. Imputation

Imputed values SHALL never masquerade as source measurements.

---

# 55. Imputation Method

Every material imputation SHALL identify:

```text
method
method_version
input observations
parameters
```

---

# 56. Outliers

Outliers SHALL be flagged, not automatically deleted.

---

# 57. Outlier Is Not Error

Extreme observations may represent important:

```text
market shocks
policy changes
supply disruptions
fraud
crises
opportunities
```

---

# 58. Outlier Classification

Pulse SHOULD distinguish:

```text
DATA_ERROR_SUSPECTED
LEGITIMATE_EXTREME
STRUCTURAL_BREAK_CANDIDATE
UNKNOWN
```

where analysis supports such distinction.

---

# 59. Duplicate Evidence

Duplicate source records SHALL be detectable.

---

# 60. Duplicate Evidence Is Not Corroboration

The same underlying record appearing in several feeds SHALL not count as independent corroboration.

---

# 61. Corroboration

`Corroboration` SHALL measure the degree to which materially independent evidence supports a claim.

---

# 62. Independence

Pulse SHALL attempt to determine whether sources are genuinely independent.

---

# 63. Source Dependency

Possible dependencies include:

```text
syndicated news
press release republication
shared upstream dataset
data reseller
government dataset mirrored elsewhere
research report citing another report
```

---

# 64. Evidence Dependency Graph

Pulse SHOULD represent material source dependencies in the Evidence Graph.

---

# 65. Corroboration Unit

Corroboration SHOULD be counted at the level of independent evidence lineage rather than raw citation count.

---

# 66. Example

```text
Article A → Reuters
Article B → Reuters
Article C → Reuters
Article D → Reuters
```

may represent essentially:

```text
one originating evidence lineage
```

rather than four independent confirmations.

---

# 67. Independent Confirmation

A registry filing plus:

```text
customs evidence
company disclosure
independent market data
```

may constitute stronger corroboration.

---

# 68. Contradiction

Pulse SHALL explicitly model contradiction.

---

# 69. Evidence Direction

Consistent with the Canonical Intelligence Model:

```text
SUPPORTS
CONTRADICTS
NEUTRAL
CONTEXTUAL
```

SHALL remain explicit.

---

# 70. Contradiction Register

Material ResearchMissions SHOULD maintain a `ContradictionRegister`.

---

# 71. Contradiction Record

Conceptually:

```text
Contradiction
 ├── contradiction_id
 ├── subject
 ├── claim_a
 ├── claim_b
 ├── evidence_a
 ├── evidence_b
 ├── materiality
 ├── status
 ├── assessment
 └── resolution
```

---

# 72. Contradiction States

Possible states:

```text
OPEN
EXPLAINED
RESOLVED
UNRESOLVED
SUPERSEDED
```

---

# 73. Explanation Is Not Erasure

If contradiction is explained by:

```text
different time periods
different definitions
different geographies
different methodologies
```

both source observations SHALL remain.

---

# 74. Example — Trade Data

Exporter-reported trade and importer-reported trade may differ.

Pulse SHALL not simply select whichever number appears larger or newer.

---

# 75. Mirror Statistics

Such differences may arise from:

```text
FOB versus CIF valuation
timing
transshipment
classification
reporting error
informal trade
partner attribution
```

The discrepancy may itself be analytically useful.

---

# 76. Example — Market Size

Three reports may estimate:

```text
USD 800M
USD 1.1B
USD 1.6B
```

Pulse SHALL examine:

```text
definition
year
geography
method
included segments
currency basis
```

before synthesising a conclusion.

---

# 77. Disagreement Range

Where reconciliation is not justified, Pulse MAY report a range or competing estimates.

---

# 78. Evidence Sufficiency

Pulse SHALL assess whether evidence is sufficient for the requested analytical claim.

---

# 79. Evidence Sufficiency Is Question-Specific

The evidence required to state:

```text
"coffee exports increased"
```

differs from that required to recommend:

```text
"invest R100 million in a processing plant."
```

---

# 80. Consequence Sensitivity

Higher-consequence recommendations SHALL require stronger evidence and governance.

---

# 81. Evidence Requirement

A ResearchMission or methodology MAY define:

```text
EvidenceRequirement
 ├── claim_type
 ├── minimum_source_classes
 ├── minimum_independent_sources
 ├── authority_requirement
 ├── freshness_requirement
 ├── geographic_coverage
 ├── temporal_coverage
 ├── contradiction_policy
 └── minimum_confidence
```

---

# 82. Evidence Coverage

Pulse SHOULD calculate evidence coverage against the EvidencePlan.

---

# 83. Evidence Gap

An unmet EvidenceRequirement SHALL create an explicit `EvidenceGap`.

---

# 84. Evidence Gap Types

Examples:

```text
NO_PRIMARY_SOURCE
INSUFFICIENT_CORROBORATION
MISSING_TIME_PERIOD
MISSING_GEOGRAPHY
MISSING_ENTITY_DATA
STALE_SOURCE
UNRESOLVED_CONTRADICTION
METHODOLOGY_UNKNOWN
INSUFFICIENT_SAMPLE
```

---

# 85. Evidence Debt

`EvidenceDebt`, introduced in `ADR-PULSE-003`, SHALL represent unresolved evidence weaknesses accepted temporarily for analytical or commercial reasons.

---

# 86. Evidence Debt Is Not Hidden

Every material EvidenceDebt item SHALL remain visible to the analysis and publication quality process.

---

# 87. Evidence Debt Record

Conceptually:

```text
EvidenceDebt
 ├── debt_id
 ├── subject
 ├── missing_requirement
 ├── reason
 ├── materiality
 ├── accepted_by
 ├── accepted_at
 ├── review_by
 └── status
```

---

# 88. Evidence Debt Lifecycle

```text
OPEN
ACCEPTED
MITIGATED
RESOLVED
EXPIRED
```

---

# 89. Evidence Debt Budget

Premium intelligence products MAY establish maximum acceptable evidence debt.

---

# 90. Publication Blocking

Critical unresolved EvidenceDebt MAY block publication.

---

# 91. Confidence

Confidence represents Pulse's justified degree of belief in a particular analytical assertion.

---

# 92. Confidence Is Object-Specific

There SHALL NOT be one universal confidence value for an entire ResearchMission.

Different claims may have different confidence.

---

# 93. Confidence Targets

Confidence MAY apply to:

```text
Observation interpretation
Entity resolution
Signal
Insight
Claim
Opportunity
Risk
Forecast
Recommendation
```

---

# 94. Confidence Vocabulary

The canonical confidence scale SHALL support:

```text
VERY_LOW
LOW
MODERATE
HIGH
VERY_HIGH
```

plus:

```text
UNKNOWN
```

where necessary.

---

# 95. Confidence Method

Every material confidence assessment SHALL identify how it was determined.

---

# 96. Confidence Method Types

Possible methods:

```text
RULE_BASED
STATISTICAL
MODEL_CALIBRATED
EXPERT_ASSESSED
EVIDENCE_WEIGHTED
HYBRID
```

---

# 97. Confidence Explanation

A consequential confidence assessment SHOULD be explainable as:

```text
HIGH because:
- official registry evidence confirms identity;
- customs records independently corroborate activity;
- observations are current;
- no material contradiction exists.

Limited because:
- market-share estimate relies on incomplete informal-market data.
```

---

# 98. No Arbitrary Percentage

Pulse SHALL NOT produce:

```text
confidence = 93.7%
```

unless a calibrated methodology supports that interpretation.

---

# 99. Probability

Where a statistical model genuinely estimates probability, Pulse MAY preserve the probability separately.

---

# 100. Probability Is Not Confidence

Example:

```text
P(currency depreciation > 10%) = 0.68
```

is not equivalent to:

```text
confidence in forecast = 68%.
```

---

# 101. Forecast Confidence

Forecasts SHOULD distinguish:

```text
predicted value
prediction interval
model uncertainty
data uncertainty
scenario uncertainty
confidence assessment
```

where methodology permits.

---

# 102. Risk Probability

Risk objects MAY include estimated:

```text
probability
impact
```

but both SHALL retain methodology.

---

# 103. Opportunity Confidence

Opportunity confidence SHALL describe confidence that the identified commercial condition exists.

It SHALL remain distinct from:

```text
opportunity attractiveness
```

and:

```text
expected commercial return.
```

---

# 104. Example

Pulse might conclude:

```text
Opportunity existence confidence: HIGH
Commercial attractiveness: MODERATE
Execution feasibility: LOW
```

These SHALL remain separate.

---

# 105. Recommendation Confidence

Recommendation confidence SHALL incorporate the strength of evidence supporting the recommendation.

It SHALL not represent certainty of successful execution.

---

# 106. Quality Propagation

Quality and confidence SHALL propagate through derivations according to explicit methodology.

---

# 107. No Naïve Averaging

Pulse SHALL NOT simply calculate:

```text
average(upstream_quality_scores)
```

for consequential intelligence.

---

# 108. Weakest-Link Effects

Some conclusions depend critically on one uncertain assumption.

Such dependency SHALL be capable of limiting overall confidence.

---

# 109. Redundant Evidence Effects

Multiple independent supporting sources MAY increase confidence.

---

# 110. Correlated Evidence

Multiple correlated sources SHALL provide less confidence gain than truly independent evidence.

---

# 111. Contradictory Evidence Effects

Material contradiction SHOULD reduce confidence or require explicit resolution.

---

# 112. Freshness Effects

Stale material evidence MAY reduce confidence.

---

# 113. Entity Resolution Effects

Uncertain entity resolution MAY reduce downstream confidence.

---

# 114. Methodology Effects

Weak methodology MAY limit confidence even when source data is excellent.

---

# 115. Confidence Composition

Conceptually:

```text
Evidence Quality
      +
Corroboration
      +
Method Quality
      +
Temporal Fitness
      +
Coverage
      -
Contradictions
      -
Material Missingness
      -
Identity Uncertainty
      =
JUSTIFIED CONFIDENCE
```

This is a conceptual relationship, not a universal arithmetic formula.

---

# 116. Confidence Policy

Different analytical methodologies MAY define different confidence-composition rules.

---

# 117. Methodology Versioning

Confidence policies SHALL be versioned.

---

# 118. Reproducibility

Historical confidence assessments SHALL remain reproducible according to the evidence and methodology available at the time.

---

# 119. Revised Confidence

New evidence MAY cause confidence to change.

---

# 120. Confidence Revision

A changed confidence assessment SHALL produce a new analytical version where consequential.

---

# 121. Confidence History

Pulse SHOULD preserve confidence evolution.

Example:

```text
March    LOW
April    MODERATE
June     HIGH
```

---

# 122. Confidence Trajectory

The trajectory itself may indicate an emerging opportunity becoming better substantiated.

---

# 123. Weak Signal

A `WeakSignal` SHALL be permitted when evidence is insufficient for a full Signal or Opportunity but potentially commercially significant.

---

# 124. Weak Signal Principle

> **Low confidence does not mean low importance.**

---

# 125. Example

One credible early source may indicate:

```text
a major manufacturer is considering entering Uganda.
```

Confidence may be:

```text
LOW
```

while potential impact is:

```text
VERY_HIGH.
```

Pulse SHOULD preserve that distinction.

---

# 126. Weak Signal Lifecycle

Conceptually:

```text
DETECTED
   ↓
MONITORING
   ↓
CORROBORATED
   ↓
PROMOTED
```

or:

```text
DISCONFIRMED
EXPIRED
```

---

# 127. Emerging Opportunity Candidate

An `EmergingOpportunityCandidate` MAY arise from weak signals.

It SHALL not be represented as a qualified Opportunity until the applicable evidence threshold is met.

---

# 128. Signal Promotion

Promotion SHALL be governed by methodology.

---

# 129. Evidence Accumulation

Conceptually:

```text
WEAK EVIDENCE
      ↓
WEAK SIGNAL
      ↓
MORE EVIDENCE
      ↓
CORROBORATED SIGNAL
      ↓
ANALYSIS
      ↓
OPPORTUNITY CANDIDATE
      ↓
QUALIFIED OPPORTUNITY
```

---

# 130. Evidence Decay

Some evidence becomes less useful with age.

Pulse MAY model evidence relevance decay where justified.

---

# 131. No Universal Decay

A legal incorporation record may remain relevant for decades.

A market price may decay within hours.

---

# 132. Quality and Temporal Architecture

Freshness SHALL integrate with `ADR-PULSE-007`.

---

# 133. Quality and Entity Resolution

Identity uncertainty SHALL integrate with `ADR-PULSE-008`.

---

# 134. Quality and Provenance

Every material quality assessment SHALL remain traceable through `ADR-PULSE-006`.

---

# 135. Quality and Raw Evidence

A quality assessment SHALL never destroy the underlying evidence defined by `ADR-PULSE-004`.

---

# 136. Source Scorecard

Pulse SHOULD maintain a `SourceScorecard`.

Conceptually:

```text
SourceScorecard
 ├── source_id
 ├── domain
 ├── authority
 ├── coverage
 ├── timeliness
 ├── historical_reliability
 ├── revision_behaviour
 ├── technical_reliability
 ├── methodology_transparency
 ├── independence
 ├── commercial_rights
 ├── evaluated_at
 └── methodology_version
```

---

# 137. Source Scorecard Is Not Global Ranking

A single:

```text
World Bank = 92
News Site = 64
```

style ranking SHALL be avoided as the primary model.

---

# 138. Domain-Specific Source Assessment

The same source may have different scorecards by:

```text
dataset
indicator
geography
time period
domain
```

where justified.

---

# 139. Source Reliability History

Pulse SHOULD learn from historical source behaviour.

---

# 140. Reliability Signals

Examples include:

```text
publication delays
revision magnitude
schema failures
missing periods
contradiction frequency
acquisition failures
```

---

# 141. Source Revision Behaviour

Pulse MAY calculate revision profiles.

---

# 142. Early Estimate Reliability

For a statistical source, Pulse MAY learn:

```text
first release usually revised by ±X
```

provided sufficient evidence exists.

---

# 143. Source Latency

Pulse SHOULD measure:

```text
real-world period
→ publication
→ acquisition
```

where useful.

---

# 144. Timeliness Quality

A source may be highly accurate but too delayed for opportunity detection.

---

# 145. Commercial Quality

Pulse SHOULD therefore distinguish:

```text
epistemic quality
```

from:

```text
decision usefulness.
```

---

# 146. Decision Usefulness

A dataset can be:

```text
accurate but late
```

and therefore less useful for time-sensitive commercial decisions.

---

# 147. Decision Fitness

Pulse MAY assess:

```text
DecisionFitness
```

based on:

```text
quality
freshness
coverage
confidence
decision horizon
materiality
```

---

# 148. Fitness-for-Purpose

The central question SHALL be:

> Is this evidence good enough for this decision?

not merely:

> Is this a good dataset?

---

# 149. Quality Gates

Pulse SHALL support quality gates throughout the intelligence pipeline.

---

# 150. Ingestion Gate

Prevents structurally invalid or dangerous evidence from automatically entering normal processing.

---

# 151. Observation Gate

Ensures canonical observations meet domain requirements.

---

# 152. Analysis Gate

Ensures required evidence is available before specified analyses run.

---

# 153. Claim Gate

Ensures a Claim has sufficient traceable evidence.

---

# 154. Recommendation Gate

Ensures consequential Recommendations satisfy stronger evidence requirements.

---

# 155. Publication Gate

Ensures commercial IntelligenceProducts meet product-quality standards.

---

# 156. Quality Gate Result

Possible outcomes:

```text
PASS
PASS_WITH_LIMITATIONS
REVIEW_REQUIRED
BLOCK
```

---

# 157. Product Quality Profile

Each IntelligenceProduct type SHOULD define its required quality profile.

---

# 158. Example — Pulse Snapshot

A low-cost rapid product might permit:

```text
moderate evidence depth
limited manual review
explicit caveats
```

---

# 159. Example — Investment Deep Dive

A premium investment report may require:

```text
primary-source coverage
independent corroboration
manual analyst review
methodology review
contradiction resolution
entity verification
full citation graph
```

---

# 160. Product Price and Quality

Commercial product tiers MAY differ partly by:

```text
research depth
evidence breadth
verification effort
analyst review
update frequency
```

but lower-priced products SHALL never be deliberately misleading.

---

# 161. Minimum Integrity Floor

Every Pulse commercial product SHALL satisfy a minimum integrity floor.

---

# 162. Publication Integrity

A report SHALL NOT be published as established fact when the supporting evidence only justifies speculation.

---

# 163. Claim Strength

Claims SHOULD be classified by epistemic strength.

Possible vocabulary:

```text
OBSERVED
CORROBORATED
ESTIMATED
INFERRED
FORECAST
SCENARIO
HYPOTHESIS
RECOMMENDATION
```

---

# 164. Claim Language

Narrative generation SHOULD reflect claim strength.

Example:

High-confidence observation:

```text
"Imports increased 18%."
```

Inference:

```text
"The evidence suggests..."
```

Weak hypothesis:

```text
"One possible explanation is..."
```

---

# 165. LLM Narrative Constraint

LLMs SHALL NOT upgrade epistemic strength through persuasive wording.

---

# 166. AI Confidence

LLM self-reported confidence SHALL NOT be accepted as intelligence confidence.

---

# 167. Model Output Quality

AI/model output quality SHALL be evaluated against:

```text
grounding
evidence coverage
consistency
task-specific validation
historical performance
```

where appropriate.

---

# 168. Hallucination Detection

Where an LLM generates factual narrative, Pulse SHOULD validate cited factual claims against structured evidence.

---

# 169. Citation Existence Is Not Enough

A citation SHALL support the claim to which it is attached.

---

# 170. Citation Entailment

Pulse MAY implement claim-to-evidence support checks.

---

# 171. Unsupported Claim

A generated Claim without sufficient evidence SHALL be:

```text
UNSUPPORTED
```

and SHALL not pass publication gates.

---

# 172. Claim Coverage

A report SHOULD measure how many material factual claims have evidence support.

---

# 173. Material Claim

Not every stylistic sentence requires independent evidence.

Material factual and analytical claims do.

---

# 174. Evidence Coverage Metric

A publication MAY calculate:

```text
supported_material_claims
/
total_material_claims
```

subject to methodology.

---

# 175. Citation Quality

Citation quality SHALL consider:

```text
source relevance
source authority
directness
independence
freshness
```

not just presence.

---

# 176. Direct Evidence

Evidence directly establishing a claim SHOULD generally receive greater evidentiary weight than distant inference.

---

# 177. Evidence Distance

Pulse MAY measure derivation distance:

```text
Source
→ Observation
→ Derived Observation
→ Analysis
→ Claim
```

Longer chains may require additional scrutiny.

---

# 178. Methodological Transparency

Every consequential analysis SHALL identify its methodology.

---

# 179. Method Quality

Method quality MAY consider:

```text
validation
assumptions
sample size
sensitivity
historical performance
peer/expert review
fitness for purpose
```

---

# 180. MethodologyLibrary

The `MethodologyLibrary` introduced in `ADR-PULSE-003` SHALL integrate with quality assessment.

---

# 181. Method Status

Methodologies MAY have:

```text
EXPERIMENTAL
VALIDATED
APPROVED
DEPRECATED
RETIRED
```

---

# 182. Experimental Method

Experimental methods MAY be used for research.

Their outputs SHALL be appropriately labelled.

---

# 183. Sensitivity Analysis

Consequential quantitative analyses SHOULD support sensitivity analysis where assumptions materially influence conclusions.

---

# 184. Assumption

Material assumptions SHALL be explicit objects or structured records.

---

# 185. Assumption Confidence

Assumptions MAY themselves have confidence/uncertainty.

---

# 186. Assumption Register

ResearchMissions SHOULD maintain material assumptions.

---

# 187. Scenario Assumptions

Scenario assumptions SHALL not be presented as evidence.

---

# 188. Quality of Opportunity

Opportunity assessment SHOULD separate:

```text
evidence confidence
market attractiveness
strategic fit
execution feasibility
timing
expected value
```

---

# 189. Opportunity Evidence Profile

Conceptually:

```text
OpportunityEvidenceProfile
 ├── demand_evidence
 ├── supply_evidence
 ├── competition_evidence
 ├── pricing_evidence
 ├── regulatory_evidence
 ├── execution_evidence
 ├── corroboration
 ├── contradictions
 └── overall_confidence
```

---

# 190. Opportunity Qualification

An Opportunity SHALL NOT become `QUALIFIED` merely because an LLM finds the narrative compelling.

---

# 191. Opportunity Qualification Gate

Qualification SHOULD require a methodology-defined evidence profile.

---

# 192. Opportunity Disqualification

Pulse SHOULD also support evidence that invalidates an apparent opportunity.

---

# 193. Disconfirmation

Pulse SHALL actively seek disconfirming evidence for high-value opportunities.

---

# 194. Confirmation Bias Control

Research workflows SHOULD ask:

> What evidence would show that this opportunity is not real?

---

# 195. Red-Team Analysis

High-value ResearchMissions MAY include a structured challenge stage.

---

# 196. Challenge Record

Conceptually:

```text
Challenge
 ├── target_claim
 ├── counter_hypothesis
 ├── contrary_evidence
 ├── result
 └── reviewer
```

---

# 197. Competing Hypotheses

Pulse SHOULD support multiple explanations where evidence does not discriminate sufficiently.

---

# 198. Example

Coffee imports may rise because of:

```text
demand growth
inventory rebuilding
temporary supply disruption
re-export
currency movement
statistical revision
```

Pulse SHALL not choose one merely because it sounds commercially attractive.

---

# 199. Hypothesis Ranking

Competing hypotheses MAY be ranked according to evidence.

---

# 200. Unknown Cause

`CAUSE_UNKNOWN` SHALL remain valid.

---

# 201. Quality Feedback

Downstream outcomes SHALL feed quality learning.

---

# 202. Recommendation Outcome

If recommendations repeatedly fail despite high confidence, Pulse SHOULD investigate:

```text
methodology calibration
source reliability
assumption quality
execution confounders
```

---

# 203. Confidence Calibration

Where sufficient historical outcomes exist, Pulse SHOULD measure whether confidence levels are calibrated.

---

# 204. Example

If `VERY_HIGH` confidence predictions succeed only half the time in a domain where success is measurable, the confidence methodology requires revision.

---

# 205. Qualitative Calibration

Even qualitative confidence categories SHOULD eventually have empirical behavioural meaning where possible.

---

# 206. Calibration Dataset

Historical:

```text
forecast
signal
opportunity
risk
recommendation
outcome
```

records MAY form calibration datasets.

---

# 207. Model Evaluation

Model evaluation SHALL remain distinct from source-quality assessment.

---

# 208. Human Analyst Quality

Human judgement SHALL also be subject to learning and review.

---

# 209. No Untouchable Analyst

Analyst-authored conclusions SHALL not automatically override contradictory evidence merely because a senior analyst wrote them.

---

# 210. Expert Override

Experts MAY override automated assessments where authorised.

The override SHALL record:

```text
who
what
why
when
evidence
```

---

# 211. Override History

Historical overrides SHALL remain auditable.

---

# 212. Review Quality

Premium research SHOULD support peer review or equivalent independent review.

---

# 213. Reviewer Independence

Where practical, reviewers SHOULD not simply reproduce the original analyst's reasoning.

---

# 214. Research Quality Scorecard

A ResearchMission MAY expose a structured scorecard such as:

```text
Evidence Coverage        HIGH
Source Diversity         HIGH
Source Independence      MODERATE
Freshness                HIGH
Entity Resolution        HIGH
Contradictions           2 OPEN
Method Quality           HIGH
Evidence Debt            LOW
Overall Confidence       MODERATE
```

---

# 215. Overall Assessment

An overall assessment MAY be provided for usability.

It SHALL remain explainable through underlying dimensions.

---

# 216. Traffic-Light Presentation

User interfaces MAY simplify quality as:

```text
GREEN
AMBER
RED
```

but the underlying multidimensional assessment SHALL remain available.

---

# 217. Executive Simplicity, Analytical Depth

Pulse SHALL permit:

```text
simple executive presentation
```

without sacrificing:

```text
deep analytical traceability.
```

---

# 218. Quality API

Pulse's APIs SHOULD permit consumers to retrieve:

```text
quality profile
confidence
limitations
evidence gaps
contradictions
validation issues
```

for consequential intelligence.

Exact API design is deferred to the API ADR.

---

# 219. Quality Events

Potential canonical events include:

```text
pulse.quality.issue.detected
pulse.quality.issue.resolved
pulse.evidence.gap.detected
pulse.evidence.contradiction.detected
pulse.confidence.changed
pulse.source.quality.changed
pulse.intelligence.reassessment.required
```

Schemas belong in `nabhold/shared`.

---

# 220. Reassessment

A material quality change MAY trigger downstream reassessment.

---

# 221. Example

If a source later announces:

```text
previous data release was erroneous
```

Pulse SHOULD identify affected:

```text
Observations
EvidenceSets
Analyses
Claims
Insights
Opportunities
Risks
Recommendations
Reports
```

through provenance lineage.

---

# 222. Quality Impact Graph

Conceptually:

```text
SOURCE QUALITY EVENT
        ↓
DATASET / OBSERVATION
        ↓
EVIDENCE GRAPH
        ↓
AFFECTED ANALYSIS
        ↓
AFFECTED CLAIMS
        ↓
MATERIALITY TEST
        ↓
REASSESS / WARN / REPUBLISH
```

---

# 223. Quality Incident

Severe failures SHALL support a `QualityIncident`.

---

# 224. Quality Incident Examples

```text
wrong currency conversion
entity false merge
major source corruption
incorrect tariff mapping
systematic parser error
fabricated AI citation
cross-tenant evidence leakage
```

---

# 225. Incident Severity

Critical quality incidents MAY require:

```text
product withdrawal
client notification
reprocessing
report correction
mapping correction
root-cause analysis
```

---

# 226. Quality Incident versus Security Incident

Some incidents may be both.

The appropriate security process SHALL apply independently.

---

# 227. Correction Policy

Pulse SHALL distinguish:

```text
MINOR_CORRECTION
MATERIAL_CORRECTION
RETRACTION
SUPERSESSION
```

for published intelligence.

---

# 228. Material Correction

A correction that changes a material conclusion SHALL trigger stronger notification than typographical correction.

---

# 229. Retraction

Pulse SHALL support retracting intelligence that no longer meets integrity requirements.

---

# 230. Retraction Does Not Erase History

The historical publication SHALL remain auditable where legally permissible, but clearly marked retracted.

---

# 231. Commercial Trust

Nabhold SHALL treat correction transparency as part of the Pulse product promise rather than a reputational failure to hide.

---

# 232. Source Diversity

Research SHOULD avoid unnecessary dependence on one provider.

---

# 233. Source Concentration

Pulse MAY calculate source concentration for critical evidence domains.

---

# 234. Provider Concentration Risk

A report whose key conclusions all depend on one commercial provider SHALL disclose that dependency where material.

---

# 235. Geographic Bias

Source portfolios SHOULD be assessed for geographic bias.

---

# 236. Language Bias

Research SHOULD recognise that English-language sources may underrepresent developments reported in:

```text
French
Arabic
Portuguese
Swahili
local African languages
other relevant languages
```

---

# 237. Digital Visibility Bias

Entities with strong web presence may appear more important simply because they generate more accessible evidence.

Pulse SHALL guard against equating digital visibility with economic importance.

---

# 238. Formality Bias

Formal-sector datasets may underrepresent informal economies.

---

# 239. Urban Bias

Data availability may be disproportionately strong for cities.

---

# 240. Survivorship Bias

Historical datasets may overrepresent organisations that survived long enough to remain visible.

---

# 241. Selection Bias

Research methodologies SHALL identify material selection biases where known.

---

# 242. Publication Bias

News and research sources may disproportionately report unusual or negative events.

---

# 243. Quality Limitation

Bias SHALL be represented as a limitation rather than silently ignored.

---

# 244. African Market Intelligence

Pulse SHALL NOT interpret limited data availability in African markets as absence of economic activity.

---

# 245. Sparse Evidence

Sparse evidence SHALL result in:

```text
lower confidence
broader uncertainty
additional research
alternative evidence
```

rather than invented precision.

---

# 246. Alternative Evidence

Where formal data is sparse, Pulse MAY responsibly combine:

```text
trade proxies
satellite/geospatial evidence
company disclosures
procurement
market prices
logistics activity
news
industry sources
tenant evidence
```

provided provenance and inference remain explicit.

---

# 247. Proxy Evidence

Proxy evidence SHALL be labelled as such.

---

# 248. Proxy Method

Every material proxy SHALL identify the relationship it assumes between proxy and target phenomenon.

---

# 249. Triangulation

Triangulation SHALL be a first-class research method.

---

# 250. Triangulation Is Not Averaging

Triangulation means reasoning across different evidence forms, not simply averaging numbers.

---

# 251. Example — Market Growth

Pulse may triangulate:

```text
import growth
+
new company registrations
+
retail price behaviour
+
warehouse expansion
+
procurement
+
news
```

to assess whether a market appears to be expanding.

---

# 252. Triangulation Result

The conclusion SHALL explain how the evidence collectively supports it.

---

# 253. Intelligence Under Scarcity

Pulse's advantage SHALL not depend upon every market having perfect data.

Instead:

```text
PERFECT DATA
is desirable

but

DISCIPLINED REASONING FROM IMPERFECT EVIDENCE
is essential.
```

---

# 254. Commercial Research Quality Tiers

Nabhold MAY define product assurance levels.

Conceptually:

```text
PULSE-Q1 — Exploratory
PULSE-Q2 — Analytical
PULSE-Q3 — Verified
PULSE-Q4 — Decision Grade
```

Names are nonbinding.

---

# 255. Exploratory

Suitable for:

```text
discovery
early hypotheses
weak signals
```

with substantial uncertainty allowed.

---

# 256. Analytical

Suitable for:

```text
structured market understanding
comparison
opportunity screening
```

with stronger evidence requirements.

---

# 257. Verified

Requires substantial:

```text
source validation
entity verification
corroboration
methodological review
```

---

# 258. Decision Grade

Reserved for high-consequence recommendations with the strongest applicable:

```text
evidence
review
traceability
confidence
limitations
```

---

# 259. Assurance Is Not Guarantee

No quality tier SHALL promise certainty or business success.

---

# 260. Research Certificate

A published premium product MAY include a machine-readable `ResearchAssuranceManifest`.

---

# 261. ResearchAssuranceManifest

Conceptually:

```text
ResearchAssuranceManifest
 ├── product_id
 ├── research_snapshot_id
 ├── evidence_cutoff
 ├── assurance_level
 ├── evidence_coverage
 ├── source_profile
 ├── unresolved_contradictions
 ├── evidence_debt
 ├── methodology_versions
 ├── reviewer_status
 ├── limitations
 ├── overall_confidence
 └── generated_at
```

---

# 262. Commercial Defensibility

This manifest could allow a paying client to distinguish a Pulse research product from an uncited AI-generated market report.

---

# 263. Quality Observatory

Pulse SHOULD eventually maintain an internal **Quality Observatory**.

---

# 264. Quality Observatory Purpose

It would continuously answer:

```text
Which sources are deteriorating?
Which datasets are becoming stale?
Which mappings create most errors?
Which methods are poorly calibrated?
Which reports carry unresolved evidence debt?
Which confidence assessments were overconfident?
Which markets have weak evidence coverage?
```

---

# 265. Evidence Scarcity Map

Pulse MAY maintain a geographic/domain map of evidence availability.

---

# 266. Evidence Scarcity as Opportunity

A market with poor information infrastructure may itself represent a commercial research opportunity.

---

# 267. Intelligence Gap

Pulse MAY identify:

```text
high commercial interest
+
low reliable information availability
=
INTELLIGENCE GAP
```

---

# 268. Intelligence Gap Product Strategy

Nabhold may deliberately invest research resources where intelligence gaps are both:

```text
economically important
and
poorly served.
```

---

# 269. Research Moat

Over time, Pulse's quality architecture creates proprietary knowledge about:

```text
which sources are trustworthy
for which questions
in which markets
at which times
with which limitations.
```

That knowledge is itself valuable.

---

# 270. Trust Graph

Pulse MAY eventually construct a logical Trust Graph:

```text
SOURCE
   ↓
DATASET
   ↓
OBSERVATION
   ↓
CLAIM
   ↓
OUTCOME
```

and learn how historical evidence quality related to actual outcomes.

No graph database is required by this decision.

---

# 271. Source Reputation Learning

Pulse MAY update source assessments from accumulated performance.

Such learning SHALL not override source-specific context.

---

# 272. Method Reputation Learning

Likewise, Pulse MAY learn which methodologies perform well in particular domains.

---

# 273. Analyst Learning

Pulse MAY identify patterns of:

```text
overconfidence
underconfidence
systematic bias
strong domain expertise
```

at an aggregate quality-improvement level, subject to appropriate governance.

---

# 274. Intelligence Confidence versus Business Decision

Even `VERY_HIGH` intelligence confidence SHALL NOT mean:

```text
business should automatically act.
```

Decision authority remains governed by `ADR-PULSE-001`.

---

# 275. Unknown Unknowns

Pulse cannot quantify every uncertainty.

Research products SHOULD therefore permit limitations such as:

```text
material factors may exist for which reliable evidence was unavailable.
```

---

# 276. No False Completeness

A large EvidenceSet SHALL not imply that the research question has been exhaustively answered.

---

# 277. Quality Budget

Research missions MAY balance:

```text
time
cost
source fees
analyst effort
required assurance
```

against decision materiality.

---

# 278. Research Stop Rule

Pulse SHOULD support methodology-defined criteria for deciding when further research is unlikely to materially change the conclusion.

---

# 279. Marginal Evidence Value

Conceptually:

```text
Value of additional research
=
expected reduction in decision uncertainty
-
research cost
```

This MAY eventually inform research orchestration.

---

# 280. Active Evidence Acquisition

Pulse may therefore evolve from:

```text
collect everything
```

toward:

```text
acquire the next piece of evidence
most likely to resolve the important uncertainty.
```

---

# 281. Research Intelligence

This creates a second-order intelligence capability:

> Pulse does not merely analyse evidence; it can learn **which evidence it should seek next**.

---

# 282. Quality Service

Pulse SHALL expose a logical:

```text
QualityService
```

responsible for orchestration of quality evaluation.

---

# 283. Confidence Service

Pulse SHALL separately expose a logical:

```text
ConfidenceService
```

responsible for confidence assessment.

---

# 284. Separation

`QualityService` answers:

> What is the quality of this evidence?

`ConfidenceService` answers:

> Given this evidence and methodology, how strongly is this conclusion justified?

These SHALL not be conflated.

---

# 285. Validation Service

Validation MAY be implemented as a distinct logical service or capability beneath quality evaluation.

---

# 286. Physical Architecture

This ADR does not prescribe:

```text
specific PostgreSQL tables
specific Python classes
specific scoring libraries
specific ML models
specific workflow engines
```

Those belong to implementation specifications and later physical ADRs.

---

# 287. Rejected Alternative — One Universal Quality Score

Rejected.

It hides materially different dimensions.

---

# 288. Rejected Alternative — Official Source Means True

Rejected.

Authority and empirical accuracy differ.

---

# 289. Rejected Alternative — More Citations Means More Confidence

Rejected.

Sources may be dependent or repetitive.

---

# 290. Rejected Alternative — Discard Contradictions

Rejected.

Contradictions may reveal important phenomena.

---

# 291. Rejected Alternative — Fill Missing Data Automatically

Rejected.

Imputation must remain explicit.

---

# 292. Rejected Alternative — Remove All Outliers

Rejected.

Outliers may be the signal Pulse is intended to discover.

---

# 293. Rejected Alternative — LLM Confidence

Rejected.

Model self-confidence is not evidentiary confidence.

---

# 294. Rejected Alternative — Confidence Percentage Everywhere

Rejected.

False numerical precision undermines trust.

---

# 295. Rejected Alternative — Publish Only When Certain

Rejected.

Useful intelligence often exists under uncertainty.

Pulse SHALL communicate uncertainty rather than demand impossible certainty.

---

# 296. Rejected Alternative — Publish Everything with Disclaimer

Rejected.

Quality gates remain necessary.

---

# 297. Rejected Alternative — Treat Sparse African Data as Unusable

Rejected.

Pulse SHALL support disciplined triangulation, proxy evidence and explicit uncertainty.

---

# 298. Governing Invariants

**QUAL-PULSE-001**  
Quality SHALL be multidimensional.

**QUAL-PULSE-002**  
Authority SHALL remain distinct from accuracy.

**QUAL-PULSE-003**  
Source quality SHALL remain distinct from Observation quality.

**QUAL-PULSE-004**  
Evidence quality SHALL remain distinct from intelligence confidence.

**QUAL-PULSE-005**  
Confidence SHALL be claim- or object-specific.

**QUAL-PULSE-006**  
Arbitrary confidence percentages SHALL be prohibited.

**QUAL-PULSE-007**  
Probability SHALL remain distinct from confidence.

**QUAL-PULSE-008**  
Missing SHALL never silently become zero.

**QUAL-PULSE-009**  
Imputed values SHALL remain distinguishable from observed values.

**QUAL-PULSE-010**  
Outliers SHALL not be discarded solely because they are unusual.

**QUAL-PULSE-011**  
Duplicate evidence SHALL not count as independent corroboration.

**QUAL-PULSE-012**  
Source dependency SHALL be considered when assessing corroboration.

**QUAL-PULSE-013**  
Material contradictions SHALL be preserved.

**QUAL-PULSE-014**  
Contradictions SHALL not be silently averaged away.

**QUAL-PULSE-015**  
Quality transformations SHALL preserve provenance.

**QUAL-PULSE-016**  
Quality rules SHALL be versioned.

**QUAL-PULSE-017**  
Consequential confidence assessments SHALL identify methodology.

**QUAL-PULSE-018**  
Material EvidenceGaps SHALL remain explicit.

**QUAL-PULSE-019**  
Accepted EvidenceDebt SHALL remain visible.

**QUAL-PULSE-020**  
Critical unresolved evidence weaknesses MAY block publication.

**QUAL-PULSE-021**  
LLM output SHALL not establish confidence merely through persuasive language.

**QUAL-PULSE-022**  
Citation presence SHALL not substitute for citation support.

**QUAL-PULSE-023**  
Material factual claims SHALL be evidence-backed.

**QUAL-PULSE-024**  
Opportunity qualification SHALL require methodology-defined evidence.

**QUAL-PULSE-025**  
High-impact analysis SHOULD seek disconfirming evidence.

**QUAL-PULSE-026**  
Historical quality/confidence states SHALL remain reconstructable.

**QUAL-PULSE-027**  
Material source-quality changes SHALL support downstream impact analysis.

**QUAL-PULSE-028**  
Sparse evidence SHALL produce uncertainty, not fabricated precision.

**QUAL-PULSE-029**  
Tenant-private evidence SHALL remain protected during quality evaluation.

**QUAL-PULSE-030**  
Quality semantics SHALL remain independent of a specific database, model or AI provider.

---

# 299. Consequences

## Positive

This architecture allows Pulse to produce intelligence that remains useful even when evidence is:

```text
incomplete
contradictory
delayed
revised
biased
sparse
estimated
uneven across markets
```

without pretending those weaknesses do not exist.

It establishes a foundation for:

```text
trustworthy research
opportunity qualification
risk assessment
forecast calibration
source reputation
method evaluation
publication assurance
research quality tiers
continuous reassessment
```

## Costs

The architecture introduces substantial requirements for:

```text
quality rules
validation
scorecards
confidence methodologies
contradiction management
evidence gaps
review workflows
calibration
quality monitoring
```

But these are essential if Pulse is intended to produce intelligence people will pay for and use in consequential decisions.

---

# 300. Strategic Consequence — Pulse Can Compete on Trust

Generative AI makes producing a polished 30-page market report increasingly inexpensive.

That means:

```text
report length
```

and:

```text
professional-looking prose
```

will become progressively weaker differentiators.

Pulse SHALL instead compete on:

```text
EVIDENCE
+
TRACEABILITY
+
METHODOLOGY
+
QUALITY
+
UNCERTAINTY DISCLOSURE
+
CONTINUOUS REASSESSMENT
```

---

# 301. Strategic Consequence — "I Don't Know" Becomes a Feature

Pulse SHALL be capable of returning:

```text
INSUFFICIENT EVIDENCE
```

rather than inventing an answer.

For a commercial intelligence platform, this is not failure.

It is part of the trust contract.

---

# 302. Strategic Consequence — Imperfect Data Can Still Produce Valuable Intelligence

The system SHALL not require every market to possess Bloomberg-like data infrastructure.

Instead:

```text
fragmented evidence
      ↓
provenance
      ↓
quality assessment
      ↓
triangulation
      ↓
contradiction analysis
      ↓
explicit uncertainty
      ↓
defensible intelligence
```

This capability is particularly important in markets where valuable commercial opportunities coexist with fragmented information infrastructure.

---

# 303. Strategic Consequence — Pulse Can Discover Information Arbitrage

A particularly interesting condition is:

```text
HIGH ECONOMIC SIGNIFICANCE
          +
LOW INFORMATION QUALITY
          +
FRAGMENTED SOURCES
          +
LOW ANALYST COVERAGE
          =
POTENTIAL INTELLIGENCE ARBITRAGE
```

Pulse can eventually search not merely for commercial opportunities, but for **markets where better information itself has unusually high value**.

That may guide Nabhold toward research areas where a high-quality Pulse product has limited competition.

---

# 304. Strategic Consequence — Confidence Can Become Dynamic

Instead of publishing:

```text
Opportunity X — High Confidence
```

and forgetting it, Pulse can maintain:

```text
JAN   LOW
FEB   LOW
MAR   MODERATE
APR   MODERATE
MAY   HIGH
JUN   VERY HIGH
```

as new evidence arrives.

Clients could therefore subscribe not merely to an opportunity, but to its **evidence maturity**.

---

# 305. Strategic Consequence — Pulse Can Search for the Missing Evidence

A mature Pulse should eventually ask:

```text
What uncertainty currently matters most?

What evidence would reduce it?

Where could that evidence be obtained?

What would obtaining it cost?

Would resolving the uncertainty materially change the decision?
```

This turns research from passive information accumulation into **active evidence acquisition**.

---

# 306. Strategic Consequence — Research Assurance Can Become Part of the Product

A premium Pulse report could eventually be accompanied by an assurance summary:

```text
Research Assurance: PULSE-Q4

Material claims supported:        98%
Primary-source coverage:          High
Independent corroboration:        High
Entity-resolution confidence:     High
Evidence freshness:               High
Open contradictions:              2
Material evidence debt:           None
Methodology review:               Complete
Analyst review:                   Complete
Evidence cutoff:                  2026-09-04
```

The exact metrics require later methodological validation.

But the architectural principle is important:

> Nabhold should be capable of showing a client not merely **what Pulse concluded**, but **how well the conclusion has earned the client's confidence**.

---

# 307. Strategic Consequence — Quality Knowledge Compounds

After years of operation, Pulse may know something that is difficult for a new competitor to reproduce:

```text
which source tends to revise which indicator
how long each authority normally takes to publish
which datasets systematically miss certain markets
which providers are independent
which proxies work in which countries
which early signals proved useful
which methodologies were overconfident
which combinations of evidence predicted real outcomes
```

That accumulated knowledge becomes part of the Baobab intelligence moat.

---

# 308. Final Decision Statement

Baobab Pulse SHALL implement **data quality, evidence reliability and intelligence confidence as first-class domain capabilities rather than post-processing metadata**.

The governing conceptual architecture SHALL be:

```text
                        SOURCE
                           │
                    source quality
                           ▼
                        DATASET
                           │
                  coverage / method
                           ▼
                      ACQUISITION
                           │
                 completeness / integrity
                           ▼
                     OBSERVATION
                           │
              validation / precision / time
                           ▼
                      EVIDENCE
                           │
          corroboration / contradiction / gaps
                           ▼
                       ANALYSIS
                           │
            methodology / assumptions / bias
                           ▼
                        CLAIM
                           │
                  justified confidence
                           ▼
             OPPORTUNITY / RISK / FORECAST
                           │
                 decision fitness
                           ▼
                   RECOMMENDATION
                           │
                    quality gates
                           ▼
               INTELLIGENCE PRODUCT
                           │
                           ▼
                        OUTCOME
                           │
                           └──────────────┐
                                          ▼
                              CALIBRATION & LEARNING
```

Pulse SHALL therefore be able to say:

```text
WHAT WE OBSERVED

HOW RELIABLE THE EVIDENCE IS

WHAT THE SOURCES DISAGREE ABOUT

WHAT INFORMATION IS MISSING

WHAT WE INFER FROM THE EVIDENCE

HOW STRONGLY THAT INFERENCE IS JUSTIFIED

WHAT COULD DISPROVE IT

WHAT DECISION IT MAY SUPPORT

AND WHAT WE SHOULD LEARN FROM THE OUTCOME
```

The purpose is not to manufacture certainty.

The purpose is to make uncertainty **visible, structured, measurable where defensible, challengeable and useful for decision-making**.

That is the standard required for Baobab Pulse to evolve from an analytical engine into a credible commercial intelligence institution.