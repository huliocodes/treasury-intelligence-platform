# Treasury Intelligence Platform

Data and decision infrastructure for allocating EUR corporate treasury capital across traditional, tokenized, and onchain yield opportunities.

The platform combines market-data ingestion, point-in-time evidence storage, analytical transformations, mandate-aware treasury analysis, evidence and freshness gates, portfolio construction, and human approval boundaries.

The core question is:

> A company has EUR X of treasury capital today. Given its current holdings and cash economics, capital-preservation requirements, EUR/FX constraints, liquidity needs, accessibility requirements, and return objectives, how should that capital be allocated across the relevant accessible opportunity universe?

The current production data path is:

~~~text
OFFICIAL / MARKET DATA SOURCES
├── Agence France Tresor
├── European Central Bank
└── additional TradFi / tokenized / onchain sources
        ↓
PYTHON INGESTION
        ↓
POSTGRESQL APPEND-ONLY MARKET EVIDENCE
        ↓
DBT
├── staging
├── latest evidence mart
├── point-in-time evidence history
└── data-quality tests
        ↓
WAREHOUSE-BACKED OPPORTUNITY INPUTS
        ↓
TREASURY ANALYTICS
├── mandate
├── eligibility
├── position-size analysis
├── risk
├── liquidity
├── return economics
├── evidence sufficiency
└── freshness gates
        ↓
PORTFOLIO DECISION
        ↓
RECOMMENDATION + HUMAN APPROVAL BOUNDARY

Prefect orchestrates the production refresh path.
Docker Compose provides the local PostgreSQL infrastructure.
~~~

Current engineering stack:

~~~text
Python
PostgreSQL 17
dbt
Prefect
Docker Compose
psycopg
requests / BeautifulSoup
web3
Git
~~~

The market-evidence store is append-only. Stable evidence identifiers make source ingestion idempotent, while dbt derives both current-state and point-in-time historical views.

The decision layer consumes persisted warehouse evidence where production ingestion is available rather than making arbitrary live source calls during portfolio construction.

The platform intentionally stops before treasury execution. Recommendations can enter a human approval layer, but execution infrastructure is outside the current scope.

This is not a generic yield dashboard.

---

## Current System Status

The analytical V1 baseline is complete. Development has since extended the project with persistent market evidence, dbt transformations, point-in-time history, live source ingestion, and Prefect orchestration.

Canonical warehouse-backed production state as of **2026-09-08**:

~~~text
Treasury capital:          EUR 5,000,000

Production opportunities:  14
Recommendation-ready:       0
Needs evidence:             9
Blocked:                    5

Decision state:             hold unallocated
Selected opportunity:       none
Allocated capital:          EUR 0
Unallocated capital:        EUR 5,000,000

Recommended action:         hold_unallocated
Recommendation status:      decision_ready
Authorized allocation:      EUR 0
Execution authorized:       False
~~~

The zero-allocation result is intentional.

The system does not weaken risk, liquidity, accessibility, evidence, or freshness requirements merely to produce a recommendation. When no opportunity is recommendation-ready under the current production state, capital remains unallocated.

The current orchestrated pipeline has been validated end to end:

~~~text
AFT BTF ingestion
        ↓
ECB ESTR ingestion
        ↓
PostgreSQL market_evidence
        ↓
dbt build
├── 3 models
└── 45 data tests
        ↓
warehouse-backed production decision
        ↓
Prefect flow Completed
~~~

The current persisted production evidence includes:

~~~text
ECB ESTR
2026-09-07
2.188%
benchmark / estr_rate

French BTF FR0129704153
2026-09-07 auction
2.720%
market_return / auction_weighted_average_rate
~~~

Ingestion is idempotent: rerunning a source adapter for an already-persisted observation produces the same stable evidence identifier and does not create a duplicate row.

### Historical V1 analytical baseline

The detailed V1 sections below preserve the **2026-09-03 analytical acceptance snapshot**.

That historical baseline produced two recommendation-ready opportunities and selected French BTF Aug 2027 at a defensible modeled return of approximately 2.760%.

Those values remain useful as deterministic regression and design documentation. They are **not the current warehouse-backed production recommendation**.

The current production result should always be obtained from the refreshed warehouse-backed pipeline rather than inferred from the historical V1 snapshot.

---

## Business Problem

Corporate cash management is not simply a search for the highest advertised yield.

A EUR-based company may have €1 million, €5 million, €20 million, or substantially more in treasury capital while still needing to:

