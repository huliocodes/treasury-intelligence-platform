# Treasury Intelligence Platform

Decision intelligence for allocating EUR corporate treasury capital across traditional, tokenized, and onchain yield opportunities.

The V1 system answers a concrete treasury question:

> A Slovenian d.o.o. has €5 million of excess cash today. Given its capital-preservation, EUR/FX, liquidity, accessibility, and return requirements, how should that €5 million be allocated across the relevant opportunity universe?

This is not a generic yield dashboard.

The platform evaluates whether an opportunity is actually usable by the treasury, analyzes it at the intended position size, estimates a defensible return after relevant costs, evaluates risk and liquidity, constructs a portfolio, explains the decision, and stops at human approval.

Execution is intentionally outside V1.

---

## V1 Status

**V1 is feature-complete and accepted.**

Final regression:

```text

Opportunity universe:       9

Position-size test cases:   45

Recommendation-ready:       15

Needs evidence:              5

Blocked:                    25

```

At the model company's actual €5 million treasury size:

```text

Opportunities:               9

Recommendation-ready:        3

Needs evidence:              1

Blocked:                     5

```

Current recommendation:

```text

Treasury capital:       €5,000,000

Selected opportunity:  ERNX

Allocation:             €5,000,000

Allocation percentage: 100.00%

Defensible return:      2.620%

Expected annual return: €131,000

Target yield:           3.000%

Target gap:             0.380 percentage points

Annual target gap:      €19,000

Recommendation:         submit_for_approval

Approval:               pending

Authorized allocation: €0

Execution authorized:  False

```

The recommendation reflects the evidence and market observations encoded or retrieved by the current V1 implementation. It is not a permanent investment recommendation and should be re-evaluated when market data, product terms, accessibility, liquidity, risk evidence, or the treasury mandate changes.

---

## Business Problem

Corporate cash management is not simply a search for the highest advertised yield.

A EUR-based company may have €1 million, €5 million, €20 million, or substantially more in excess capital while still needing to:

- preserve principal,
- maintain high liquidity,
- avoid meaningful FX exposure,
- recover capital for operating requirements,
- understand the risks required to earn incremental yield,
- determine whether an opportunity is actually accessible,
- estimate realistic return after access and execution costs,
- determine whether the intended position size can enter and exit,
- allocate capital across multiple opportunities when justified,
- and periodically reconsider the allocation as conditions change.

The core analytical unit is therefore not:

> "What product has the highest yield?"

It is:

> "What return is defensible for this treasury, through this access route, at this allocation size, subject to this mandate?"

---

## V1 Model Company

The production V1 mandate models a Slovenian EUR corporate treasury.

Key constraints:

```text

Treasury capital:                    €5,000,000

Base currency:                       EUR

Minimum useful allocation:          €100,000

Maximum single position:            100%

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

```

The 3% target is a preference, not permission to violate the risk, liquidity, currency, or accessibility requirements.

---

## V1 Opportunity Universe

V1 evaluates nine representative opportunities spanning bank products, exchange-traded cash/bond products, direct sovereign bills, institutional money-market products, tokenized products, and DeFi.

| Opportunity | Category | €5M V1 status | Defensible return |

|---|---|---:|---:|

| Addiko 91–180d Deposit | Bank deposit | Blocked | 1.500% |

| XEON | Overnight-rate ETF | Blocked | 1.973% |

| Amundi Smart Overnight | Cash / overnight product | Needs evidence | 2.088% |

| ERNX | Short-duration bond ETF | Recommendation-ready | 2.620% |

| French BTF | Sovereign Treasury bill | Recommendation-ready | ~2.575% |

| German Bubill | Sovereign Treasury bill | Recommendation-ready | ~2.547% |

| BlackRock ICS Euro Liquidity | Institutional liquidity product | Blocked | 2.210% |

| Spiko EU T-Bills | Tokenized Treasury-bill product | Blocked | 2.090% |

| Aave V3 Base EURC | Onchain lending | Blocked | Live / variable |

Aave observations are retrieved from live market state and therefore change between runs.

The detailed V1 universe research is documented in:

```text

docs/v1_opportunity_[universe.md](http://universe.md)

```

---

## Current €5M Decision

Three opportunities currently reach recommendation-ready status under the V1 mandate:

```text

ERNX           2.620%

French BTF     ~2.575%

German Bubill  ~2.547%

```

The return-priority allocator therefore selects:

```text

€5,000,000 → ERNX

```

Expected defensible annual return:

```text

2.620%

€131,000

```

Against the soft 3.00% target:

```text

Shortfall: 0.380 percentage points

Shortfall: approximately €19,000 per year

```

V1 does not increase risk merely to force the portfolio above the target.

---

