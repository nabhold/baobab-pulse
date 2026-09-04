# ADR-PULSE-007 — Temporal, Bitemporal and Data-Vintage Semantics

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-007`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:** `ADR-PULSE-001` through `ADR-PULSE-006`  
**Decision Type:** Temporal Semantics, Historical Reconstruction and Research Reproducibility Architecture Decision

---

# 1. Context

Almost every form of intelligence processed by Baobab Pulse has more than one meaningful time dimension.

Consider:

```text
Uganda exported coffee worth X in March 2026.
```

Possible temporal questions include:

```text
When did the trade occur?

Which reporting period does X describe?

When did the statistical authority publish X?

When did Pulse acquire X?

When did Pulse process X?

Was X later revised?

When did Pulse learn about the revision?

Which value was available when a report was written?

Which value is currently considered authoritative?
```

These are different questions.

Similarly:

```text
A regulation is announced in January,
published in February,
adopted in March,
and effective from July.
```

A single timestamp cannot describe this correctly.

Weather introduces another distinction:

```text
forecast issued Monday
for rainfall on Friday

versus

rainfall actually measured Friday
```

Macroeconomic data may be revised months or years after initial publication.

Company registry status changes.

FX rates vary continuously.

Commodity contracts have observation times and delivery periods.

News may report an event days after it occurred.

Trade statistics may be released months after the reporting period.

Pulse must preserve these distinctions if its intelligence is to remain historically defensible.

---

# 2. Decision

Baobab Pulse SHALL implement an explicit **multi-temporal intelligence model**.

The canonical temporal vocabulary SHALL distinguish at minimum:

```text
valid_time
observed_time
reporting_period
event_time
published_time
announced_time
effective_time
retrieved_time
processed_time
recorded_time
created_time
superseded_time
```

where applicable.

Pulse SHALL additionally implement **bitemporal semantics** for intelligence objects where both:

```text
when something was true
```

and:

```text
when Pulse knew or recorded it
```

are material.

Pulse SHALL implement explicit **data-vintage semantics** for revisable datasets and derived intelligence.

---

# 3. Fundamental Principle

> **Time is part of the meaning of evidence, not merely metadata about its storage.**

---

# 4. No Universal Timestamp

Pulse SHALL NOT use one generic field such as:

```text
timestamp
```

to represent every temporal concept.

---

# 5. Temporal Dimensions

The canonical model SHALL support distinct temporal dimensions.

## `valid_time`

When the fact, state or assertion applies in the represented world.

## `observed_time`

When a measurement or observation was physically or logically observed.

## `event_time`

When an event occurred.

## `reporting_period`

The period represented by a statistic.

## `published_time`

When the source published the information.

## `announced_time`

When an announcement was made.

## `effective_time`

When a rule, price, contract or state becomes operationally applicable.

## `retrieved_time`

When Pulse obtained the source information.

## `processed_time`

When Pulse processed it.

## `recorded_time`

When Pulse persisted its canonical representation.

## `created_time`

When the Pulse domain object itself was created.

## `superseded_time`

When a later version superseded it.

---

# 6. Temporal Context

Temporal semantics SHALL be represented through a canonical logical `TemporalContext`.

Conceptually:

```text
TemporalContext
 ├── valid_time
 ├── observed_time
 ├── event_time
 ├── reporting_period
 ├── published_time
 ├── announced_time
 ├── effective_time
 ├── retrieved_time
 ├── processed_time
 ├── recorded_time
 ├── created_time
 ├── superseded_time
 ├── timezone
 ├── precision
 └── calendar
```

Only applicable fields SHALL be populated.

---

# 7. Temporal Precision

Pulse SHALL preserve the precision actually supplied by the evidence.

Examples:

```text
2026
2026-Q3
2026-08
2026-08-14
2026-08-14T10:32
```

SHALL not be treated as equivalent.

---

# 8. No Invented Precision

If a source states:

```text
August 2026
```

Pulse SHALL NOT silently transform that into:

```text
2026-08-01T00:00:00
```

and imply that the source supplied day-level precision.

---

# 9. Temporal Precision Types

Canonical precision MAY include:

```text
YEAR
QUARTER
MONTH
WEEK
DAY
HOUR
MINUTE
SECOND
SUBSECOND
INTERVAL
UNKNOWN
```

---

# 10. Reporting Period

Statistical data SHALL use structured reporting periods.

Conceptually:

```text
ReportingPeriod
 ├── period_type
 ├── start
 ├── end
 ├── label
 ├── calendar
 └── precision
```

---

# 11. Half-Open Intervals

Where intervals are represented internally, Pulse SHOULD use half-open semantics:

```text
[start, end)
```

unless a source-specific domain requires otherwise.

This avoids ambiguity at adjacent boundaries.

---

# 12. Annual Data

An annual statistic SHOULD semantically represent:

```text
[2026-01-01, 2027-01-01)
```

without pretending that the original source supplied exact midnight timestamps.

---

# 13. Quarter Semantics

Quarter SHALL be represented explicitly.

```text
2026-Q2
```

is preferable to arbitrary date substitution.

---

# 14. Fiscal Periods

Pulse SHALL support fiscal periods that do not align with calendar years.

---

# 15. Source Calendar

Where relevant, Pulse SHALL preserve source calendar conventions.

---

# 16. Timezone

Timezone SHALL be explicit whenever interpretation depends upon local time.

---

# 17. UTC Normalisation

Machine timestamps MAY be normalised to UTC for storage and comparison.

Original timezone context SHALL remain recoverable where meaningful.

---

# 18. Local Market Time

Market-sensitive observations MAY require local-market time.

Example:

```text
Johannesburg close
London close
New York close
```

These SHALL not be treated merely as arbitrary UTC timestamps.

---

# 19. Event Time versus Processing Time

Pulse SHALL distinguish:

```text
event_time
```

from:

```text
processed_time
```

This is mandatory for event-driven ingestion.

---

# 20. Late-Arriving Evidence

An event may occur:

```text
Monday
```

but reach Pulse:

```text
Thursday.
```

Pulse SHALL preserve both.

---

# 21. Out-of-Order Arrival

Processing order SHALL not be assumed to equal real-world event order.

---

# 22. Late Data

Late-arriving observations SHALL be incorporated according to domain-specific temporal policies.

They SHALL not silently rewrite historical analytical outputs.

---

# 23. Backfill

Historical ingestion SHALL explicitly identify:

```text
BACKFILL
```

rather than pretending the evidence was acquired contemporaneously.

---

# 24. Acquisition Mode

Temporal processing SHALL recognise modes including:

```text
LIVE
BACKFILL
REPROCESS
CORRECTION
```

consistent with the parent architecture.

---

# 25. Published Time

`published_time` represents when the source made information available.

It SHALL not be inferred from:

```text
retrieved_time
```

unless explicitly marked as inferred.

---

# 26. Retrieved Time

`retrieved_time` represents when Pulse acquired the evidence.

It says nothing by itself about when the evidence became publicly available.

---

# 27. Knowledge Availability

Where decision reconstruction requires it, Pulse SHOULD model when evidence became reasonably available to Pulse or the relevant decision context.

---

# 28. Knowledge Time

Pulse SHALL therefore recognise the concept:

```text
knowledge_time
```

as the time from which the platform could legitimately use a piece of information within a particular analytical state.

---

# 29. Knowledge Time Is Not Always Retrieval Time

For example:

```text
Source published: 09:00
Pulse retrieved: 14:00
```

For a historical reconstruction of Pulse itself:

```text
knowledge_time = 14:00
```

may be appropriate.

For reconstruction of public market knowledge:

```text
published_time = 09:00
```

may be relevant.

The analytical context SHALL specify which perspective is intended.

---

# 30. Bitemporal Model

Where material, Pulse SHALL distinguish:

```text
VALID TIME
```

from:

```text
SYSTEM / KNOWLEDGE TIME
```

Conceptually:

```text
                SYSTEM KNOWLEDGE
                      TIME
                       →
             ┌────────────────────
             │