- preserve principal,
- maintain sufficient liquidity,
- avoid meaningful FX exposure,
- recover capital for operating requirements,
- understand the risks required to earn incremental yield,
- determine whether an opportunity is actually accessible to the company,
- estimate realistic return after access and execution costs,
- determine whether the intended position size can enter and exit,
- compare proposed returns with the company's actual current cash and holdings,
- allocate capital across multiple opportunities when justified,
- and periodically reconsider the allocation as conditions change.

The core analytical unit is therefore not:

> "What product has the highest yield?"

It is:

> "What return is defensible for this treasury, through this access route, at this allocation size, subject to this mandate and current treasury state?"

---

## Company Inputs

The analytical engine is not restricted to a €5 million treasury or a 0% current cash yield.

Relevant company inputs include:

~~~text
Treasury capital
Current positions
Current unallocated cash
Current cash balance(s)
Current cash yield(s)
Cash-return evidence and observation dates
Treasury mandate / constraints
Analysis as-of date
~~~

V1 includes an explicit arbitrary-company acceptance fixture using:

~~~text
Treasury capital:          €10,000,000
Current cash balance:      €10,000,000
Current cash return:       1.250%
Current annual return:     €125,000
~~~

The same 14-opportunity production universe is analyzed at exactly €10 million.

This proves that:

~~~text
€5M treasury capital is not a hidden analytical constant.
0% current cash return is not a hidden analytical constant.
~~~

The €5 million / 0% case remains the deterministic canonical model-company fixture used for V1 acceptance and regression.

---

## V1 Model Company

The canonical V1 mandate models a Slovenian EUR corporate treasury.

Key constraints:

~~~text
Treasury capital:                    €5,000,000
Current unallocated cash:            €5,000,000
Current supplied cash return:        0.00%

Base currency:                       EUR
Minimum useful allocation:           €100,000
Maximum single position:             100%

Target yield:                        3.00%
Target is hard constraint:           No

Capital-preservation priority:       Very high
Liquidity requirement:              High

Allowed currency:                    EUR
Maximum unhedged FX exposure:        0%

Immediate liquidity requirement:     100%
Maximum settlement time:             T+2

Verified corporate access required:  Yes
Review frequency:                    30 days
~~~

The 3% target is a preference, not permission to violate risk, liquidity, currency, accessibility, or evidence requirements.

The current 0% cash return is explicitly supplied by the model-company fixture. It is not inferred from market data and is not a default assumption for other companies.

---

## Historical V1 Opportunity Universe

The canonical production universe contains **14 opportunities** spanning bank products, exchange-traded cash and bond products, direct sovereign bills, institutional money-market products, tokenized products, and DeFi.

At €5 million on 2026-09-03:

~~~text
Recommendation-ready:  2
Needs evidence:         7
Blocked:                5
~~~

### Recommendation-ready

~~~text
French BTF Aug 2027     2.760%
French BTF Mar 2027     2.597%
~~~

### Needs evidence

~~~text
Amundi Smart Overnight
ERNX
Franklin Euro Short Maturity
iShares € Govt Bond 0–1yr
ICASH
German Bubill Jul 2027
German Bubill Aug 2027
~~~

### Blocked

~~~text
Addiko 91–180d Deposit
XEON
BlackRock ICS Euro Liquidity
Spiko EU T-Bills
Aave V3 Base EURC
~~~

Candidate status is not determined by yield alone.

An opportunity can fail recommendation readiness because of known mandate violations, insufficient position-size liquidity, accessibility problems, stale evidence, incomplete risk evidence, incomplete execution-cost evidence, or other explicitly modeled requirements.

---

## Historical V1 €5M Decision

The two recommendation-ready opportunities are:

~~~text
French BTF Aug 2027     2.760%
French BTF Mar 2027     2.597%
~~~

The production return-priority construction therefore selects:

~~~text
€5,000,000 → French BTF Aug 2027
~~~

Expected defensible annual return:

~~~text
2.760%
€137,985
~~~

Against the soft 3.00% target:

~~~text
Shortfall: 0.240 percentage points
Shortfall: €12,015 per year
~~~

The March 2027 French BTF has a modeled defensible return of 2.597%, producing approximately €129,835 annually at €5 million.

The August BTF therefore has an approximately 16.3 bps modeled return advantage over the March BTF at the canonical allocation size.

V1 does not increase risk merely to force the portfolio above the target.

---

## Historical V1 Cash vs Proposed Allocation

The canonical model company currently has:

~~~text
Treasury capital:       €5,000,000
Invested capital:       €0
Unallocated cash:       €5,000,000
Current cash return:    0.000%
Current annual return:  €0
~~~

The proposed allocation produces:

~~~text
Proposed annual return:       €137,985
Incremental annual benefit:   €137,985
Net improvement:              275.970 bps
~~~

The production rebalance materiality policy requires an improvement of 5 bps of treasury capital.

For €5 million:

~~~text
5 bps = €2,500
~~~

The proposed improvement materially exceeds that threshold.

Therefore:

~~~text
Rebalance decision:       rebalance
Decision status:          decision_ready
Final review action:      review_for_rebalance
~~~

Execution remains prohibited until the separate approval boundary is satisfied.

---

## Historical V1 Concentration Diagnostics

The production mandate currently permits a 100% maximum single position.

V1 also evaluates counterfactual concentration limits to understand their economic effect.

### 50% maximum-position diagnostic

~~~text
Positions:               2
Largest position:        50%
Portfolio return:        2.690%
Expected annual return:  €134,485
Cost vs selected:        7.00 bps
~~~

### 40% maximum-position diagnostic

~~~text
Positions:               3
Largest position:        40%
Portfolio return:        2.671%
Expected annual return:  €133,540
Cost vs selected:        8.89 bps
~~~

These are diagnostics only.

The system does not claim that a 40% or 50% maximum position is safer or optimal. Lower concentration does not by itself establish lower treasury risk.

A defensible production concentration policy would require portfolio-level exposure and risk evidence rather than an arbitrary diversification percentage.

---

## Historical V1 Evidence Gaps

V1 does not silently discard an opportunity because its yield is unattractive.

Every non-ready candidate remains classified with explicit blockers and/or evidence requirements.

### ERNX

ERNX currently has a modeled defensible return of approximately 2.620%, but its market-liquidity evidence was observed on 2026-08-21.

As of 2026-09-03 that evidence is 13 days old and exceeds the V1 seven-day market-liquidity freshness requirement.

ERNX is therefore `needs_evidence`, not recommendation-ready.

### German Bubill Jul 2027

The modeled defensible return is approximately 2.547%.

Its market-return and market-liquidity observations date from 2026-08-24 and are stale under the seven-day freshness requirement as of 2026-09-03.

### German Bubill Aug 2027

The modeled defensible return is approximately 2.556%.

Its market-return and market-liquidity observations date from 2026-08-17 and are stale under the seven-day freshness requirement as of 2026-09-03.

### XEON

XEON is economically relevant as an overnight-rate ETF, but the current very-high-capital-preservation mandate rejects its known moderate principal/credit and structural/counterparty risk associated with indirect swap replication.

### Addiko Deposit

The modeled deposit does not satisfy the treasury's 100% immediate-liquidity requirement at the analyzed position size, and additional evidence remains incomplete.

### Amundi Smart Overnight

Potentially relevant, but the current evidence set is insufficient for recommendation-ready status.

### Franklin Euro Short Maturity

Potentially relevant, but available position-size liquidity evidence is not currently sufficient for recommendation-ready status at €5 million.

### iShares € Govt Bond 0–1yr

Potentially relevant, but available position-size liquidity evidence is not currently sufficient for recommendation-ready status at €5 million.

### ICASH

ICASH is part of the production opportunity universe, with Slovenian corporate access modeled through an appropriate Slovenian exchange-member route rather than an assumed IBKR route.

Position-size liquidity and recurring execution/access economics remain insufficient for recommendation-ready status at larger allocations.

### BlackRock ICS Euro Liquidity

Corporate accessibility through the required V1 route has not been sufficiently established.

### Spiko EU T-Bills

Corporate accessibility for the Slovenian d.o.o. has not been sufficiently established.

### Aave V3 Base EURC

The complete Slovenian corporate EUR → EURC → Aave → EUR → corporate-bank operating path has not been verified.

At the canonical €5 million analysis, observed immediate exit liquidity is also insufficient for the mandate.

Live Aave observations may change between runs.

---

## Historical V1 Evidence Freshness

Recommendation readiness depends not only on whether evidence exists but also on whether time-sensitive evidence remains usable as of the analysis date.

Current V1 freshness policy:

~~~text
Market return:          7 days
Market liquidity:       7 days
Benchmark:              3 days
Risk evidence:          30 days
Accessibility:          90 days
Cost evidence:          90 days
~~~

Required evidence that is missing or stale prevents recommendation-ready status.