## Why ERNX?

Among the opportunities that currently satisfy the mandate and have sufficient evidence, ERNX has the highest defensible modeled return at the €5 million position size.

At €5 million:

```text

ERNX           2.620%

French BTF     ~2.575%

German Bubill  ~2.547%

```

Approximate ERNX return advantage:

```text

vs French BTF:     ~4.5 bps

vs German Bubill:  ~7.3 bps

```

This selection is the output of the current mandate and evidence set.

It does not assert that ERNX is universally superior to sovereign bills or that a single-position portfolio is universally optimal.

---

## Concentration Diagnostics

The production mandate currently permits a 100% maximum single position.

V1 also tests counterfactual concentration limits to show their economic effect.

### 50% maximum position

```text

Positions:               2

Largest position:        50%

Portfolio return:        ~2.597%

Expected annual return:  ~€129,860

Cost vs selected:

~2.28 bps

~€1,140 per year

```

### 40% maximum position

```text

Positions:               3

Largest position:        40%

Portfolio return:        ~2.587%

Expected annual return:  ~€129,340

Cost vs selected:

~3.32 bps

~€1,660 per year

```

These are diagnostics only.

The system does **not** claim that a 40% or 50% maximum position is safer or optimal. A defensible portfolio-level concentration policy would require additional exposure and risk evidence.

---

## Why Opportunities Are Excluded

V1 does not silently discard an opportunity because its yield is unattractive.

Every non-ready candidate remains classified with explicit blockers and/or evidence requirements.

Examples:

### XEON

Economically attractive as an overnight-rate product, but the current very-high-capital-preservation mandate rejects its known moderate principal/credit and structural/counterparty risk associated with indirect swap replication.

### Amundi Smart Overnight

Potentially relevant, but the current evidence set is insufficient for recommendation-ready status.

### Addiko Deposit

The modeled product does not satisfy the treasury's immediate-liquidity requirement and additional risk/execution evidence remains incomplete.

### BlackRock ICS Euro Liquidity

Corporate accessibility through the required V1 route has not been sufficiently established, and additional evidence remains outstanding.

### Spiko EU T-Bills

Corporate accessibility for the Slovenian d.o.o. has not been sufficiently established, and additional evidence remains outstanding.

### Aave V3 Base EURC

The corporate EUR → EURC → Aave → EUR → corporate bank operating path has not been verified for the Slovenian d.o.o.

The €5 million position also exceeds currently observed immediate exit liquidity in the modeled market.

The exact Aave APY and liquidity coverage are live observations and may change between runs.

---

## Architecture

The V1 architecture follows the business decision rather than a predetermined technology stack.

```text

MARKET DATA

├── Reference rates

├── TradFi

├── Tokenized / RWA

└── DeFi

        ↓

NORMALIZED OPPORTUNITY UNIVERSE

        ↓

TREASURY MANDATE

        ↓

ELIGIBILITY

        ↓

POSITION-SIZE ANALYSIS

        ↓

RISK / RETURN / LIQUIDITY ANALYSIS

        ↓

PORTFOLIO CONSTRUCTION

        ↓

RECOMMENDATION

        ↓

DECISION EXPLANATION

        ↓

HUMAN APPROVAL

        ↓

[EXECUTION OUTSIDE V1]

```

The implementation deliberately separates:

```text

INSTRUMENT

What economically owns or generates the return

ACCESS ROUTE

How the corporate treasury can buy or hold it

MARKET / VENUE

Where the instrument is traded or executed

```

This prevents economic exposure from being confused with brokerage, custody, venue, or protocol access.

---

## Core Domain Model

Important V1 entities include:

```text

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

```

The system keeps observations, assessments, and decisions separate.

For example:

```text

Observed liquidity

        ↓

Position-size liquidity analysis

        ↓

Eligibility / evidence sufficiency

        ↓

Recommendation readiness

```

A raw observation does not automatically become an investment conclusion.

---

## Position Size Is a First-Class Input

An opportunity is not analyzed only once.

The platform evaluates:

```text

Opportunity + Treasury Mandate + Position Size

```

Position size can affect:

- execution costs,
- commissions,
- slippage,
- market impact,
- entry capacity,
- exit liquidity,
- achievable return,
- and recommendation readiness.

The final system supports arbitrary allocation sizes.

The standard matrix:

```text

€100k

€500k

€1m

€2m

€5m

```

exists only as a regression and diagnostic tool.

It is **not** the allocation model.

The portfolio allocator can request arbitrary position sizes and requires those exact sizes to be analyzed upstream before they can be allocated.

---

## Return Model

V1 distinguishes advertised yield from defensible treasury return.

Conceptually:

```text

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

```

Risk is not subtracted from return as an arbitrary numerical penalty.