VALID        │
TIME         │
 ↓           │
             │
```

---

# 31. Valid Time

Valid time answers:

> When was this state true or applicable in the represented world?

---

# 32. System Time

System time answers:

> During which period did Pulse hold this representation as the recorded state?

---

# 33. Bitemporal Record

Conceptually:

```text
BitemporalRecord
 ├── valid_from
 ├── valid_to
 ├── system_from
 └── system_to
```

---

# 34. Current Record

A record is current only relative to a temporal dimension.

Pulse SHALL avoid ambiguous use of:

```text
current
```

---

# 35. Current in the World

`valid_to = infinity`

may indicate currently valid.

---

# 36. Current in Pulse

`system_to = infinity`

may indicate the current system representation.

These concepts SHALL remain distinct.

---

# 37. Example — Company Status

Suppose a company was dissolved on:

```text
2026-05-01
```

but Pulse learned this on:

```text
2026-05-20.
```

The temporal representation may conceptually be:

```text
status = DISSOLVED

valid_from  = 2026-05-01
system_from = 2026-05-20
```

Pulse can then answer both:

```text
Was the company legally dissolved on 10 May?
```

and:

```text
Did Pulse know it was dissolved on 10 May?
```

Those answers may differ.

---

# 38. Example — Regulatory Change

Suppose:

```text
announced:  1 March
published:  15 March
adopted:    10 April
effective:  1 July
```

Pulse SHALL preserve all four dates.

---

# 39. Regulation Validity

The regulation SHALL not be treated as operationally effective on its announcement date.

---

# 40. Regulatory Intelligence

Before effectiveness, Pulse MAY still produce:

```text
regulatory risk
preparation recommendation
scenario analysis
```

based on the proposed/adopted change.

The intelligence SHALL correctly represent the rule's lifecycle.

---

# 41. Example — Trade Statistics

Suppose 2025 trade statistics are:

```text
period represented:
2025

first publication:
February 2026

revision:
June 2026
```

Pulse SHALL preserve:

```text
reporting_period = 2025
published_time   = February 2026
vintage          = February 2026
```

for the original observation and the later revision separately.

---

# 42. Data Vintage

A `DataVintage` identifies a particular historical release state of a dataset.

---

# 43. Vintage Principle

> **A statistical value is not fully identified merely by indicator, geography and reporting period when the source can revise history.**

Its vintage matters.

---

# 44. Dataset Version versus Data Vintage

Pulse SHALL distinguish:

```text
DatasetVersion
```

from:

```text
DataVintage
```

A DatasetVersion concerns schema, methodology or provider-defined dataset versioning.

A DataVintage concerns the release state of the actual observations available at a point in time.

---

# 45. Example

```text
Dataset:
National Accounts

DatasetVersion:
Methodology 2025

DataVintage:
2026-03 release

DataVintage:
2026-06 revised release
```

---

# 46. Vintage Identity

A vintage SHOULD identify:

```text
dataset
release identifier
release time
acquisition
source version where available
```

---

# 47. Vintage Manifest

Pulse SHOULD maintain a manifest of observations belonging to a material data vintage.

---

# 48. Vintage Comparison

Pulse SHALL support comparison:

```text
Vintage A
vs
Vintage B
```

to identify revisions.

---

# 49. Revision Delta

For numeric observations:

```text
revision_delta =
new_value - previous_value
```

MAY be calculated.

---

# 50. Revision Percentage

Where meaningful:

```text
revision_percentage
```

MAY also be derived.

---

# 51. Revision Is Evidence

A revision is itself analytically meaningful.

Repeated revisions may reveal:

```text
measurement uncertainty
reporting weakness
methodological change
economic volatility
institutional capacity issues
```

depending upon context.

Pulse MAY analyse revision behaviour.

---

# 52. Original Release Preservation

Pulse SHALL preserve original releases where licensing permits.

---

# 53. Latest Vintage

The latest vintage SHALL not erase earlier vintages.

---

# 54. Research Vintage Pinning

Every reproducible ResearchSnapshot SHALL pin the data vintages it used.

---

# 55. Report Reproduction

Pulse SHALL therefore be able to answer:

> Which exact version of the trade statistics did this report use?

---

# 56. Historical Report Stability

A report issued in March SHALL not silently change because the underlying statistical authority revised the data in June.

---

# 57. Living Report Exception

A living IntelligenceProduct MAY deliberately update.

Such updates SHALL produce a new edition, snapshot or version.

---

# 58. Edition Semantics

Conceptually:

```text
Market Report
   ├── Edition 2026-03
   ├── Edition 2026-06
   └── Edition 2026-09