The engine uses an explicit analysis `as_of` date rather than silently using the system clock.

---

## Historical V1 Evidence Refresh Planning

V1 includes structured evidence-refresh planning.

The refresh layer identifies which production dependencies require attention without embedding live web requests inside portfolio analysis.

As of 2026-09-03, the current stale production refresh items are:

~~~text
ERNX
  - market_liquidity

German Bubill Jul 2027
  - market_return
  - market_liquidity

German Bubill Aug 2027
  - market_return
  - market_liquidity
~~~

Current refresh capability design distinguishes:

~~~text
automatic
manual
supplied
unsupported
~~~

Examples:

- ECB €STR can be retrieved through an automatic source adapter.
- French AFT BTF evidence is maintained as verified source evidence; automatic HTML retrieval was not used for V1 because the official endpoint was not sufficiently deterministic for the production evidence path.
- German Finance Agency evidence is currently maintained manually.
- ERNX market-liquidity evidence is currently maintained manually.
- Company cash economics can be supplied by the company with an observation date.

A refresh action does not manufacture a new observation date. If an official source still contains only an older observation, that evidence remains old.

---

## Historical V1 Slovenian Treasury-Bill Research

V1 includes source and discovery modeling for Slovenian Treasury bills.

Relative to the canonical analysis date of 2026-09-03, the following auctions were scheduled for 2026-09-08:

~~~text
TZ233
SZ163
DZ125
~~~

As of 2026-09-03 they had not yet been auctioned.

Therefore V1 does not manufacture:

- auction yield,
- price,
- issued amount,
- ISIN,
- listing status,
- or secondary-market liquidity.

They remain scheduled future issuance observations rather than canonical production opportunities for the 2026-09-03 decision.

This is intentional evidence discipline, not a missing analytical capability.

---

## Architecture

The architecture follows the treasury decision and evidence lifecycle.

~~~text
SOURCE SYSTEMS
├── ECB
├── Agence France Tresor
├── TradFi market / product sources
├── Tokenized / RWA sources
└── Onchain sources
        ↓
SOURCE ADAPTERS
├── retrieval
├── parsing
├── normalization
└── provenance
        ↓
POSTGRESQL
└── public.market_evidence
        ↓
DBT STAGING
└── analytics_staging.stg_market_evidence
        ↓
DBT MARTS
├── analytics_marts.latest_market_evidence
└── analytics_marts.market_evidence_history
        ↓
WAREHOUSE ADAPTERS
        ↓
NORMALIZED OPPORTUNITY UNIVERSE
        ↓
TREASURY MANDATE
        ↓
ELIGIBILITY
        ↓
POSITION-SIZE ANALYSIS
        ↓
RISK / RETURN / LIQUIDITY
        ↓
EVIDENCE + FRESHNESS GATES
        ↓
PORTFOLIO CONSTRUCTION
        ↓
RECOMMENDATION
        ↓
HUMAN APPROVAL BOUNDARY

[EXECUTION / OPERATIONS OUTSIDE CURRENT SCOPE]
~~~

### Market evidence

`public.market_evidence` is the append-only operational evidence store.

Each record retains:

~~~text
stable evidence ID
instrument / benchmark identity
market and access route where applicable
evidence type
measure
observation timestamp
numeric value and unit
source reference
source name / URL
ingestion run ID
raw normalized source payload
ingestion timestamp
~~~

Stable evidence IDs make retries idempotent.

### dbt transformation layer

dbt transforms raw operational evidence into analytical representations.

Current models include:

~~~text
analytics_staging.stg_market_evidence
analytics_marts.latest_market_evidence
analytics_marts.market_evidence_history
~~~

`latest_market_evidence` resolves the most recent persisted observation for each evidence series.

`market_evidence_history` derives validity intervals from immutable observations so historical evidence remains queryable without mutating previous rows.

The dbt project currently runs 45 data tests covering source constraints, required fields, uniqueness, latest-series correctness, historical validity intervals, and one-current-row-per-series invariants.

### Orchestration

Prefect coordinates the current production pipeline:

~~~text
ingest AFT BTF evidence
        ↓
ingest ECB ESTR evidence
        ↓
dbt build
        ↓
warehouse-backed production decision
~~~

Source-ingestion tasks use retries for transient upstream failures.

### Domain separation

The implementation deliberately separates:

~~~text
INSTRUMENT
What economically owns or generates the return

ACCESS ROUTE
How the corporate treasury can buy or hold it