Risk remains a separate decision dimension.

---

## Risk Framework

V1 uses seven risk dimensions:

```text

principal_credit

market

liquidity

currency_asset

structural_counterparty

technical

operational_regulatory

```

Qualitative levels:

```text

very_low

low

moderate

high

very_high

unknown

not_applicable

```

Observable evidence remains separate from assessed risk.

For the current model-company mandate, very-high capital preservation requires sufficiently supported risk assessments and rejects known risk levels above the permitted tolerance.

Position-aware liquidity is evaluated separately because liquidity depends directly on allocation size.

---

## Entry Capacity Is Not Exit Liquidity

V1 treats these as different questions.

```text

ENTRY CAPACITY

Can the treasury deploy €X?

EXIT LIQUIDITY

Can the treasury recover €X within the mandate's

required time?

```

A market can accept a position without necessarily supporting immediate liquidation of the same position.

This distinction is particularly important for onchain markets and less-liquid products.

---

## Accessibility Is a Hard Constraint

An economically attractive opportunity is not actionable merely because it exists.

For V1:

> No opportunity enters the actionable universe until both instrument economics and Slovenian-d.o.o. accessibility are sufficiently verified.

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

```text

recommendation_ready

needs_evidence

blocked

```

`needs_evidence` is intentionally different from `blocked`.

A potentially attractive opportunity should not be rejected merely because research is incomplete.

Likewise, missing evidence should not be silently treated as evidence of safety.

---

## Portfolio Construction

The allocator operates on integrated portfolio candidates that have already passed the upstream analytical layers.

It does not resize an existing analysis.

If the allocator wants to allocate €1.75 million to an opportunity, that opportunity must first be analyzed at exactly €1.75 million.

This invariant prevents a return or liquidity assessment calculated at one position size from being reused incorrectly at another.

The current V1 allocator is deterministic and mandate-faithful:

1. identify recommendation-ready opportunities,
2. analyze the exact required allocation sizes,
3. respect mandate constraints,
4. prioritize the highest defensible return among eligible candidates,
5. preserve unallocated capital if the mandate prevents full deployment.

V1 does not introduce an opaque portfolio optimizer when the current business problem does not require one.

---

## Recommendation and Human Approval

Portfolio construction does not authorize execution.

The decision chain is:

```text

Portfolio Construction

        ↓

Portfolio Proposal

        ↓

Recommendation

        ↓

Human Approval

        ↓

Execution Authorization

```

The accepted V1 state is:

```text

Recommendation status:  decision_ready

Recommended action:     submit_for_approval

Approval status:        pending

Authorized allocation:  €0

Execution authorized:   False

```

This is an intentional product boundary.

---

## Execution Is Outside V1

V1 does not:

- place broker orders,
- transfer corporate cash,
- interact with a brokerage API,
- sign blockchain transactions,
- manage private keys,
- execute token swaps,
- subscribe to funds,
- perform accounting entries,
- or automatically rebalance live treasury assets.

The platform produces decision intelligence.

Actual treasury execution requires separate legal, operational, accounting, custody, authorization, and control design.

---

## Data Sources

V1 uses a combination of authoritative/public sources and normalized research evidence.

Examples include:

- ECB data for €STR,
- official issuer and fund documentation,
- sovereign debt-management publications,
- public brokerage pricing and access information,
- public market observations,
- and live onchain state where appropriate.

Source provenance and observation timing matter because market conditions and product terms change.

---

## Running the Project

### Requirements

- Python
- Git
- internet access for live source adapters
- dependencies in `requirements.txt`

Current Python dependencies:

```text

requests>=2.32,<3

web3>=7,<8

```

### Create a virtual environment

From Git Bash:

```bash

python -m venv .venv

source .venv/Scripts/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

```

### Run the end-to-end €5M decision

```bash

PYTHONPATH=src python \

  scripts/inspect_end_to_end_treasury_[decision.py](http://decision.py)

```

This runs the production V1 decision path and prints:

- mandate,
- real €5M opportunity-universe status,
- selected allocation,
- ready-opportunity comparison,
- target shortfall,
- concentration diagnostics,
- non-ready opportunity blockers,
- evidence requirements,
- recommendation status,
- approval status,
- and execution authorization.

### Run the position-size matrix

```bash

PYTHONPATH=src python \

  scripts/inspect_universe_position_[matrix.py](http://matrix.py)

```

The V1 regression matrix analyzes nine opportunities at:

```text

€100k

€500k

€1m

€2m

€5m

```

Expected structural summary:

```text

Opportunity count:       9

Position analyses:       45

Recommendation-ready:    15

Needs evidence:           5

Blocked:                 25

```

Live observations such as Aave APY and liquidity can change between runs without representing a regression failure.