```

Each edition SHALL preserve its own evidence state.

---

# 59. Point-in-Time Reconstruction

Pulse SHALL support the conceptual query:

```text
AS_OF(system_time)
```

---

# 60. Valid-Time Query

Pulse SHALL support:

```text
VALID_AT(valid_time)
```

---

# 61. Combined Temporal Query

Where bitemporal data exists, Pulse SHOULD support the conceptual operation:

```text
KNOWN_AS_OF(system_time)
AND
VALID_AT(valid_time)
```

---

# 62. Example — Due Diligence

A client asks:

> Based only on information available on 31 December 2025, what would Pulse have concluded about Company X?

Pulse SHALL be architecturally capable of answering this without using evidence learned in 2026.

---

# 63. No Look-Ahead Bias

Historical analysis, model training and backtesting SHALL prevent **look-ahead bias**.

---

# 64. Look-Ahead Bias Definition

Look-ahead bias occurs when an analysis uses information that was not actually available at the historical decision point.

---

# 65. Example

A model evaluating a 2024 investment opportunity SHALL not use:

```text
a 2025 revision of 2024 GDP
```

unless the analytical experiment explicitly intends retrospective reconstruction using revised data.

---

# 66. Backtesting Modes

Pulse SHOULD distinguish:

```text
REAL_TIME_VINTAGE
LATEST_REVISED
HYBRID
```

backtesting modes.

---

# 67. Real-Time Vintage Backtest

Uses only information actually available at each historical decision time.

This is preferred for evaluating realistic decision performance.

---

# 68. Latest-Revised Backtest

Uses today's best historical data.

This may be useful for economic analysis but SHALL not be represented as a real-time historical simulation.

---

# 69. Hybrid Backtest

Combines specified vintage policies.

Its methodology SHALL be explicit.

---

# 70. Forecast Origin

Every Forecast SHALL have:

```text
forecast_origin
```

representing the time at which the forecast was made.

---

# 71. Forecast Horizon

Forecast SHALL identify its horizon.

Example:

```text
forecast_origin = 2026-09-01
target_period   = 2026-Q4
```

---

# 72. Forecast Evidence Cut-Off

A Forecast SHOULD record:

```text
evidence_cutoff
```

after which evidence was excluded.

---

# 73. Forecast Reproducibility

Forecast reproduction SHALL use evidence available at or before the cut-off according to the selected vintage policy.

---

# 74. Forecast Revision

A later forecast for the same target period SHALL be a new Forecast.

It SHALL not overwrite the earlier one.

---

# 75. Forecast Sequence

Pulse SHALL support:

```text
Q4 Forecast made in June
Q4 Forecast made in July
Q4 Forecast made in August
Q4 Forecast made in September
```

as distinct objects.

---

# 76. Forecast Evolution

Comparing these forecasts MAY itself provide useful intelligence.

---

# 77. Forecast Evaluation

Once actual evidence becomes available:

```text
Forecast
   ↓
Actual Observation
   ↓
ForecastEvaluation
```

---

# 78. Actual Vintage

Forecast evaluation SHALL state which actual-data vintage is used.

---

# 79. Re-evaluation

A ForecastEvaluation MAY be recalculated when actual historical data is revised.

The original evaluation SHOULD remain reconstructable.

---

# 80. Signal Time

A Signal SHALL distinguish:

```text
phenomenon_time
```

from:

```text
detection_time
```

where applicable.

---

# 81. Detection Lag

Pulse MAY calculate:

```text
detection_lag =
detection_time - phenomenon_time
```

---

# 82. Commercial Importance of Detection Lag

For opportunity intelligence:

```text
earlier detection
```

may materially increase commercial value.

Pulse SHOULD therefore measure detection lag for relevant signal families.

---

# 83. News Event Time

A NewsArticle SHALL preserve:

```text
publication_time
```

while an extracted Event MAY have:

```text
event_time
```

---

# 84. Example

```text
Factory fire:
Monday

News publication:
Tuesday