MARKET / VENUE
Where the instrument is traded or executed

EVIDENCE
What observed fact supports an analytical claim

OPPORTUNITY SNAPSHOT
The normalized state consumed by treasury analytics
~~~

This prevents economic exposure from being confused with brokerage, custody, venue, protocol access, or source evidence.

---

## Core Domain Model

Important V1 entities include:

~~~text
benchmark
instrument
market
access_route
accessibility
opportunity_snapshot
market_observation
risk_observation
risk_assessment
source
treasury_mandate
position_analysis
eligibility_result
evidence_gap
portfolio_candidate
portfolio_construction
portfolio_proposal
recommendation
approval
treasury_state
cash_baseline
allocation_delta
economic_comparison
switching_friction
rebalance_decision
monthly_review
~~~

The system keeps observations, assessments, and decisions separate.

For example:

~~~text
Observed liquidity
        ↓
Position-size liquidity analysis
        ↓
Eligibility / evidence sufficiency
        ↓
Recommendation readiness
~~~

A raw observation does not automatically become an investment conclusion.

---

## Position Size Is a First-Class Input

An opportunity is evaluated as:

~~~text
Opportunity + Treasury Mandate + Position Size
~~~

Position size can affect:

- execution costs,
- commissions,
- slippage,
- market impact,
- entry capacity,
- exit liquidity,
- achievable return,
- and recommendation readiness.

The analytical engine supports arbitrary position sizes.

Diagnostic matrices such as:

~~~text
€100k
€500k
€1m
€2m
€5m
~~~

are regression and research tools.

They are not the production allocation model.

The allocator requires the exact proposed allocation size to have been analyzed upstream before that amount can be allocated.

V1 additionally proves the full production universe can be evaluated at a non-model-company €10 million position size.

---

## Return Model

V1 distinguishes advertised yield from defensible treasury return.

Conceptually:

~~~text
Headline / observed yield
        ↓
product costs
access costs
broker commissions
execution costs
spread / slippage
network costs where relevant
FX / hedging costs where relevant
other modeled friction
        ↓
DEFENSIBLE RETURN
~~~

Risk is not subtracted from return as an arbitrary numerical penalty.

Risk remains a separate decision dimension.

---

## Risk Framework

V1 uses seven risk dimensions:

~~~text
principal_credit
market
liquidity
currency_asset
structural_counterparty
technical
operational_regulatory
~~~

Qualitative levels:

~~~text
very_low
low
moderate
high
very_high
unknown
not_applicable
~~~

Observable evidence remains separate from assessed risk.

For the canonical model-company mandate, very-high capital preservation requires sufficiently supported risk assessments and rejects known risk levels above the permitted tolerance.

Position-aware liquidity is evaluated separately because liquidity depends directly on allocation size.

---

## Entry Capacity Is Not Exit Liquidity

V1 treats these as different questions.

~~~text
ENTRY CAPACITY
Can the treasury deploy €X?

EXIT LIQUIDITY
Can the treasury recover €X within the mandate's required time?
~~~

A market can accept a position without necessarily supporting liquidation of the same position within the required horizon.

This distinction is particularly important for onchain markets and less-liquid products.

---

## Accessibility Is a Hard Constraint

An economically attractive opportunity is not actionable merely because it exists.

For V1:

> No opportunity becomes actionable until both instrument economics and Slovenian-d.o.o. accessibility are sufficiently verified.

Accessibility may depend on:

- jurisdiction,
- legal entity type,
- corporate-account availability,
- brokerage or platform access,
- exact instrument availability,
- venue access,
- custody route,
- and operational feasibility.

Technical accessibility alone is not enough.

---

## Evidence Sufficiency

V1 explicitly represents uncertainty.

An opportunity can be:

~~~text
recommendation_ready
needs_evidence
blocked
~~~

`needs_evidence` is intentionally different from `blocked`.

A potentially attractive opportunity should not be rejected merely because research is incomplete.

Likewise, missing evidence must not be silently treated as evidence of safety.

---

## Portfolio Construction

The production allocator operates on integrated candidate assessments that have already passed the upstream analytical layers.

It does not resize an existing position analysis.

If the allocator wants to allocate €X to an opportunity, that opportunity must first be analyzed at exactly €X.

This prevents a return or liquidity assessment calculated at one position size from being reused incorrectly at another.

For the current mandate, which permits 100% concentration, the canonical production selector:

1. receives the exact freshness-gated production candidate set,
2. identifies recommendation-ready candidates,
3. respects mandate constraints,
4. selects the highest defensible-return candidate,
5. preserves the full candidate set for proposal provenance.

The same canonical 14-candidate set feeds both the production recommendation and the recurring monthly-review path.

V1 does not introduce an opaque optimizer when the current business problem does not require one.

---

## Treasury State and Monthly Review

V1 represents the current treasury separately from the proposed portfolio.

Current state can include:

~~~text
Current positions
Current unallocated capital
Current cash balances
Current cash return evidence
~~~

The monthly-review path evaluates:

~~~text
CURRENT TREASURY
        ↓
CURRENT MANDATE SURVEILLANCE
        ↓
PROPOSED CANONICAL ALLOCATION
        ↓
ALLOCATION DELTA
        ↓
CURRENT vs PROPOSED ECONOMICS
        ↓
SWITCHING FRICTION
        ↓
REBALANCE DECISION
        ↓
MONTHLY REVIEW ACTION
~~~

For the canonical 2026-09-03 model-company state:

~~~text
Mandate surveillance:    compliant
Rebalance decision:      rebalance
Decision status:         decision_ready
Review action:           review_for_rebalance
Review status:           follow_up_required
~~~

---

## Rebalance Materiality

V1 uses an explicit production rebalance policy rather than switching for economically trivial differences.

Current policy:

~~~text
Required net improvement: 5 bps of treasury capital
~~~

For €5 million:

~~~text
€2,500
~~~

Validated cash-return scenarios demonstrate:

~~~text
Current cash 1.50%
→ proposed 2.760%
→ +125.970 bps
→ rebalance

Current cash 2.73%
→ proposed 2.760%
→ +2.970 bps
→ keep_current

Current cash 2.80%
→ proposed 2.760%
→ -4.030 bps
→ keep_current
~~~

The canonical model-company 0% cash return produces a material rebalance decision.

---

## Recommendation and Human Approval

Portfolio construction does not authorize execution.

The decision chain is:

~~~text
Portfolio Construction
        ↓
Portfolio Proposal
        ↓
Recommendation
        ↓
Human Approval
        ↓
[Future execution boundary]
~~~

The canonical V1 state is:

~~~text
Recommendation status:  decision_ready
Recommended action:     submit_for_approval
Approval status:        pending
Authorized allocation:  €0
Execution authorized:   False
~~~

This is an intentional product boundary.

---

## Execution Is Outside V1

V1 does not:

- place broker orders,
- transfer corporate cash,
- interact with brokerage execution APIs,
- sign blockchain transactions,
- manage private keys,
- execute token swaps,
- subscribe to funds automatically,
- perform accounting entries,
- or automatically rebalance live treasury assets.

The platform produces intelligence, recommendations, review decisions, and approval-state outputs.

Actual treasury execution requires separate legal, operational, accounting, custody, authorization, and control design and is intentionally not part of the current product.

---

## Data Sources

V1 uses a combination of authoritative/public sources, normalized research evidence, company-supplied evidence, and live adapters where justified.

Examples include:

- ECB data for €STR,
- official sovereign debt-management publications,
- official issuer and fund documentation,
- public brokerage pricing and access information,
- public market observations,
- company-supplied current cash economics,
- and live onchain state where appropriate.

Source provenance and observation timing matter because market conditions and product terms change.

Live source access is separated from portfolio decision logic. Portfolio analysis consumes normalized observations rather than performing arbitrary live web requests during construction.

---

## Running the Project

### Requirements

- Python
- Git
- Docker / Docker Compose
- internet access for live source adapters
- dependencies in `requirements.txt`

### Local environment

From Git Bash:

~~~bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
~~~

Review `.env` before running the pipeline.

### Start PostgreSQL

~~~bash
docker compose up -d postgres
docker compose ps
~~~

### Start Prefect

In a separate terminal:

~~~bash
source .venv/Scripts/activate
prefect server start
~~~

The local Prefect UI and API are served on port `4200`.

### Run the end-to-end production pipeline

With Prefect running:

~~~bash
./scripts/run_showcase_demo.sh
~~~

The runner:

~~~text
loads the local environment
starts / verifies PostgreSQL
applies the database schema
checks the Prefect API
runs the orchestrated production pipeline
queries the latest warehouse evidence
prints the final repository state
~~~

The Prefect flow itself can also be run directly:

~~~bash
PYTHONPATH=src python -m treasury_intelligence.orchestration.production_pipeline
~~~

### Run source ingestion independently

