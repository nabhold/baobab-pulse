# ADR-PULSE-005 — Canonical Observation Model and Domain-Specific Evidence Profiles

**Status:** Proposed  
**Decision ID:** `ADR-PULSE-005`  
**Engine:** Baobab Pulse  
**Repository:** `nabhold/baobab-pulse`  
**Parent Architecture:** `ARCH-PULSE-001`  
**Parent Semantic Contract:** `ARCH-PULSE-CIM-001`  
**Depends on:** `ADR-PULSE-001` through `ADR-PULSE-004`  
**Decision Type:** Canonical Data Semantics and Domain Intelligence Architecture

---

# 1. Context

Baobab Pulse must reason across fundamentally different forms of evidence.

A single commercial investigation might require:

```text
FX rates
commodity prices
trade flows
tariffs
customs information
macroeconomic indicators
weather
climate
market prices
company registries
geospatial information
government open data
news
regulatory changes
MedusaJS commerce data
iDempiere ERP data
Payload CMS information
```

These datasets have almost nothing in common at their provider-schema level.

Nevertheless, Pulse must eventually answer cross-domain questions such as:

> Which East African origin currently presents the strongest risk-adjusted sourcing opportunity for a South African coffee importer?

That question may require simultaneous interpretation of:

```text
coffee production
+
bilateral trade
+
commodity prices
+
USD/ZAR
+
local currencies
+
weather anomalies
+
tariffs
+
transport corridors
+
supplier identities
+
regulatory requirements
+
internal procurement costs
+
internal demand
```

If every domain is modelled independently, cross-domain intelligence becomes an endless integration exercise.

If every domain is forced into one simplistic table such as:

```text
date | subject | metric | value
```

Pulse loses precisely the specialist semantics required to produce credible intelligence.

Neither extreme is acceptable.

---

# 2. Decision

Pulse SHALL implement a **Canonical Observation Kernel with Domain-Specific Evidence Profiles**.

The architecture SHALL follow:

```text
                 CANONICAL OBSERVATION
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    common identity   common time     common provenance
        │                │                │
        └────────────────┼────────────────┘
                         │
                 DOMAIN PROFILE
                         │
       ┌─────────────────┼──────────────────┐
       ▼                 ▼                  ▼
      FX               TRADE             WEATHER
       │                 │                  │
 COMMODITY            CUSTOMS           REGULATION
       │                 │                  │
    MACRO             REGISTRY             GEO
```

The Canonical Observation defines universal intelligence semantics.

A Domain Profile defines additional semantics required to interpret observations correctly within a specialist domain.

---

# 3. Governing Principle

> **Canonicalise what is genuinely common. Preserve what is meaningfully different.**

Pulse SHALL not pursue uniformity merely for implementation convenience.

---

# 4. Observation Kernel

Every canonical Observation SHALL conceptually contain:

```text
Observation
 ├── observation_id
 ├── observation_type
 ├── domain
 ├── subject
 ├── metric
 ├── value
 ├── value_type
 ├── unit
 ├── currency
 ├── temporal_context
 ├── geographic_context
 ├── market_context
 ├── tenant_context
 ├── source_reference
 ├── provenance
 ├── quality_profile
 ├── confidence
 ├── classification
 ├── revision
 ├── lifecycle_status
 └── domain_profile
```

Not every field is mandatory for every observation.

Domain profiles define applicable requirements.

---

# 5. Observation Is a Claim About the World

An Observation SHALL represent:

> **A sourced assertion about some property of some subject within a defined context.**

Conceptually:

```text
SUBJECT
   │
   │ has
   ▼
METRIC
   │
   │ represented by
   ▼
VALUE
   │
   │ within
   ▼
TIME + PLACE + MARKET + CONTEXT
   │
   │ according to
   ▼
SOURCE
```

---

# 6. Observation Is Not Necessarily Truth

This distinction is fundamental.

Suppose:

```text
Source A:
Coffee production = 6.2 million bags

Source B:
Coffee production = 6.8 million bags
```

Pulse SHALL be capable of storing both.

The Observation means:

```text
Source A asserts X
```

not:

```text
Pulse declares X universally true
```

---

# 7. Observation Identity

Each Observation SHALL have an immutable canonical identity.

Observation identity SHALL NOT depend solely upon:

```text
source record ID
metric
subject
timestamp
```

because revisions and corroborating observations may share these characteristics.

---

# 8. Observation Domain

Every Observation SHALL declare a primary `domain`.

Initial canonical domains SHALL include:

```text
FX
COMMODITY
TRADE
CUSTOMS
MACROECONOMIC
WEATHER
CLIMATE
MARKET_PRICE
COMPANY_REGISTRY
GEOSPATIAL
GOVERNMENT_OPEN_DATA
NEWS
REGULATORY
CONTENT
COMMERCE
ERP
OTHER
```

Domain taxonomies SHALL be versioned through shared contracts.

---

# 9. Subject

Every Observation SHALL concern one or more identifiable subjects.

Examples:

```text
currency pair
commodity
country
company
product
market
trade corridor
regulation
location
economic indicator
shipment
sector
customer segment
```

---

# 10. Subject References

Where a canonical Baobab entity exists, Pulse SHALL reference it.

Pulse SHALL not create competing canonical identities for:

```text
Market
DigitalEstate
LegalEntity
Organisation
Engine
Commodity
Location
```

where those identities are governed elsewhere.

---

# 11. Composite Subjects

Some observations inherently concern relationships.

Example:

```text
Uganda → South Africa
green coffee exports
2025
```

The subject is not simply Uganda.

It represents:

```text
reporter = Uganda
partner = South Africa
commodity = green coffee
flow = export
```

Domain profiles SHALL support such composite semantics.

---

# 12. Metric

A `Metric` defines what is being observed.

Examples:

```text
exchange_rate
export_value
export_quantity
rainfall
inflation_rate
commodity_price
tariff_rate
company_status
freight_cost
```

Metrics SHALL have canonical definitions.

---

# 13. Metric Registry

Pulse SHALL maintain or consume a governed Metric Registry.

Conceptually:

```text
MetricDefinition
 ├── metric_id
 ├── canonical_code
 ├── name
 ├── description
 ├── domain
 ├── value_type
 ├── expected_unit
 ├── aggregation_semantics
 ├── temporal_semantics
 ├── dimensionality
 └── version
```

---

# 14. Metric Semantics

Metrics SHALL define whether they are:

```text
FLOW
STOCK
RATE
INDEX
COUNT
PRICE
RATIO
STATUS
CATEGORY
TEXT
GEOMETRY
EVENT
```

This prevents invalid aggregation.

---

# 15. Flow versus Stock

For example:

```text
annual exports
```

may be summed over compatible periods.

But:

```text
foreign reserves at month-end
```

cannot simply be summed across months.

The MetricDefinition SHALL encode this distinction.

---

# 16. Value Types

Canonical value types SHOULD include:

```text
DECIMAL
INTEGER
BOOLEAN
STRING
CATEGORY
DATE
DATETIME
INTERVAL
MONEY
QUANTITY
PERCENTAGE
RATE
INDEX
GEOMETRY
REFERENCE
DOCUMENT
JSON_STRUCTURE
```

---

# 17. Missing Is Not Zero

Pulse SHALL distinguish:

```text
0
```

from:

```text
UNKNOWN
NOT_AVAILABLE
NOT_APPLICABLE
NOT_COLLECTED
WITHHELD
SUPPRESSED
```

This is mandatory for statistical integrity.

---

# 18. Measurement

A `Measurement` SHALL be a numeric Observation carrying:

```text
value
unit
precision
```

and, where applicable:

```text
currency
```

---

# 19. Money

Money SHALL always be:

```text
amount + currency
```

Never:

```text
amount
```

alone.

---

# 20. Quantity

Quantity SHALL always carry its unit where applicable.

```text
60
```

is insufficient.

```text
60 kg
```

is meaningful.

---

# 21. Unit Registry

Pulse SHALL use governed units.

Examples:

```text
kg
tonne
litre
barrel
hectare
mm
km
MWh
bag_60kg
```

Domain-specific units MAY exist.

---

# 22. Conversion

Unit conversion SHALL create traceable transformation lineage.

Original values SHALL remain recoverable.

---

# 23. Temporal Context

Every Observation SHALL define appropriate temporal semantics.

Possible dimensions:

```text
valid_time
observed_time
published_time
effective_time
retrieved_time
processed_time
```

---

# 24. Reporting Period

Statistical observations SHOULD use a structured `ReportingPeriod`.

Examples:

```text
2026
2026-Q2
2026-M08
2026-W31
```

rather than invented timestamps.

---

# 25. Geographic Context

An Observation MAY reference:

```text
country
region
district
municipality
site
coordinates
geometry
economic region
trade bloc
```

---

# 26. Market Context

Geography and Market SHALL remain distinct.

A South African market may involve:

```text
South African buyers
+
Ugandan suppliers
+
USD invoicing
+
Durban port
```

A country is therefore not synonymous with a market.

---

# 27. Observation Profiles

Every specialist domain SHALL define an Observation Profile specifying:

```text
required dimensions
optional dimensions
allowed metrics
allowed units
temporal semantics
revision semantics
quality rules
identity rules
domain-specific invariants
```

---

# 28. FX Profile

The FX domain SHALL preserve:

```text
base_currency
quote_currency
rate
rate_type
market/provider
bid
ask
mid
observation_time
reference_time
```

where applicable.

---

# 29. Currency Pair Direction

```text
USD/ZAR
```

is not semantically equivalent to:

```text
ZAR/USD
```

although one may be mathematically derived from the other.

The base/quote order SHALL be explicit.

---

# 30. FX Rate Types

Pulse SHALL distinguish:

```text
SPOT
REFERENCE
CLOSING
OPENING
BID
ASK
MID
INDICATIVE
FIXING
CROSS
FORWARD
```

as appropriate.

---

# 31. Official versus Market FX

An official central-bank reference rate SHALL not automatically be treated as an executable market rate.

---

# 32. FX Derived Cross

If:

```text
UGX/ZAR
```

is derived through:

```text
UGX/USD × USD/ZAR
```

the resulting rate SHALL retain both contributing observations.

---

# 33. FX Timestamp Sensitivity

FX comparisons SHALL use temporally compatible rates.

Using today's FX to convert a historical transaction without explicit intent is prohibited.

---

# 34. FX Commercial Intelligence

The profile SHALL support derivation of:

```text
currency exposure
volatility
conversion cost
margin sensitivity
landed-cost sensitivity
```

without redefining those derivatives as raw FX observations.

---

# 35. Commodity Profile

Commodity observations SHALL support:

```text
commodity
grade
variety
benchmark
exchange
contract
delivery_month
origin
delivery_location
price
currency
unit
observation_time
```

---

# 36. Commodity Identity

"Coffee" alone may be insufficient.

Pulse MAY need:

```text
Arabica
Robusta
green coffee
roasted coffee
specialty grade
commercial grade
specific origin
```

depending upon analysis.

---

# 37. Benchmark versus Physical Market

A futures benchmark SHALL not automatically equal the physical purchase price available to a specific buyer.

---

# 38. Commodity Basis

Pulse SHOULD support:

```text
physical_price - benchmark_price
```

as derived evidence where appropriate.

---

# 39. Contract Semantics

Commodity futures observations SHALL preserve:

```text
contract
expiry/delivery month
exchange
settlement type
```

where relevant.

---

# 40. Commodity Units

Pulse SHALL preserve original units such as:

```text
USD/lb
USD/tonne
USD/bushel
```

before conversion.

---

# 41. Trade Profile

Trade is a flagship Pulse domain.

A canonical TradeObservation SHALL support:

```text
reporter
partner
commodity
classification_system
classification_revision
commodity_code
flow
period
trade_value
currency
quantity
quantity_unit
net_weight
gross_weight
transport_mode
customs_procedure
source
```

as applicable.

---

# 42. Reporter and Partner

Reporter and Partner SHALL remain directional.

```text
Uganda exports to South Africa
```

is not semantically identical to:

```text
South Africa reports imports from Uganda
```

even where both concern the same physical flow.

---

# 43. Mirror Trade

Pulse MAY compare:

```text
reported exports
```

against:

```text
partner-reported imports
```

as mirror statistics.

Differences SHALL not automatically be classified as errors.

---

# 44. Trade Flow

Canonical values SHALL include:

```text
EXPORT
IMPORT
RE_EXPORT
RE_IMPORT
```

where sources support them.

---

# 45. Commodity Classification

Trade observations SHALL identify both:

```text
classification system
```

and:

```text
classification revision
```

Examples:

```text
HS2017
HS2022
```

---

# 46. HS Code Is Not Universal Identity

The same numeric code may not have identical meaning across classification revisions.

Therefore:

```text
090111
```

without:

```text
HS revision
```

is incomplete.

---

# 47. Trade Concordance

Cross-revision analysis SHALL use explicit concordance mappings.

Concordance may be:

```text
ONE_TO_ONE
ONE_TO_MANY
MANY_TO_ONE
AMBIGUOUS
```

---

# 48. Trade Value

Trade value SHALL preserve the source's valuation semantics where known.

Examples may include:

```text
FOB
CIF
customs value
```

These SHALL not be conflated.

---

# 49. Unit Value

Pulse MAY derive:

```text
trade_value / quantity
```

as an approximate unit value.

It SHALL NOT automatically call this:

```text
market price
```

because composition and reporting effects may materially distort it.

---

# 50. Trade Quantity

Quantity and net weight SHALL remain separate where both are provided.

---

# 51. Trade Partner Aggregates

Special partners such as:

```text
World
Unspecified
Special Categories
```

SHALL not be treated as ordinary countries.

---

# 52. Trade Commercial Derivatives

Trade observations may support:

```text
growth
market share
supplier concentration
destination concentration
revealed trade patterns
market penetration
import dependency
```

through versioned methodologies.

---

# 53. Customs Profile

Customs observations SHALL support, where lawful:

```text
declaration
commodity
HS classification
origin
destination
customs office
port
procedure
valuation
duty
tax
clearance
importer/exporter reference
transport mode
```

---

# 54. Customs Sensitivity

Customs data MAY contain commercially sensitive or personal information.

The profile SHALL support stronger classifications and access policies than aggregated trade statistics.

---

# 55. Tariff Profile

Tariff observations SHALL support:

```text
jurisdiction
partner/origin
commodity classification
tariff type
rate
rate structure
effective_from
effective_to
legal basis
preference scheme
quota
```

---

# 56. Tariff Types

Pulse SHALL distinguish:

```text
MFN_APPLIED
BOUND
PREFERENTIAL
TEMPORARY
ANTI_DUMPING
SAFEGUARD
COUNTERVAILING
OTHER
```

where applicable.

---

# 57. Ad Valorem versus Specific Duty

```text
10%
```

and:

```text
R5/kg
```

are fundamentally different tariff structures.

Pulse SHALL preserve this distinction.

---

# 58. Preferential Eligibility

A preferential tariff SHALL not automatically be applied merely because two countries belong to an agreement.

Eligibility may depend on:

```text
rules of origin
product
documentation
quota
effective date
```

---

# 59. Landed Cost Relationship

Tariff observations MAY feed LandedCostAnalysis but SHALL remain separate canonical evidence.

---

# 60. Macroeconomic Profile

Macroeconomic observations SHALL support:

```text
indicator
geography
period
frequency
value
unit
methodology
seasonal_adjustment
price_basis
currency_basis
release
vintage
```

---

# 61. Macro Indicators

Examples include:

```text
GDP
GDP growth
inflation
policy rate
unemployment
government debt
current account
foreign reserves
population
industrial production
agricultural production
money supply
```

---

# 62. Nominal versus Real

Pulse SHALL distinguish:

```text
nominal GDP
```

from:

```text
real GDP
```

and preserve base-year or methodology metadata where relevant.

---

# 63. Current versus Constant Prices

These SHALL not be conflated.

---

# 64. Seasonally Adjusted Data

Seasonally adjusted and unadjusted observations SHALL remain distinguishable.

---

# 65. Macro Revisions

Macroeconomic datasets commonly revise historical values.

Vintage semantics defined by `ADR-PULSE-004` SHALL apply.

---

# 66. Indicator Methodology

An indicator code alone is insufficient where methodology changes materially.

Pulse SHOULD retain methodology-version references where available.

---

# 67. Weather Profile

Weather observations SHALL support:

```text
location
station/grid
metric
measurement
unit
observed_time
measurement_method
source
```

---

# 68. Weather Metrics

Examples:

```text
temperature
rainfall
humidity
wind speed
wind direction
pressure
soil moisture
solar radiation
```

---

# 69. Station versus Grid

A station measurement and a gridded model estimate SHALL not be treated as methodologically identical.

---

# 70. Weather Forecast Profile

Forecasts SHALL additionally preserve:

```text
forecast_origin
target_time
forecast_horizon
model
model_run
predicted_value
uncertainty
```

---

# 71. Forecast Is Not Observation

A weather forecast SHALL never silently become a measured historical observation after the target time passes.

The actual observation must be separately acquired.

---

# 72. Forecast Evaluation

After the target period:

```text
Forecast
   ↓ compare
Actual Observation
   ↓
ForecastEvaluation
```

---

# 73. Climate Profile

Climate evidence SHALL be distinguished from short-term weather.

Possible concepts:

```text
climate normal
anomaly
drought index
long-term rainfall trend
temperature anomaly
climate projection
```

---

# 74. Climate Projection

A climate-model projection SHALL retain:

```text
model
scenario
ensemble
projection period
uncertainty
```

and SHALL not be presented as a deterministic forecast.

---

# 75. Agricultural Climate Link

Weather and climate evidence MAY be mapped to:

```text
crop
production area
growing season
harvest period
```

through derived agricultural intelligence.

---

# 76. Market Price Profile

MarketPriceObservation SHALL support:

```text
product
market
location
seller/market type
price
currency
unit
price_basis
observation_time
```

---

# 77. Price Basis

Possible bases include:

```text
RETAIL
WHOLESALE
FARM_GATE
AUCTION
SPOT
CONTRACT
LIST
TRANSACTION
ASKING
```

These SHALL remain distinct.

---

# 78. Asking versus Transaction Price