Pulse retrieval:
Tuesday afternoon
```

All three times are meaningful.

---

# 85. Regulatory Detection Lag

Pulse MAY measure:

```text
source publication
→ Pulse acquisition
→ analyst/client notification
```

for regulatory intelligence products.

---

# 86. Opportunity Discovery Time

Opportunity SHALL preserve:

```text
detected_at
```

and, where inferable:

```text
emergence_period
```

---

# 87. Opportunity Evolution

An Opportunity MAY evolve through:

```text
EMERGING
DEVELOPING
MATURE
DECLINING
CLOSED
```

subject to the Opportunity ADR.

Temporal history SHALL be preserved.

---

# 88. Opportunity Window

An Opportunity MAY define:

```text
window_start
window_end
```

where meaningful.

---

# 89. Opportunity Half-Life

Future methodology MAY estimate how rapidly the value of an opportunity decays after detection.

---

# 90. Risk Temporal Semantics

Risk SHALL distinguish:

```text
risk detected
risk expected
risk materialised
risk resolved
```

where applicable.

---

# 91. Risk Horizon

A Risk MAY be:

```text
IMMEDIATE
SHORT_TERM
MEDIUM_TERM
LONG_TERM
```

according to methodology.

---

# 92. Price Validity

Commercial prices may have validity windows.

Example:

```text
freight quote valid until Friday
```

Pulse SHALL preserve that expiry.

---

# 93. Stale Price

After validity expires, the observation remains historical evidence but SHALL not automatically qualify as a current actionable price.

---

# 94. FX Temporal Semantics

FX observations SHALL preserve precise observation/reference times appropriate to the rate.

---

# 95. FX Historical Conversion

Historical monetary values SHALL use temporally appropriate FX observations according to declared methodology.

---

# 96. FX Conversion Policies

Possible methodologies MAY include:

```text
TRANSACTION_TIME
DAILY_CLOSE
DAILY_REFERENCE
MONTHLY_AVERAGE
PERIOD_AVERAGE
PERIOD_END
```

---

# 97. Conversion Method Required

Pulse SHALL not silently choose among these methods for consequential analysis.

---

# 98. Commodity Temporal Semantics

Commodity evidence may distinguish:

```text
observation time
trade date
settlement date
contract delivery period
```

where relevant.

---

# 99. Contract Time

A December futures contract observed in September SHALL preserve both:

```text
observed in September
delivery in December
```

---

# 100. Weather Temporal Semantics

Measured weather SHALL distinguish observation period.

Forecast weather SHALL distinguish:

```text
forecast origin
target time
horizon
```

---

# 101. Climate Temporal Semantics

Climate projections SHALL preserve:

```text
reference period
projection period
scenario
model run
```

---

# 102. Company Registry Temporal Semantics

Company registry facts may have:

```text
effective date
filing date
publication date
retrieval date
```

These SHALL not be conflated.

---

# 103. Ownership Temporal Semantics

Corporate ownership SHALL be temporally bounded where data permits.

---

# 104. Director Temporal Semantics

Officer/director relationships SHOULD support:

```text
valid_from
valid_to
```

where known.

---

# 105. Geospatial Temporal Semantics

Geospatial facts may change.

Examples:

```text
administrative boundary
road completion
port capacity
land use
facility status
```

Geospatial evidence SHALL support validity periods where necessary.

---

# 106. Market Membership Time

Country membership in:

```text
trade bloc
customs union
preferential scheme
```

SHALL be temporally modelled.

---

# 107. Tariff Temporal Semantics

Tariffs SHALL support:

```text
announced
published
effective_from
effective_to
```

where available.

---

# 108. Preferential Agreement Time

A trade agreement's signature date SHALL not automatically equal its effective date.

---

# 109. Internal Commerce Time

Medusa-derived observations may distinguish:

```text
order_created
order_completed
payment_authorised
payment_captured
fulfilment
return
refund
```

according to source contract.

---

# 110. Internal ERP Time

iDempiere-derived evidence may distinguish:

```text
document date
accounting date
due date
posting date
payment date
```

according to ERP semantics.

Pulse SHALL preserve relevant distinctions rather than collapse them.

---

# 111. Content Time

Payload-derived evidence may distinguish:

```text
created
scheduled
published
unpublished
revised
```

where relevant.

---

# 112. Event-Time Windows

Streaming or near-real-time analysis SHOULD use event-time windows where domain correctness depends upon actual occurrence time.

---

# 113. Processing-Time Windows

Processing-time windows MAY be used for operational monitoring.

They SHALL not substitute for event-time analysis where event order matters.

---

# 114. Watermark Concept

For delayed event streams, Pulse MAY adopt watermark semantics to determine when a time window is sufficiently complete for analysis.

---

# 115. Watermark Is Policy

Watermark thresholds SHALL be domain and source specific.

---

# 116. Example

A market-price feed might tolerate:

```text
minutes
```

of lateness.

Trade statistics may tolerate:

```text
weeks or months.
```

---

# 117. Window Revision

A completed analytical window MAY later receive late evidence.

Pulse SHALL define whether to:

```text
IGNORE
AMEND
RECOMPUTE
CREATE_REVISION
```

according to product policy.

---

# 118. Default Revision Policy

For consequential intelligence, Pulse SHOULD create a revision rather than silently mutate previously published results.

---

# 119. Temporal Aggregation

Aggregation SHALL respect metric temporal semantics.

---

# 120. Flow Metric

Flows MAY be aggregated across compatible non-overlapping periods.

---

# 121. Stock Metric

Stocks require appropriate point-in-time or period-end treatment.

---

# 122. Rate Metric

Rates require explicit aggregation methodology.

---

# 123. Temporal Alignment

Cross-domain analysis SHALL align evidence periods deliberately.

---

# 124. Example

Comparing:

```text
annual trade
```

with:

```text
daily FX
```

requires an explicit temporal transformation.

---

# 125. Alignment Methods

Possible policies:

```text
PERIOD_AVERAGE
PERIOD_END
PERIOD_START
NEAREST
INTERPOLATE
ASOF
CUSTOM
```

---

# 126. Temporal Join

Pulse SHOULD provide governed temporal join semantics.

---

# 127. As-Of Join

An `ASOF` join selects the latest eligible observation available before or at a specified time according to policy.

---

# 128. Look-Ahead Protection

Temporal joins used for historical modelling SHALL enforce evidence availability constraints.

---

# 129. Interpolation

Interpolated values SHALL become derived observations.

They SHALL retain the interpolation method and source observations.

---

# 130. Extrapolation

Extrapolated values SHALL be even more explicitly marked.

---

# 131. Time Series Identity

A TimeSeries SHALL be defined by more than metric.

Conceptually:

```text
metric
+
subject
+
dimensions
+
methodology
+
unit
+
source/profile
```

---

# 132. Time Series Observation

Individual points remain canonical Observations.

The TimeSeries is a logical grouping or analytical projection.

---

# 133. Irregular Time Series

Pulse SHALL support irregularly spaced observations.

---

# 134. Missing Period

A missing period SHALL remain missing.

Pulse SHALL not infer zero.

---

# 135. Temporal Gap

Pulse MAY explicitly identify gaps.

---

# 136. Staleness

Every relevant evidence class SHOULD define a freshness or staleness policy.

---

# 137. Staleness Is Contextual

A one-day-old FX observation may be stale.

A one-year-old census statistic may still be the latest authoritative value.

---

# 138. Freshness Policy

Conceptually:

```text
FreshnessPolicy
 ├── domain
 ├── metric
 ├── source
 ├── expected_frequency
 ├── warning_after
 ├── stale_after
 ├── invalid_after
 └── action
```

---

# 139. Freshness States

Possible states:

```text
FRESH
AGING
STALE
EXPIRED
UNKNOWN
```

---

# 140. Freshness Evaluation Time

Freshness SHALL be evaluated relative to an explicit reference time.

---

# 141. Freshness Propagation

Derived intelligence SHOULD account for the freshness of material upstream evidence.

---

# 142. No Blind Freshness Minimum

A Recommendation does not necessarily become stale merely because one contextual source becomes stale.

Materiality SHALL matter.

---

# 143. Temporal Confidence

Confidence MAY decrease as evidence ages where methodology justifies it.

This SHALL be explicit.

---

# 144. Intelligence Validity

Material intelligence objects MAY define:

```text
valid_from
valid_until
```

---

# 145. Recommendation Validity

A Recommendation SHOULD declare an expiry or review date where its assumptions are time-sensitive.

---

# 146. Report Validity

A report MAY declare:

```text
evidence_cutoff
published_at
review_after
```

---

# 147. Research Cut-Off

Every consequential ResearchSnapshot SHALL define:

```text
evidence_cutoff
```

---

# 148. Evidence After Cut-Off

Evidence obtained after the cut-off SHALL not silently enter the frozen snapshot.

---

# 149. Publication Delay

A report may be published after its evidence cut-off.

Both dates SHALL be visible internally.

---

# 150. Example

```text
evidence_cutoff:
2026-08-31