~~~bash
PYTHONPATH=src python scripts/ingest_aft_btf.py
PYTHONPATH=src python scripts/ingest_ecb_estr.py
~~~

### Run dbt independently

~~~bash
export DBT_POSTGRES_HOST=localhost

dbt build     --project-dir dbt     --profiles-dir dbt
~~~

### Run the warehouse-backed production decision

~~~bash
set -a
source .env
set +a

PYTHONPATH=src python     scripts/inspect_production_5m_recommendation.py
~~~

### Other analytical regressions

The repository retains deterministic analytical inspection scripts for individual domain invariants and historical V1 acceptance scenarios, including:

~~~text
inspect_arbitrary_company_inputs.py
inspect_end_to_end_treasury_decision.py
inspect_monthly_review.py
inspect_freshness_gated_universe.py
inspect_production_evidence_refresh_plan.py
inspect_cash_rebalance_scenarios.py
~~~

These complement the dbt data-quality layer rather than replace it.

---

## Repository Structure

~~~text
treasury-intelligence-platform/
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
├── docs/
│   └── v1_opportunity_universe.md
├── scripts/
│   ├── apply_database_schema.py
│   ├── ingest_aft_btf.py
│   ├── ingest_ecb_estr.py
│   ├── inspect_production_5m_recommendation.py
│   ├── run_showcase_demo.sh
│   └── ... analytical inspection / regression scripts
├── sql/
│   └── 001_create_market_evidence.sql
├── src/
│   └── treasury_intelligence/
│       ├── analytics/
│       ├── mandates/
│       ├── models/
│       ├── orchestration/
│       ├── persistence/
│       ├── policies/
│       └── sources/
├── compose.yaml
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
~~~

The codebase separates source acquisition, persistence, transformation, treasury analytics, policy, and orchestration rather than embedding those concerns in one execution script.

---

## Engineering Philosophy

The core engineering rule is:

> Add technology when a concrete data, analytical, reliability, or operational requirement justifies it.

The project follows this hierarchy:

~~~text
BUSINESS PROBLEM
        ↓
ANALYTICAL REQUIREMENT
        ↓
DATA REQUIREMENT
        ↓
ENGINEERING REQUIREMENT
        ↓
TECHNOLOGY CHOICE
~~~

The analytical V1 began as deterministic Python domain logic.

Infrastructure was added when the system developed concrete requirements for:

~~~text
immutable source evidence
historical observations
idempotent ingestion
shared warehouse-backed inputs
data-quality validation
repeatable transformation
source refresh orchestration
failure visibility
reproducible local infrastructure
~~~

Those requirements led to PostgreSQL, dbt, Prefect, and Docker Compose.

The project still avoids infrastructure that has no current requirement. There is no distributed-processing layer, separate cloud warehouse, dashboard application, or execution system simply for architectural completeness.

Validated progress is committed incrementally so each milestone leaves the repository in a reproducible state.

---

## V1 Acceptance Criteria

V1 is accepted when the system can:

- accept company treasury capital as an analytical input,
- accept current cash economics as supplied evidence,
- represent the canonical €5 million model-company mandate,
- evaluate the relevant production opportunity universe,
- verify or reject corporate accessibility,
- analyze opportunities at arbitrary allocation sizes,
- distinguish entry capacity from exit liquidity,
- estimate defensible return rather than headline yield,
- assess risk across explicit dimensions,
- distinguish insufficient evidence from known blockers,
- enforce evidence freshness,
- identify recommendation-ready candidates,
- construct a mandate-compliant allocation,
- quantify expected portfolio return,
- compare the proposal with current treasury economics,
- compare the result with the target yield,
- evaluate explicit concentration-policy counterfactuals,
- explain why opportunities were selected or excluded,
- maintain current treasury state,
- monitor current holdings against the mandate,
- calculate allocation deltas,
- assess switching friction,
- make an economic rebalance decision,
- produce a recurring monthly-review action,
- generate structured evidence-refresh requirements,
- produce a recommendation,
- require human approval,
- and prevent execution authorization before approval.

The canonical €5 million regression and the €10 million / 1.25% arbitrary-company acceptance fixture satisfy these analytical requirements.

---

## Validation Strategy

V1 uses deterministic inspection/assertion scripts as its acceptance and regression harness.

The repository does not currently include a separate formal unit-test framework.

Important release checks include:

~~~text
inspect_arbitrary_company_inputs.py
inspect_production_5m_recommendation.py
inspect_monthly_review.py
inspect_end_to_end_treasury_decision.py
inspect_freshness_gated_universe.py
inspect_production_evidence_refresh_plan.py
inspect_cash_rebalance_scenarios.py
~~~

The inspection scripts contain executable assertions for the business invariants they validate.

---

## Known Limitations

The current system is intentionally incomplete in several areas.

1. The 14-opportunity universe is representative of the current EUR treasury problem but is not every accessible financial product.
2. Several opportunities remain evidence-incomplete and therefore cannot become recommendation-ready.
3. Production warehouse ingestion is currently implemented for selected official evidence paths, including AFT BTF auction evidence and ECB ESTR; other sources still use older adapters or manually maintained evidence.
4. Some TradFi observations still require manual evidence maintenance rather than deterministic automated retrieval.
5. Live onchain observations can change between runs.
6. Execution costs are modeled from available evidence rather than confirmed live fills.
7. The PostgreSQL/dbt warehouse currently covers the evidence series migrated into the production persistence path; the full opportunity universe has not yet been warehouse-backed.
8. Prefect orchestration is implemented locally, but scheduled deployment / worker infrastructure has not yet been productionized.
9. There is no user-facing application or dashboard.
10. Portfolio-level concentration and correlated-exposure policy is not yet sufficiently modeled to claim that arbitrary diversification limits improve safety.
11. Tax and accounting treatment are not modeled as a complete jurisdiction-specific treasury engine.
12. Live treasury execution is outside the current scope.
13. A recommendation is specific to the stated mandate, treasury state, analysis date, and available evidence and must be regenerated when those inputs change.

These are current system boundaries rather than reasons to add infrastructure without a corresponding requirement.

---

## What Is Already Implemented

Current capabilities include:

### Data ingestion and persistence

- live ECB ESTR retrieval,
- live AFT BTF auction retrieval,
- normalized source adapters,
- stable idempotent evidence IDs,
- append-only PostgreSQL market evidence,
- raw normalized payload retention,
- source provenance,
- ingestion run identifiers,
- historical evidence backfill.

### Transformation and data quality

- dbt source definitions,
- staging transformation,
- latest-evidence mart,
- point-in-time market-evidence history,
- validity intervals,
- source and model tests,
- latest-series correctness tests,
- one-current-row-per-series validation.

### Orchestration and infrastructure

- Prefect production flow,
- retryable source-ingestion tasks,
- dbt orchestration,
- warehouse-backed decision orchestration,
- Docker Compose PostgreSQL,
- reproducible database schema application,
- end-to-end local pipeline runner.

### Treasury intelligence

- treasury-state modeling,
- current cash economics,
- mandate surveillance,
- accessibility analysis,
- arbitrary position-size analysis,
- liquidity analysis,
- return economics,
- risk assessment,
- evidence sufficiency,
- evidence freshness,
- evidence dependency classification,
- structured evidence-refresh planning,
- production-universe freshness gating,
- portfolio construction,
- allocation deltas,
- current-versus-proposed economics,
- switching-friction analysis,
- rebalance materiality,
- recurring monthly-review decisions,
- recommendation generation,
- human approval boundaries,
- arbitrary-company treasury-size and cash-return inputs.

The production decision layer can consume persisted warehouse evidence and is allowed to return a valid `hold_unallocated` decision when no candidate satisfies the current evidence and freshness gates.

---

## Potential Future Problems

Further development should remain requirement-driven.

Current likely areas include:

- migrate additional production opportunity evidence into the PostgreSQL/dbt path,
- broaden deterministic official-source ingestion,
- productionize Prefect scheduling / deployment,
- add pipeline-run and source-freshness observability,
- extend warehouse-backed point-in-time decision inputs,
- broaden EUR opportunity coverage,
- support additional company mandates and jurisdictions,
- persist recommendation and review history,
- improve portfolio-level correlated-exposure modeling,
- add evidence-backed concentration policy,
- extend tax/accounting-aware return analysis,
- add a persistent approval workflow,
- integrate with company treasury/accounting systems,
- and, only if intentionally added later, controlled execution infrastructure.

These are not automatically required in sequence. The next implementation should be chosen by the most valuable unresolved product or data requirement.

---

## Disclaimer

This repository is a research and decision-intelligence project.

It does not constitute investment, legal, tax, accounting, or financial advice.

Market data, yields, liquidity, product terms, accessibility, and risk conditions can change.

Any real corporate treasury decision requires appropriate professional review, current source verification, internal authorization, and appropriate execution controls.