An advertised property price, for example, SHALL not automatically be interpreted as a completed transaction price.

---

# 79. Market Price Comparability

Pulse SHALL consider:

```text
quality
package size
location
tax inclusion
delivery basis
time
```

before comparing prices.

---

# 80. Freight Price Profile

Freight observations SHOULD support:

```text
origin
destination
transport_mode
equipment/container
commodity class
rate
currency
unit
validity
surcharges
```

---

# 81. Freight Rate Basis

Examples:

```text
USD/container
USD/tonne
USD/km
```

shall remain explicit.

---

# 82. Company Registry Profile

Registry observations SHALL support:

```text
registered_name
registration_number
jurisdiction
legal_form
incorporation_date
status
registered_address
officers
directors
ownership
industry
filing
source_authority
verified_at
```

subject to law and source availability.

---

# 83. Registry Fact versus Pulse Entity

A registry record is evidence about an organisation.

It is not automatically the Baobab canonical organisation itself.

---

# 84. Registry Status

Possible states might include:

```text
ACTIVE
DISSOLVED
LIQUIDATION
DEREGISTERED
UNKNOWN
```

but source-specific values SHALL be mapped explicitly.

---

# 85. Ownership Relationships

Ownership SHALL preserve:

```text
parent
child
relationship type
percentage where known
validity
source
```

---

# 86. Beneficial Ownership

Beneficial-ownership information SHALL receive appropriate legal, privacy and confidence controls.

---

# 87. Company Activity Inference

A registered company does not necessarily indicate an operating company.

Operational activity requires additional evidence.

---

# 88. Geospatial Profile

Geospatial observations SHALL support:

```text
geometry
coordinate_reference_system
location type
validity
accuracy
source
```

---

# 89. Geometry Types

Pulse SHOULD support:

```text
POINT
LINE
POLYGON
MULTIPOINT
MULTILINE
MULTIPOLYGON
```

where needed.

---

# 90. Coordinate Reference System

CRS SHALL be explicit where required.

Coordinates SHALL not be assumed universally interchangeable.

---

# 91. Location Accuracy

Geospatial evidence SHOULD preserve accuracy/resolution where known.

---

# 92. Administrative Boundaries

Boundary datasets SHALL be versioned.

A district boundary in 2020 may differ from one in 2026.

---

# 93. Geospatial Derived Evidence

Derived analyses MAY include:

```text
distance
proximity
catchment
route
intersection
coverage
density
accessibility
```

---

# 94. Spatial Relationship

Pulse SHOULD support semantic relationships such as:

```text
WITHIN
INTERSECTS
NEAR
CONNECTED_TO
SERVES
```

without requiring a graph database.

---

# 95. Government Open Data Profile

Government datasets SHALL retain:

```text
publishing authority
dataset
jurisdiction
methodology
publication date
reporting period
revision
```

---

# 96. Government Data Authority

Official publication increases source authority.

It SHALL NOT remove the need for quality assessment.

---

# 97. Procurement Profile

Where lawful, procurement evidence MAY support:

```text
buyer
supplier
tender
award
amount
currency
category
location
publication
deadline
status
```

---

# 98. Project Profile

Public project observations MAY support:

```text
project
sponsor
sector
location
budget
currency
status
planned_start
planned_completion
contractor
funding source
```

---

# 99. News Profile

News observations SHALL preserve:

```text
publisher
article
headline
authors
publication_time
language
jurisdiction
URL
retrieved_time
rights
```

---

# 100. News Article Is Source Evidence

Pulse SHALL distinguish:

```text
Article
```

from:

```text
Event extracted from Article
```

and:

```text
Claim extracted from Article
```

---

# 101. News Event Extraction

An extracted event MAY contain:

```text
event_type
entities
location
event_time
description
source_articles
confidence
```

---

# 102. News Syndication

Pulse SHOULD attempt to distinguish independent reporting from syndicated duplication where practical.

---

# 103. Sentiment

Sentiment derived from news SHALL be:

```text
DERIVED ANALYSIS
```

not source fact.

---

# 104. Narrative Signals

Pulse MAY track changes in:

```text
topic frequency
sentiment
entity mentions
narrative emergence
```

provided methodology is explicit.

---

# 105. Regulatory Profile

Regulatory evidence SHALL support:

```text
jurisdiction
authority
instrument
instrument_type
title
publication
subject
affected sectors
affected products
announcement_date
publication_date
adoption_date
effective_date
expiry
repeal
legal_status
source_document
```

---

# 106. Regulatory Lifecycle

Canonical states SHOULD support concepts equivalent to:

```text
ANNOUNCED
PROPOSED
CONSULTATION
ADOPTED
PUBLISHED
EFFECTIVE
AMENDED
SUSPENDED
REPEALED
EXPIRED
```

where appropriate.

---

# 107. Proposed Is Not Effective

A proposed regulation SHALL never be represented as currently binding merely because it has been publicly announced.

---

# 108. Regulatory Delta

Pulse SHALL support:

```text
previous rule
    ↓
change
    ↓
new rule
```

as derived regulatory intelligence.

---

# 109. Effective Period

A regulatory rule SHOULD have:

```text
effective_from
effective_to
```

where known.

---

# 110. Regulatory Applicability

Applicability MAY depend on:

```text
jurisdiction
product
industry
company type
transaction
origin
destination
threshold
```

and therefore SHALL not be inferred solely from document title.

---

# 111. Content Profile

Payload-derived content observations MAY include:

```text
content item
publication status
campaign
taxonomy
audience
publication time
engagement
```

Pulse SHALL not become content authority.

---

# 112. Commerce Profile

MedusaJS-derived observations MAY include:

```text
product
variant
price
market
order
customer segment
inventory
promotion
sales channel
return
cart
```

subject to shared contracts and privacy policy.

---

# 113. ERP Profile

iDempiere-derived observations MAY include:

```text
procurement
supplier
inventory
cost
accounting
receivable
payable
asset
project
cash
```

subject to ERP authority and tenancy boundaries.

---

# 114. Operational Event versus Observation

A canonical event such as:

```text
trade.order.completed
```

is not itself necessarily an Observation.

Pulse MAY transform it into observations such as:

```text
order_value
quantity_sold
customer_activity
```

with lineage to the original event.

---

# 115. Internal Evidence Time

Internal operational data SHALL retain:

```text
occurred_at
recorded_at
processed_at
```

where relevant.

---

# 116. Internal Corrections

Operational corrections SHALL propagate through events or governed APIs.

Pulse SHALL not repair another engine's source record itself.

---

# 117. Cross-Domain Join

Canonical observations exist specifically to permit governed cross-domain relationships.

Example:

```text
TradeObservation
    commodity = coffee
    market = South Africa

CommodityObservation
    commodity = coffee

FXObservation
    currency pair = USD/ZAR

TariffObservation
    commodity = coffee
    jurisdiction = South Africa
```

can participate in one analysis.

---

# 118. Join Semantics

Cross-domain joins SHALL use canonical dimensions such as:

```text
entity
commodity
market
country
currency
time
classification
location
```

rather than provider-specific strings.

---

# 119. Semantic Compatibility

Two observations are not automatically comparable merely because they share a metric name.

Compatibility requires consideration of:

```text
definition
unit
time
geography
methodology
source
classification
```

---

# 120. Comparison Contract

Pulse SHOULD implement a semantic compatibility check before automated comparisons.

---

# 121. Comparison Result

Compatibility MAY be:

```text
COMPATIBLE
COMPATIBLE_AFTER_TRANSFORMATION
PARTIALLY_COMPATIBLE
NOT_COMPARABLE
UNKNOWN
```

---

# 122. Transformation Before Comparison

Example:

```text
USD/lb
```

may be compared with:

```text
USD/kg
```

after unit conversion.

But:

```text
FOB export unit value
```

may not be directly comparable with:

```text
retail shelf price
```

merely after currency conversion.

---

# 123. Analytical Context

Pulse SHALL support an `AnalyticalContext` describing the comparison assumptions.

---

# 124. Observation Families

Domain profiles MAY define specialised semantic subtypes.

Examples:

```text
FXObservation
TradeObservation
TariffObservation
WeatherObservation
RegistryObservation
```

These are logical domain profiles.

They do NOT require one physical database table per subtype.

---

# 125. Physical Storage Independence

This ADR SHALL NOT dictate:

```text
single table
table-per-domain
JSONB profile
partitioning strategy
```

Those decisions belong to the PostgreSQL physical architecture ADR.

---

# 126. Domain Profile Schema

A Domain Profile SHALL itself be versioned.

Conceptually:

```text
DomainProfile
 ├── profile_id
 ├── domain
 ├── version
 ├── required_dimensions
 ├── optional_dimensions
 ├── metric_constraints
 ├── unit_constraints
 ├── temporal_rules
 ├── quality_rules
 ├── compatibility_rules
 └── status
```

---

# 127. Profile Evolution

A new profile version SHALL not silently reinterpret historical observations.

---

# 128. Validation

An Observation SHALL be validated against its declared profile before becoming production-grade evidence.

---

# 129. Validation States

```text
RECEIVED
NORMALISED
VALIDATED
QUARANTINED
REJECTED
```

---

# 130. Structural Validation

Checks:

```text
required dimensions
data types
enumerations
unit presence
currency presence
```

---

# 131. Semantic Validation

Checks may include:

```text
valid currency pair
known country
known HS revision
plausible reporting period
valid regulatory lifecycle
```

---

# 132. Range Validation

Example:

```text
humidity = 950%
```

may warrant quarantine.

But range rules SHALL remain domain-specific.

---

# 133. Cross-Field Validation

Example:

```text
flow = EXPORT
reporter = Uganda
partner = Uganda
```

may require investigation depending upon source semantics.

---

# 134. Source-Specific Exceptions

Domain rules MAY allow source-specific semantics where justified.

These exceptions SHALL be explicit.

---

# 135. Quality Profile

Each Observation SHOULD carry quality assessments appropriate to its domain.

Possible dimensions:

```text
completeness
timeliness
authority
consistency
precision
method quality
corroboration
```

---

# 136. Quality Is Multidimensional

Pulse SHALL not reduce every quality question to a single score.

---

# 137. Confidence

Confidence belongs to an interpretation or assessment.

An official source may have high authority while an individual observation is stale or methodologically uncertain.

---

# 138. Source Observation versus Derived Observation

Every Observation SHALL identify whether it is:

```text
SOURCE_REPORTED
DERIVED
ESTIMATED
MODELLED
MANUAL
```

---

# 139. Estimated Data

Estimated source data SHALL remain distinguishable from directly measured or reported data.

---

# 140. Imputation

Imputed values SHALL be derived observations.

The imputation method SHALL be recorded.

---

# 141. Aggregation

Aggregated observations SHALL retain lineage to their contributing observation set or reproducible query.

---

# 142. Aggregation Semantics

Metric definitions SHALL specify whether aggregation supports:

```text
SUM
AVERAGE
WEIGHTED_AVERAGE
MIN
MAX
LAST
FIRST
NONE
CUSTOM
```

---

# 143. No Blind Averaging

Rates, indices, prices and ratios SHALL not be blindly averaged without defined methodology.

---

# 144. Derived Indicator

Pulse MAY define reusable derived indicators.

Example:

```text
ImportDependencyRatio
```

The indicator SHALL specify:

```text
formula
inputs
method version
```

---

# 145. Indicator Registry

Derived indicators SHOULD live in a versioned Indicator Registry.

---

# 146. Observation Granularity

Observations SHALL preserve the finest meaningful granularity available and permitted.

Aggregation can happen later.

Destroyed granularity cannot easily be recovered.

---

# 147. Privacy Constraint

The previous rule SHALL not override:

```text
privacy
licensing
security
data minimisation
```

requirements.

---

# 148. Statistical Disclosure

Aggregated outputs MAY be required where individual-level data would create disclosure risk.

---

# 149. Cross-Tenant Aggregation

Cross-tenant intelligence SHALL require explicit policy.

---

# 150. Anonymous Benchmarking

Future Pulse products MAY provide anonymised benchmarks across consenting tenants.

Such functionality SHALL require a separate privacy and aggregation decision.

---

# 151. Observation Provenance

Every material Observation SHALL resolve through:

```text
Observation
    ↓
Transformation
    ↓
RawRecord
    ↓
SourceArtefact
    ↓
Acquisition
    ↓
Dataset
    ↓
DataSource
    ↓
Source
```

where applicable.

---

# 152. Domain-Specific Provenance

Profiles MAY require additional provenance.

Example:

Trade:

```text
classification revision
```

Weather:

```text
model/station
```

Regulation:

```text
legal instrument
```

---

# 153. Observation Revision

Observation revisions SHALL follow `ADR-PULSE-004`.

No destructive historical replacement.

---

# 154. Observation Supersession

```text
Observation v2
    SUPERSEDES
Observation v1
```

---

# 155. Observation Correction

Corrections SHALL state whether they arise from:

```text
source revision
mapping correction
parser correction
entity-resolution correction
methodology correction
```

---

# 156. Observation Validity

Some observations have explicit validity windows.

Example:

```text
tariff rate
freight quote
regulation
```

Others represent historical measurements.

Profiles SHALL define appropriate semantics.

---

# 157. Observation Freshness

Freshness SHALL be domain-specific.

Examples:

```text
FX                 minutes/hours
weather forecast   hours
market price       hours/days
trade statistics   months
GDP                 quarters
company registry   days/months
```

---

# 158. Freshness Does Not Mean Correctness

A fresh source can be wrong.

An older source can remain authoritative for a historical period.

---

# 159. Domain Productisation

Each evidence domain SHOULD be designed not merely for ingestion but for reusable commercial intelligence.

Examples:

```text
FX
→ FX Pulse

Trade
→ Trade Pulse

Commodity
→ Commodity Pulse

Regulation
→ Regulatory Pulse

Country + Macro + Trade
→ Country Pulse

Weather + Commodity + Trade
→ Supply Risk Pulse
```

---

# 160. Cross-Domain Productisation

The greatest value emerges when domains combine.

```text
TRADE
 +
FX
 +
COMMODITY
 +
TARIFF
 +
LOGISTICS
 +
REGULATION
       ↓
TRADE OPPORTUNITY
```

---

# 161. Opportunity Evidence Cube

For opportunity research, Pulse SHOULD conceptually evaluate multiple dimensions:

```text
                  DEMAND
                    │
                    │
SUPPLY ───── OPPORTUNITY ───── PRICE
                    │
                    │
                 ACCESS
```

with additional dimensions:

```text
RISK
REGULATION
LOGISTICS
MACRO
TIMING
STRATEGIC FIT
```

---

# 162. Evidence Domain Coverage

A ResearchMission SHOULD know which domains support its conclusion.

Example:

```text
Trade          ✓
FX             ✓
Commodity      ✓
Regulation     ✓
Weather        ✓
Company        partial
Logistics      missing
```

---

# 163. Domain Coverage Is Not Evidence Strength

Five weak domains do not automatically outweigh two strong sources.

---

# 164. Niche Intelligence

Domain Profiles SHALL be extensible enough to support specialist future domains.

Examples:

```text
agricultural crop cycles
port congestion
electricity reliability
mining licences
construction permits
property transactions
shipping movements
carbon markets
renewable generation
water availability
public procurement
tourism flows
```

without redesigning the Observation Kernel.

---

# 165. Vertical Profiles

A vertical intelligence pack MAY compose several Domain Profiles.

Example:

```text
AGRICULTURE PROFILE
 ├── commodity
 ├── weather
 ├── climate
 ├── trade
 ├── market price
 ├── geospatial
 └── regulation
```

---

# 166. Vertical Profile Does Not Own Raw Semantics

The agriculture vertical consumes the constituent profiles.

It SHALL not redefine them.

---

# 167. Agricultural Season

A future agricultural profile MAY add:

```text
crop
planting season
growing season
harvest season
production region
yield
```

---

# 168. Logistics Profile

A future logistics profile MAY add:

```text
route
mode
carrier
port
border
transit time
capacity
cost
delay
congestion
```

---

# 169. Real Estate Profile

A future real-estate profile MAY add:

```text
property
property type
land use
asking price
transaction price
rent
yield
vacancy
permit
location
```

---

# 170. Energy Profile

A future energy profile MAY add:

```text
generation
capacity
fuel
tariff
load
outage
grid
renewable resource
```

---

# 171. Financial Market Profile

A future financial profile MAY support:

```text
security
exchange
price
yield
volume
market capitalisation
corporate action
```

without contaminating commodity or FX semantics.

---

# 172. Profile Registration

New Domain Profiles SHALL require governance approval before becoming canonical production contracts.

---

# 173. Experimental Profiles

Pulse MAY support:

```text
EXPERIMENTAL
```

profiles during research.

Experimental profiles SHALL not silently become organisation-wide canonical contracts.

---

# 174. Shared Contract Promotion

A mature Pulse profile MAY be promoted into `nabhold/shared` where its semantics become organisation-wide contracts.

---

# 175. Pulse-Local Semantics

Highly intelligence-specific profile details MAY remain owned by Pulse.

---

# 176. Control Plane Relationship

The Control Plane SHALL remain authoritative for platform context and canonical identity/mapping concerns defined by its architecture.

Pulse Domain Profiles SHALL reference those identities.

---

# 177. Provider Code Mapping

Provider codes SHALL map through explicit references.

Example:

```text
provider:
"UGA"

      ↓ ExternalReference

canonical:
country_id = ...
```

---

# 178. Mapping Confidence

Uncertain mappings SHALL not silently become canonical.

---

# 179. Observation Reconciliation

Multiple observations describing apparently identical phenomena MAY be reconciled analytically.

They SHALL not be physically merged merely because their values match.

---

# 180. Consensus Observation

A consensus or blended value SHALL be a new derived Observation.

---

# 181. Benchmark Observation

Pulse MAY designate particular observations as benchmarks according to methodology.

Benchmark status SHALL not erase alternative evidence.

---

# 182. Official Observation

`OFFICIAL` is source classification, not absolute truth.

---

# 183. Client Observation

Client-supplied data MAY participate alongside external evidence.

Its classification and tenant context SHALL be preserved.

---

# 184. Internal Commercial Advantage

This allows:

```text
public market price
+
public trade volume
+
tenant purchase cost
+
tenant sales demand
```

to produce tenant-specific intelligence.

The resulting derived Observation SHALL inherit appropriate confidentiality.

---

# 185. Data Leakage Prevention

Cross-domain joins SHALL enforce tenant and classification policy before computation, not merely before presentation.

---

# 186. Observation Query Semantics

Pulse APIs SHOULD allow filtering by:

```text
domain
metric
subject
country
market
commodity
currency
period
source
quality
classification
tenant
revision
```

---

# 187. Query Defaults

APIs SHALL avoid ambiguous defaults.

For example, querying:

```text
coffee price
```

without:

```text
market
currency
unit
benchmark/basis
time
```

may require qualification rather than returning an arbitrary value.

---

# 188. Latest Value

`latest` SHALL mean:

```text
latest according to defined temporal semantics
```

not merely:

```text
row with greatest database insertion timestamp
```

---

# 189. Current Value

`current` and `latest` MAY differ.

A newly published revision of a historical statistic is latest publication but not a current-period measurement.

---

# 190. Observation Search

Search indexes MAY project observations for discovery.

Search SHALL not become canonical storage.

---

# 191. Vector Embeddings

Embeddings MAY be generated for textual observations/documents.

They SHALL be treated as derived indexes.

---

# 192. LLM Semantic Retrieval

An LLM may retrieve relevant evidence semantically.

Retrieved evidence SHALL still resolve to canonical references.

---

# 193. Natural-Language Query

A future query:

> Show coffee-export growth from East Africa to Southern Africa over five years.

may be translated into canonical filters.

The generated query SHALL be inspectable for consequential analysis.

---

# 194. Machine-Generated Query Validation

LLM-generated analytical queries SHALL be subject to:

```text
tenant scope
classification
semantic compatibility
resource limits
```

---

# 195. Observation Materialisation

Frequently used aggregates MAY be materialised for performance.

They SHALL retain derivation semantics.

---

# 196. Cached Observation

Caching SHALL not alter evidence identity.

---

# 197. Domain Partitioning

Physical partitioning by:

```text
domain
time
tenant
```

MAY later be considered.

This ADR does not prescribe it.

---

# 198. Schema Evolution

Canonical Observation schema evolution SHALL be backward-aware.

Breaking changes require explicit schema versions and migration strategy.

---

# 199. Event Representation

Observation creation or revision MAY produce events such as:

```text
pulse.observation.created
pulse.observation.revised
pulse.observation.invalidated
```

Canonical event schemas belong in `nabhold/shared`.

---

# 200. Bulk Observation Events

High-volume ingestion SHALL not require one heavyweight external event per raw observation if that becomes operationally inefficient.

Batch/event-summary patterns MAY be defined later.

---

# 201. Observation Authority

Pulse is authoritative for:

```text
its canonical representation
its provenance
its quality assessment
its derived observations
```

Pulse is NOT authoritative for the external real-world institution's original assertion.

---

# 202. Commercial Defensibility

A market report must therefore be able to state not merely:

```text
imports grew 17%
```

but internally reconstruct:

```text
metric:
bilateral import value

classification:
HS2022 / relevant code

period:
2025 vs 2024

reporter:
South Africa

partner:
Uganda

source:
specific dataset

source vintage:
specific release

calculation:
growth method vX

currency:
USD

quality:
defined assessment

limitations:
declared
```

That is decision-grade intelligence.

---

# 203. Anti-Pattern — Universal Fact Table

Rejected:

```text
timestamp
name
value
```

for all domains.

It destroys essential semantics.

---

# 204. Anti-Pattern — Provider Tables as Domain Model

Rejected:

```text
world_bank_indicators
wto_trade
provider_x_fx
provider_y_weather
```

as the canonical semantic architecture.

Provider-specific staging is acceptable.

Provider-specific canonical truth is not.

---

# 205. Anti-Pattern — JSON Everything

Rejected as the semantic model.

JSON MAY carry profile-specific fields physically.

But the meaning of those fields SHALL be governed.

---

# 206. Anti-Pattern — Table per Provider

Rejected for canonical storage.

It creates provider lock-in and makes cross-domain research unnecessarily difficult.

---

# 207. Anti-Pattern — Flatten Domain Differences

Rejected.

Trade, weather and regulation are not merely different names for generic metrics.

---

# 208. Anti-Pattern — One Canonical Schema per Domain with No Shared Kernel

Also rejected.

It recreates integration complexity at every analytical boundary.

---

# 209. Governing Invariants

**OBS-PULSE-001**  
Every canonical Observation SHALL identify its domain.

**OBS-PULSE-002**  
Every material Observation SHALL have provenance.

**OBS-PULSE-003**  
Provider schema SHALL not define canonical semantics.

**OBS-PULSE-004**  
Domain-specific meaning SHALL not be discarded merely to obtain structural uniformity.

**OBS-PULSE-005**  
Every measurement SHALL carry appropriate unit semantics.

**OBS-PULSE-006**  
Every monetary value SHALL carry currency.

**OBS-PULSE-007**  
Missing values SHALL not be silently converted to zero.

**OBS-PULSE-008**  
Source-reported and derived observations SHALL remain distinguishable.

**OBS-PULSE-009**  
Forecasts SHALL remain distinct from realised observations.

**OBS-PULSE-010**  
Trade classification SHALL preserve classification system and revision.

**OBS-PULSE-011**  
Trade reporter and partner SHALL remain directional.

**OBS-PULSE-012**  
FX currency-pair direction SHALL be explicit.

**OBS-PULSE-013**  
Tariff structure SHALL preserve ad-valorem versus specific-duty semantics.

**OBS-PULSE-014**  
Regulatory proposal and legal effectiveness SHALL remain distinct.

**OBS-PULSE-015**  
Company registry evidence SHALL not automatically establish operational capability.

**OBS-PULSE-016**  
Geospatial observations SHALL preserve applicable spatial reference semantics.

**OBS-PULSE-017**  
News-derived events SHALL remain traceable to source publications.

**OBS-PULSE-018**  
Canonical entities SHALL reuse Control Plane identities where applicable.

**OBS-PULSE-019**  
Uncertain mappings SHALL not silently become authoritative.