analysis_completed:
2026-09-02

published:
2026-09-05
```

This is valid.

---

# 151. Embargoed Evidence

Pulse MAY acquire evidence before its public release where legitimately authorised.

Embargo status SHALL be respected.

---

# 152. Embargo Time

Embargoed evidence SHALL record:

```text
available_to_pulse
public_release_time
```

where applicable.

---

# 153. No Historical Leakage

Backtests representing public knowledge SHALL not use embargoed evidence before its public availability.

---

# 154. Temporal Classification Changes

Classification itself may change over time.

Example:

```text
CONFIDENTIAL
→ PUBLIC
```

after official publication.

Such transitions SHALL be recorded rather than retroactively pretending the evidence was always public.

---

# 155. Temporal Licensing

Source licences may have effective and expiry periods.

---

# 156. Licence Expiry

Licence expiry SHALL not automatically erase historical lineage.

Use and redistribution rights SHALL be evaluated according to licence terms.

---

# 157. Retention Time

Retention policy is distinct from valid time.

---

# 158. Retention Expiry

Evidence may remain historically valid while becoming legally or contractually ineligible for continued storage.

The retention ADR SHALL govern deletion.

---

# 159. Model Temporal Semantics

ModelVersion SHALL have lifecycle times such as:

```text
created
validated
approved
activated
deprecated
retired
```

---

# 160. ModelRun Time

ModelRun SHALL preserve:

```text
started_at
completed_at
evidence_cutoff
model_version
dataset_vintages
```

---

# 161. Training Cut-Off

Predictive models SHALL record the latest evidence time included in training where relevant.

---

# 162. Training Vintage

Training datasets SHOULD be versioned/vintage-aware.

---

# 163. Temporal Leakage

Training or validation processes SHALL guard against using future evidence to predict the past.

---

# 164. Temporal Cross-Validation

Time-dependent predictive models SHOULD use temporally appropriate validation rather than random splitting where random splitting would introduce leakage.

---

# 165. Analyst Time

Human research actions MAY preserve:

```text
started_at
completed_at
reviewed_at
approved_at
```

where relevant.

---

# 166. Decision Time

Decision SHALL preserve:

```text
decision_time
```

and exact Recommendation version available at that time.

---

# 167. Execution Time

Operational execution SHALL remain distinct from decision time.

---

# 168. Outcome Time

Outcome SHALL preserve when the consequence occurred or was measured.

---

# 169. Outcome Observation Delay

Pulse SHALL distinguish:

```text
outcome occurred
```

from:

```text
outcome became measurable.
```

---

# 170. Decision Evaluation Window

Recommendation/decision evaluation MAY define:

```text
evaluation_start
evaluation_end
```

---

# 171. Premature Evaluation

Pulse SHALL not label a long-term recommendation unsuccessful merely because its intended evaluation window has not elapsed.

---

# 172. Opportunity Timing

Opportunity quality SHALL eventually consider:

```text
time to market
window duration
decision lead time
execution lead time
```

---

# 173. Temporal Feasibility

An opportunity that expires before the tenant could realistically act MAY be commercially irrelevant.

---

# 174. Opportunity Timing Score

Future opportunity methodologies MAY therefore include:

```text
timing_score
```

---

# 175. First Detection

Pulse SHALL preserve the first time it detected a material Signal or Opportunity.

---

# 176. Rediscovery

Repeated detection SHALL not erase first-detection history.

---

# 177. Lead-Time Measurement

Pulse MAY calculate:

```text
market recognition time
-
Pulse first detection time
```

as a measure of intelligence lead.

---

# 178. Intelligence Lead

If Pulse consistently detects developments before they become widely recognised, that lead may become an important performance metric.

---

# 179. Temporal Advantage

The commercial value of intelligence may therefore be considered as a function of:

```text
quality
×
relevance
×
confidence
×
timeliness
```

not accuracy alone.

---

# 180. Temporal Opportunity Decay

Certain opportunities decay rapidly.

Conceptually:

```text
Opportunity Value
      │\
      │ \
      │  \
      │   \
      │    \____
      └────────────── Time
```

---

# 181. Opportunity Decay Function

Future methodologies MAY estimate opportunity decay.

It SHALL be versioned and evidence-based.

---

# 182. Temporal Risk Escalation

Risks may behave oppositely:

```text
Risk
 │       /
 │      /
 │    _/
 │___/
 └──────────── Time
```

Pulse MAY model escalation trajectories.

---

# 183. Temporal Pattern Library

Pulse MAY eventually maintain reusable patterns such as:

```text
ACCELERATING
DECELERATING
CYCLICAL
SEASONAL
STRUCTURAL_BREAK
REGIME_CHANGE
TRANSIENT
```

---

# 184. Seasonality

Seasonal interpretation SHALL require sufficient temporal evidence.

---

# 185. Agricultural Seasonality

Agricultural analysis MAY require calendars such as:

```text
planting
flowering
harvest
export season
```

which do not necessarily align with calendar quarters.

---

# 186. Commercial Seasonality

Retail and commerce evidence may follow:

```text
holiday
school
tourism
tax
financial-year
```

cycles.

---

# 187. Multiple Calendars

Pulse SHALL allow analytical calendars to coexist.

---

# 188. Market Sessions

Financial/commodity markets MAY require trading-session calendars.

---

# 189. Business Days

Business-day calculations SHALL use applicable market/jurisdiction calendars where consequential.

---

# 190. Temporal Normalisation

Pulse MAY normalise temporal representations for computation.

It SHALL preserve source temporal meaning.

---

# 191. Temporal Provenance

Temporal transformations SHALL be recorded when they materially affect interpretation.

---

# 192. Example

Converting:

```text
monthly CPI
```

into:

```text
annual inflation rate
```

is an analytical transformation, not merely date formatting.

---

# 193. Temporal Method Registry

Reusable temporal transformations SHOULD identify method versions.

---

# 194. Temporal Compatibility

Before combining evidence, Pulse SHOULD assess temporal compatibility.

Possible states:

```text
ALIGNED
ALIGNABLE
PARTIALLY_ALIGNED
MISALIGNED
UNKNOWN
```

---

# 195. Temporal Misalignment Warning

Material misalignment SHOULD surface as an analytical limitation.

---

# 196. Temporal Coverage

EvidenceSet SHOULD be capable of describing its temporal coverage.

---

# 197. Coverage Gaps

Significant temporal gaps SHOULD be visible.

---

# 198. Publication Currency

An IntelligenceProduct SHOULD expose:

```text
data_current_through
```

or equivalent where useful.

---

# 199. Multiple Currency Dates

A product may contain:

```text
trade data current through June
FX current through yesterday
regulation current through today
```

Pulse SHALL support this rather than inventing one misleading universal "data date."

---

# 200. Domain Currency Manifest

A ResearchSnapshot SHOULD be able to expose freshness by evidence domain.

Example:

```text
TRADE       2026-06
MACRO       2026-Q2
FX          2026-09-04
NEWS        2026-09-04
REGULATION  2026-09-04
```

---

# 201. Temporal Impact Analysis

Changes to historical evidence SHALL integrate with the Evidence Graph defined by `ADR-PULSE-006`.

---

# 202. Revision Propagation

Conceptually:

```text
NEW DATA VINTAGE
       ↓