### Run the allocator inspection

```bash

PYTHONPATH=src python \

  scripts/inspect_return_priority_[allocation.py](http://allocation.py)

```

Expected model-company structure:

```text

Treasury capital:             €5,000,000

Maximum single position:      100%

Construction status:          valid_allocation

Allocated capital:            €5,000,000

Unallocated capital:          €0

Portfolio defensible return:  2.620%

Target yield gap:             0.380 percentage points

```

---

## Repository Structure

```text

treasury-intelligence-platform/

├── docs/

│   └── v1_opportunity_[universe.md](http://universe.md)

├── scripts/

│   ├── inspect_end_to_end_treasury_[decision.py](http://decision.py)

│   ├── inspect_universe_position_[matrix.py](http://matrix.py)

│   ├── inspect_return_priority_[allocation.py](http://allocation.py)

│   └── ... analytical inspection / regression scripts

├── src/

│   └── treasury_intelligence/

│       ├── analytics/

│       ├── mandates/

│       ├── models/

│       └── sources/

├── .gitignore

├── [README.md](http://README.md)

└── requirements.txt

```

The project currently uses Python modules and inspection scripts directly.

There is intentionally no database, dbt project, Docker deployment, cloud warehouse, orchestration platform, or UI in V1.

---

## Engineering Philosophy

The core engineering rule is:

> Add technology only when the project develops a problem that the technology solves.

The project therefore follows this hierarchy:

```text

BUSINESS PROBLEM

        ↓

ANALYTICAL REQUIREMENT

        ↓

DATA REQUIREMENT

        ↓

ENGINEERING SOLUTION

        ↓

TECHNOLOGY CHOICE

```

V1 did not require a database, warehouse, dbt, Docker, orchestration framework, distributed processing system, or dashboard to answer its core business question.

Those technologies should be introduced only when a later product requirement creates a concrete need for them.

---

## V1 Acceptance Criteria

V1 is accepted when the system can:

- represent the €5 million model-company treasury mandate,
- evaluate the relevant opportunity universe,
- verify or reject corporate accessibility,
- analyze opportunities at arbitrary allocation sizes,
- distinguish entry capacity from exit liquidity,
- estimate defensible return rather than headline yield,
- assess risk across explicit dimensions,
- distinguish insufficient evidence from known blockers,
- identify recommendation-ready candidates,
- construct a mandate-compliant €5 million allocation,
- quantify expected portfolio return,
- compare the result with the target yield,
- evaluate explicit concentration-policy counterfactuals,
- explain why opportunities were selected or excluded,
- produce a recommendation,
- require human approval,
- and prevent execution authorization before approval.

The final V1 regression satisfies these conditions.

---

## Known V1 Limitations

V1 is intentionally narrow.

Current limitations include:

1. The opportunity universe is representative rather than exhaustive.
2. Some products remain research-incomplete and therefore cannot become recommendation-ready.
3. Some market observations are static research inputs rather than continuously refreshed feeds.
4. Live onchain observations can change between runs.
5. Execution costs are modeled from available evidence rather than confirmed live fills.
6. The system does not yet maintain a production historical data store.
7. The system does not automatically refresh all TradFi product evidence.
8. Portfolio-level concentration and correlated-exposure policy is not yet sufficiently modeled to claim that arbitrary diversification limits improve safety.
9. Tax and accounting treatment are not modeled as a full jurisdiction-specific treasury engine.
10. Execution and operational implementation are outside V1.
11. The current recommendation is specific to the encoded model-company mandate and evidence set.
12. A recommendation must be regenerated when relevant market conditions, product terms, evidence, accessibility, or mandate constraints change.

These are boundaries of the current product, not reasons to add infrastructure without a corresponding business requirement.

---

## Potential V2 Problems

V2 should begin only when a concrete business requirement justifies reopening development.

Possible future problems include:

- automated refresh of market and product evidence,
- persistent historical observations,
- monthly treasury review,
- change detection,
- recommendation drift,
- treasury-state ingestion,
- rebalance analysis,
- richer portfolio-level exposure modeling,
- concentration-policy research,
- additional EUR opportunity classes,
- multi-company mandates,
- additional jurisdictions,
- tax/accounting-aware return analysis,
- decision history and auditability,
- approval workflows,
- and eventually controlled execution infrastructure.

These are not automatically part of V2.

The next architecture should be chosen only after selecting the next business problem.

---

## Disclaimer

This repository is a research and decision-intelligence project.

It does not constitute investment, legal, tax, accounting, or financial advice. Market data, yields, liquidity, product terms, accessibility, and risk conditions can change. Any real corporate treasury decision requires appropriate professional review, current source verification, internal authorization, and execution controls.