**OBS-PULSE-020**  
Observation revision SHALL preserve historical versions.

**OBS-PULSE-021**  
Cross-domain comparisons SHALL be semantically validated.

**OBS-PULSE-022**  
Derived aggregates SHALL retain lineage.

**OBS-PULSE-023**  
Profile-specific validation SHALL occur before observations become production evidence.

**OBS-PULSE-024**  
Domain Profiles SHALL be versioned.

**OBS-PULSE-025**  
Profile evolution SHALL not silently reinterpret historical evidence.

**OBS-PULSE-026**  
Tenant isolation SHALL apply during analytical computation as well as retrieval.

**OBS-PULSE-027**  
Observation freshness SHALL be domain-specific.

**OBS-PULSE-028**  
Official source status SHALL not eliminate quality assessment.

**OBS-PULSE-029**  
Canonical storage implementation SHALL remain separable from canonical semantic definition.

**OBS-PULSE-030**  
New specialist domains SHALL extend the Observation Kernel through governed profiles rather than fork Pulse.

---

# 210. Consequences

## Positive

This architecture provides:

```text
cross-domain comparability
provider independence
specialist analytical fidelity
traceability
schema evolution
future domain extensibility
reusable research infrastructure
commercial product reuse
```

It enables Pulse to speak one broad intelligence language without pretending every evidence domain speaks the same dialect.

## Costs

It requires:

```text
metric governance
unit governance
domain profiles
classification mappings
semantic validation
concordances
profile versioning
```

This is more work than storing arbitrary JSON.

That work is justified because the semantics themselves become part of Pulse's intellectual property.

---

# 211. Strategic Consequence — The Evidence Matrix

With these profiles in place, Pulse can construct an increasingly rich evidence matrix:

```text
                     TRADE  FX  PRICE  MACRO WEATHER REG COMPANY GEO INTERNAL

COUNTRY                  ●    ●    ●     ●      ●     ●     ●     ●      ●

MARKET                   ●    ●    ●     ●            ●     ●     ●      ●

COMMODITY                ●    ●    ●            ●     ●           ●      ●

COMPANY                  ●    ●    ●                  ●     ●     ●      ●

CORRIDOR                 ●    ●    ●            ●     ●           ●      ●

REGULATION               ●                           ●     ●            ●
```

The intersection of these dimensions is where commercially interesting questions emerge.

---

# 212. Strategic Consequence — Questions Become Computable

Consider:

> Where should a coffee importer source from next year?

Without canonical semantics this is largely manual research.

With domain profiles, Pulse can systematically reason over:

```text
origin export capacity
+
commodity grade
+
historical prices
+
FX exposure
+
weather outlook
+
tariffs
+
supplier availability
+
corridor accessibility
+
internal purchase history
```

while still retaining the specialist meaning of each datum.

---

# 213. Strategic Consequence — New Domains Become Revenue Options

Once the kernel is stable, adding a new evidence domain can unlock an entire family of intelligence products.

For example:

```text
PORT CONGESTION PROFILE
          ↓
Trade Corridor Monitor
Supply Chain Risk Report
Import Delay Alert
Supplier Reliability Analysis
```

or:

```text
BUILDING PERMIT PROFILE
          ↓
Construction Activity Radar
Real Estate Growth Report
Infrastructure Demand Report
Building Materials Opportunity Report
```

or:

```text
PUBLIC PROCUREMENT PROFILE
          ↓
Tender Radar
Government Demand Intelligence
Supplier Opportunity Report
Sector Spending Monitor
```

This is why domain modelling is not merely database design.

It becomes **commercial-option architecture**.

---

# 214. Strategic Consequence — Niche Before Scale

Pulse does not need every possible dataset before it can become commercially useful.

A narrow but deeply modelled combination such as:

```text
TRADE
+
FX
+
COMMODITY
+
TARIFF
+
REGULATION
+
COMPANY
```

may already support formidable specialist research in African cross-border trade.

The architecture therefore favours:

> **depth in commercially meaningful evidence combinations before indiscriminate breadth.**

---

# 215. Strategic Consequence — Semantic Compounding

Every correctly resolved:

```text
country
company
commodity
HS code
currency
market
location
metric
```

makes later research easier.

Every validated mapping becomes reusable.

Every concordance becomes reusable.

Every domain methodology becomes reusable.

The semantic layer therefore compounds in value alongside the evidence corpus.

---

# 216. Final Decision Statement

Baobab Pulse SHALL adopt a **Canonical Observation Kernel plus versioned Domain-Specific Evidence Profiles**.

The kernel SHALL provide common semantics for:

```text
identity
subject
metric
value
unit
currency
time
geography
market
tenant
source
provenance
quality
confidence
classification
revision
```

while domain profiles preserve specialist semantics for:

```text
FX
COMMODITIES
TRADE
CUSTOMS
MACROECONOMICS
WEATHER
CLIMATE
MARKET PRICES
COMPANY REGISTRIES
GEOSPATIAL DATA
GOVERNMENT OPEN DATA
NEWS
REGULATION
CONTENT
COMMERCE
ERP
```

The architecture SHALL deliberately reject both extremes:

```text
EVERY DOMAIN IS DIFFERENT
```

and:

```text
EVERY DOMAIN IS JUST
timestamp + metric + value
```

Instead:

```text
                 COMMON INTELLIGENCE KERNEL
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       identity          context         provenance
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    DOMAIN SEMANTICS
                           │
        ┌──────────┬───────┼───────┬──────────┐
        ▼          ▼       ▼       ▼          ▼
      TRADE       FX    WEATHER   GEO    REGULATION
        │          │       │       │          │
        └──────────┴───────┼───────┴──────────┘
                           ▼
                   CROSS-DOMAIN EVIDENCE
                           │
                           ▼
                      INTELLIGENCE
                           │
                           ▼
                 COMMERCIAL OPPORTUNITY
```

The purpose is not simply to make heterogeneous data fit into PostgreSQL.

The purpose is to make heterogeneous evidence **reason together without losing what makes each source meaningful**.

That semantic capability is foundational to Baobab Pulse becoming not merely a data-processing engine, but a reusable commercial intelligence platform.