revision detected
       ↓
affected observations
       ↓
lineage traversal
       ↓
affected analyses
       ↓
affected claims
       ↓
materiality evaluation
```

---

# 203. Historical Recalculation

Pulse MAY recalculate historical analyses using new vintages.

The recalculated result SHALL be a new analytical version.

---

# 204. Original Analysis Preservation

The original analysis SHALL remain available for historical reconstruction.

---

# 205. "What We Knew Then"

Pulse SHALL support the conceptual research mode:

```text
WHAT_WE_KNEW_THEN
```

---

# 206. "What We Know Now"

Pulse SHALL also support:

```text
WHAT_WE_KNOW_NOW
```

---

# 207. Difference Analysis

The difference between those two states may itself be useful intelligence.

---

# 208. Example

```text
2025 initial estimate:
GDP growth = 4.2%

2026 revised estimate:
GDP growth = 3.1%
```

Pulse can ask:

```text
Would the 2025 recommendation still have been made
if today's revised evidence had been known?
```

---

# 209. Counterfactual Review

Such analysis SHALL be clearly labelled retrospective/counterfactual.

It SHALL not rewrite the historical decision context.

---

# 210. Temporal Research Modes

ResearchMission MAY declare:

```text
CURRENT
POINT_IN_TIME
REAL_TIME_HISTORICAL
RETROSPECTIVE_REVISED
FORECAST
SCENARIO
```

---

# 211. Current Mode

Uses the current eligible evidence state.

---

# 212. Point-in-Time Mode

Uses evidence according to a defined historical cut-off.

---

# 213. Real-Time Historical Mode

Uses only vintages actually available at the historical time.

---

# 214. Retrospective Revised Mode

Uses current revised historical evidence.

---

# 215. Forecast Mode

Uses evidence up to a declared forecast origin/cut-off.

---

# 216. Scenario Mode

May deliberately introduce future assumptions.

Scenario assumptions SHALL remain distinguishable from observations.

---

# 217. Temporal Query Contract

Pulse's application layer SHALL expose temporal query concepts explicitly.

It SHALL not force every caller to implement temporal logic manually.

---

# 218. Conceptual Query Parameters

These MAY include:

```text
valid_at
known_at
published_before
retrieved_before
reporting_period
vintage
latest_vintage
as_of
```

Exact API design belongs to the API ADR.

---

# 219. Default Query Semantics

Every query returning temporal evidence SHALL have documented default temporal semantics.

---

# 220. Dangerous Default

A generic:

```text
latest=true
```

without defining which temporal dimension is latest SHALL be prohibited for consequential interfaces.

---

# 221. Temporal Repository Semantics

Repositories handling bitemporal aggregates SHALL expose domain-aware temporal retrieval.

---

# 222. No ORM Leakage

ORM timestamp conventions SHALL not define Pulse temporal semantics.

---

# 223. Database Timestamp Fields

Database `created_at` and `updated_at` MAY exist operationally.

They SHALL not substitute for domain time.

---

# 224. Physical PostgreSQL Design

The exact use of:

```text
range types
exclusion constraints
partitioning
temporal indexes
```

belongs to the PostgreSQL physical architecture ADR.

---

# 225. Temporal Exclusion

Where domain rules prohibit overlapping valid states, physical constraints SHOULD enforce this where practical.

---

# 226. Example

A single exclusive legal status MAY not have two overlapping authoritative validity periods for the same source/entity/version context.

---

# 227. Overlap Can Be Legitimate

Multiple sources may legitimately assert different overlapping states.

Therefore constraints SHALL account for source and assertion identity.

---

# 228. Temporal Events

Material temporal transitions MAY produce events such as:

```text
pulse.observation.superseded
pulse.dataset.vintage.published
pulse.evidence.stale
pulse.recommendation.expired
pulse.opportunity.window.closing
pulse.research.reassessment.required
```

Canonical event contracts belong in `nabhold/shared`.

---

# 229. Scheduled Temporal Evaluation

Pulse scheduler SHALL support periodic evaluation of:

```text
freshness
expiry
effective dates
forecast targets
review dates
opportunity windows
```

---

# 230. Effective-Date Activation

A regulation already acquired but not yet effective MAY trigger a state transition when its effective date arrives.

---

# 231. Scheduled Reassessment

Recommendations MAY request reassessment at defined dates.

---

# 232. Time-Triggered Intelligence

Not every new Signal requires new external evidence.

Time itself may cause a meaningful transition.

Example:

```text
tariff becomes effective today
```

---

# 233. Deterministic Clock

Tests SHALL use an injectable/domain clock abstraction.

---

# 234. No Hidden Wall Clock

Domain logic SHALL not depend arbitrarily on direct wall-clock calls where deterministic testing is required.

---

# 235. Reproducible Time

Research jobs SHALL record their temporal reference context.

---

# 236. Temporal Test Cases

Testing SHALL cover:

```text
late arrival
revision
backfill
timezone conversion
DST where relevant
month/year boundaries
fiscal periods
overlapping intervals
future-effective rules
expired evidence
point-in-time reconstruction
```

---

# 237. Clock Skew

Distributed components MAY have minor clock differences.

Ordering SHALL not depend solely upon physical timestamp equality.

---

# 238. Event Ordering

Where strict ordering is required, Pulse SHOULD use appropriate sequence/version semantics in addition to timestamps.

---

# 239. Source Clock Reliability

External timestamps SHALL not automatically be trusted as perfectly accurate.

---

# 240. Estimated Time

Where an event time is estimated, Pulse SHALL record temporal uncertainty.

---

# 241. Temporal Uncertainty

Temporal context MAY include:

```text
EXACT
APPROXIMATE
INFERRED
RANGE
UNKNOWN
```

---

# 242. Inferred Date

An inferred date SHALL never be represented as exact without qualification.

---

# 243. Open-Ended Validity

Unknown end dates SHALL be modelled explicitly.

---

# 244. Infinity Semantics

Internal representations MAY use an unbounded upper interval rather than arbitrary dates such as:

```text
9999-12-31
```

where the persistence layer permits.

---

# 245. Future Data

Future-dated evidence SHALL be validated against domain semantics.

A future regulation may be valid evidence.

A future historical measurement is generally suspicious.

---

# 246. Temporal Anomaly Detection

Pulse MAY detect anomalies such as:

```text
published before event occurred
effective before adoption
retrieved before publication
forecast target before forecast origin
```

subject to legitimate domain exceptions.

---

# 247. Source Corrections

Temporal errors from sources SHALL remain source evidence.

Pulse MAY flag them rather than silently correcting them.

---

# 248. Corrected Canonical Interpretation

Where Pulse corrects a parser or mapping error, the correction SHALL preserve original source timestamps and create new system-time history.

---

# 249. Performance

Temporal history may significantly increase data volume.

Physical storage SHALL optimise without discarding required temporal semantics.

---

# 250. Temporal Partitioning

Large observation tables MAY eventually partition by appropriate temporal dimensions based on measured workload.

---

# 251. Archival

Older system versions MAY be archived according to retention policy.

They SHALL remain reconstructable where required.

---

# 252. Temporal Indexing

Indexes SHOULD support major query patterns such as:

```text
current state
point in time
reporting period
vintage
latest eligible before cut-off
```

Exact design is deferred.

---

# 253. Commercial Research Implication

Temporal correctness enables Pulse to sell more than static historical summaries.

It enables:

```text
historical reconstruction
revision analysis
real-time vintage backtesting
regulatory calendars
opportunity timing
risk timing
forecast evolution
decision monitoring
```

---

# 254. Intelligence Timing Product Family

The architecture MAY support products such as:

```text
Regulatory Effective-Date Monitor
Trade Data Revision Monitor
Commodity Forecast Tracker
Opportunity Window Monitor
Market Turning-Point Watch
Decision Assumption Monitor
```

---

# 255. Vintage Intelligence

Statistical revisions themselves can become a research subject.

For example:

```text
Which economies consistently revise export data downward?

Which sectors have the largest initial-estimate errors?

Which indicators provide reliable early estimates?
```

Such questions may be commercially useful for analysts, investors and enterprises.

---

# 256. Early-Warning Advantage

By preserving:

```text
event time
publication time
acquisition time
detection time
```

Pulse can measure its own ability to detect important developments quickly.

---

# 257. Intelligence Lead-Time

Conceptually:

```text
Pulse Detection
      │
      │  intelligence lead
      ▼
───────────────●─────────────── Time
               │
               ▼
       Broad Market Recognition
```

A demonstrable intelligence lead may itself become a commercial differentiator.

---

# 258. Decision Reconstruction

Temporal lineage enables a future client to ask:

> Why did we make this decision eighteen months ago?

Pulse can reconstruct:

```text
evidence available then
+
source vintages then
+
model version then
+
assumptions then
+
recommendation then
+
decision then
```

without contaminating the answer with knowledge acquired later.

---

# 259. Institutional Learning

Pulse can then compare:

```text
WHAT WE KNEW
      ↓
WHAT WE EXPECTED
      ↓
WHAT WE DECIDED
      ↓
WHAT ACTUALLY HAPPENED
      ↓
WHAT WE KNOW NOW
```

This is substantially richer than ordinary business intelligence.

---

# 260. Rejected Alternative — One Timestamp

Rejected.

It destroys temporal meaning.

---

# 261. Rejected Alternative — Only `created_at` and `updated_at`

Rejected.

Database lifecycle timestamps do not represent real-world temporal semantics.

---

# 262. Rejected Alternative — Keep Only Latest Value

Rejected.

It prevents historical reconstruction, backtesting and report reproduction.

---

# 263. Rejected Alternative — Rewrite Revised Statistics

Rejected.

Earlier vintages SHALL remain historically available.

---

# 264. Rejected Alternative — Bitemporal Everything

Also rejected.

Bitemporal storage introduces complexity and SHALL be used where temporal reconstruction materially justifies it.

---

# 265. Rejected Alternative — Ignore Publication Availability in Backtests

Rejected.

This creates look-ahead bias.

---

# 266. Rejected Alternative — Treat Forecast as Future Observation

Rejected.

Forecast and realised evidence have different epistemic meanings.

---

# 267. Rejected Alternative — Global Freshness Threshold

Rejected.

Freshness is domain-, metric- and source-dependent.

---

# 268. Governing Invariants

**TIME-PULSE-001**  
Domain time SHALL remain distinct from database lifecycle time.

**TIME-PULSE-002**  
Applicable temporal dimensions SHALL not be collapsed into one timestamp.

**TIME-PULSE-003**  
Pulse SHALL preserve source temporal precision.

**TIME-PULSE-004**  
Pulse SHALL not invent unsupported temporal precision.

**TIME-PULSE-005**  
Reporting period SHALL remain distinct from publication time.

**TIME-PULSE-006**  
Publication time SHALL remain distinct from retrieval time.

**TIME-PULSE-007**  
Event time SHALL remain distinct from processing time.

**TIME-PULSE-008**  
Effective time SHALL remain distinct from announcement or publication time.

**TIME-PULSE-009**  
Forecast origin SHALL remain distinct from forecast target time.

**TIME-PULSE-010**  
Historical forecasts SHALL not be overwritten by later forecasts.

**TIME-PULSE-011**  
Revised observations SHALL preserve earlier vintages.

**TIME-PULSE-012**  
ResearchSnapshots SHALL pin material data vintages.

**TIME-PULSE-013**  
Historical products SHALL not silently rebind to newer evidence.

**TIME-PULSE-014**  
Living products SHALL version material updates.

**TIME-PULSE-015**  
Backtests SHALL declare their vintage policy.

**TIME-PULSE-016**  
Real-time historical backtests SHALL prevent look-ahead bias.

**TIME-PULSE-017**  
Derived temporal transformations SHALL preserve lineage.

**TIME-PULSE-018**  
Historical monetary conversions SHALL declare their FX temporal methodology.

**TIME-PULSE-019**  
Late-arriving evidence SHALL not silently rewrite published intelligence.

**TIME-PULSE-020**  
Freshness SHALL be domain-specific.

**TIME-PULSE-021**  
Stale evidence SHALL remain historical evidence unless retention policy removes it.

**TIME-PULSE-022**  
Temporal joins SHALL respect evidence availability for historical modelling.

**TIME-PULSE-023**  
Point-in-time reconstruction SHALL exclude evidence not yet legitimately available.

**TIME-PULSE-024**  
Decision records SHALL reference the exact Recommendation available at decision time.

**TIME-PULSE-025**  
Outcome evaluation SHALL respect intended evaluation windows.

**TIME-PULSE-026**  
Temporal uncertainty SHALL remain explicit.

**TIME-PULSE-027**  
Temporal classification changes SHALL preserve history.

**TIME-PULSE-028**  
Bitemporal semantics SHALL be applied where business meaning requires both valid and knowledge/system time.

**TIME-PULSE-029**  
Bitemporal complexity SHALL not be imposed indiscriminately.

**TIME-PULSE-030**  
Temporal semantics SHALL remain independent of physical persistence technology.

---

# 269. Consequences

## Positive

This architecture enables:

```text
historically correct research
real-time vintage backtesting
reproducible reports
revision analysis
regulatory effective-date intelligence
forecast evaluation
opportunity timing
risk timing
decision reconstruction
anti-look-ahead controls
living intelligence
```

It gives Pulse a substantially stronger temporal model than ordinary reporting systems.

## Costs

It introduces complexity in:

```text
storage
queries
indexes
testing
revisions
API semantics
data ingestion
analytical methodology
```

and requires domain teams to understand the meaning of time rather than treat it as a generic technical field.

That complexity is justified because temporal ambiguity can materially change an intelligence conclusion.

---

# 270. Strategic Consequence — Pulse Can Preserve Historical Reality

Most analytical systems eventually overwrite yesterday's understanding with today's corrected data.

Pulse SHALL preserve both.

It can therefore distinguish:

```text
REALITY AS CURRENTLY UNDERSTOOD
```

from:

```text
REALITY AS IT COULD HAVE BEEN UNDERSTOOD THEN
```

That distinction is essential for evaluating real decisions.

---

# 271. Strategic Consequence — Pulse Can Measure Whether It Was Early

Once Pulse knows:

```text
event occurred
source published
Pulse acquired
Pulse detected
client notified
market broadly recognised
```

it can begin measuring **intelligence lead-time**.

That creates an unusually important performance question:

> Did Pulse merely explain what everybody already knew, or did it identify the development while commercial advantage still existed?

---

# 272. Strategic Consequence — Time Becomes Part of Opportunity Scoring

A commercially attractive opportunity with:

```text
high demand
high margin
low competition
```

may still be worthless if:

```text
the window closes in 14 days
```

and market entry requires six months.

Pulse can therefore reason:

```text
ATTRACTIVENESS
       +
ACTIONABILITY
       +
TIME AVAILABLE
       -
EXECUTION LEAD TIME
       =
REALISTIC OPPORTUNITY
```

---

# 273. Strategic Consequence — Research Becomes Continuously Re-Evaluable

A report no longer has to be treated as an artefact frozen forever after publication.

Its historical edition remains immutable, but Pulse can monitor the assumptions supporting it:

```text
Report
  ↓
Claims
  ↓
Assumptions
  ↓
Evidence
  ↓
Temporal validity
```

When important evidence expires, changes or becomes effective, Pulse can identify the need for reassessment.

---

# 274. Strategic Consequence — A New Commercial Category

This architecture enables Nabhold eventually to sell not only:

```text
"Here is our report."
```

but:

```text
"Here is our report,
here is exactly what was known when we wrote it,
and we will tell you when the evidence supporting it materially changes."
```

That transforms research from a document transaction into a continuing intelligence relationship.

---

# 275. Final Decision Statement

Baobab Pulse SHALL adopt a **multi-temporal, selectively bitemporal and data-vintage-aware architecture**.

Pulse SHALL preserve the distinctions among:

```text
WHEN IT HAPPENED
WHEN IT WAS TRUE
WHEN IT WAS OBSERVED
WHEN IT WAS REPORTED
WHEN IT WAS PUBLISHED
WHEN IT BECAME EFFECTIVE
WHEN PULSE ACQUIRED IT
WHEN PULSE PROCESSED IT
WHEN PULSE KNEW IT
WHEN IT WAS REVISED
WHEN IT WAS SUPERSEDED
```

and SHALL preserve historical data vintages sufficient to reconstruct consequential analytical states.

The resulting temporal model SHALL support:

```text
                    REAL WORLD
                        │
                  valid/event time
                        │
                        ▼
                      SOURCE
                        │
                  publication time
                        │
                        ▼
                    ACQUISITION
                        │
                   retrieval time
                        │
                        ▼
                      PULSE
                        │
                  knowledge time
                        │
                        ▼
                    ANALYSIS
                        │
                  evidence cut-off
                        │
                        ▼
                 RECOMMENDATION
                        │
                   decision time
                        │
                        ▼
                    DECISION
                        │
                        ▼
                     OUTCOME
                        │
                   outcome time
```

Consequently, Pulse SHALL be capable of answering two fundamentally different questions:

> **What do we know now about what happened then?**

and:

> **What could we actually have known then?**

For a system intended to discover opportunities, assess risk, publish research and learn from decisions, both questions are indispensable.