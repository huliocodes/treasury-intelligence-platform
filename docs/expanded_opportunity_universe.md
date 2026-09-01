# Expanded Opportunity Universe

## Purpose

Treasury Intelligence Platform V1 proved that the decision engine can evaluate a corporate treasury mandate, analyze opportunities at arbitrary position sizes, construct a portfolio, explain the decision, and stop at human approval.

The next product problem is opportunity coverage.

The initial nine-opportunity universe is sufficient to validate the analytical architecture but is not broad enough to establish reasonable confidence that the best relevant opportunity available to the treasury has been identified.

The purpose of the expanded opportunity universe is therefore:

> Systematically discover the reasonably comprehensive set of liquid yield opportunities relevant to a conservative EUR corporate treasury, determine which are realistically accessible to a Slovenian d.o.o., prioritize the economically relevant candidates for deeper research, and run sufficiently researched opportunities through the existing position-size and portfolio decision engine.

The objective is not to maximize the number of products.

The objective is to reduce the probability that the treasury recommendation misses a materially superior relevant opportunity.

---

## Model Treasury

The primary V1.1 discovery mandate remains the existing model company:

- Slovenian d.o.o.

- EUR base currency

- €5,000,000 treasury capital

- approximately €100,000 minimum useful allocation

- 3% target yield, soft constraint

- very high capital-preservation priority

- high liquidity requirement

- 0% unhedged FX exposure

- 100% immediate liquidity requirement

- maximum T+2 settlement

- verified corporate access required

- approximately monthly review

Discovery may include opportunities that ultimately fail these constraints.

Failure is useful information when the reason is preserved.

---

## Core Question

The expanded universe should improve the answer to:

> A Slovenian d.o.o. has €5 million of excess cash today. Given its capital-preservation, EUR/FX, liquidity, accessibility, and return requirements, how should that €5 million be allocated across the reasonably comprehensive relevant opportunity universe?

---

## Universe Philosophy

The universe should be broad enough to challenge the current recommendation.

It should not be artificially restricted to products already known to the project.

It should also not include every financial instrument in existence.

A candidate belongs in discovery when there is a plausible economic reason that a conservative EUR corporate treasury might consider it.

The process is:

```text

DISCOVERY UNIVERSE

        ↓

RELEVANCE SCREEN

        ↓

ACCESSIBILITY SCREEN

        ↓

PRELIMINARY ECONOMIC SCREEN

        ↓

RESEARCH UNIVERSE

        ↓

FULL POSITION-SIZE ANALYSIS

        ↓

RECOMMENDATION-READY UNIVERSE

        ↓

PORTFOLIO CONSTRUCTION

```

Discovery does not imply recommendation.

---

## Opportunity Taxonomy

### 1. Bank Cash and Deposits

Examples:

- interest-bearing corporate current accounts

- overnight deposits

- call deposits

- notice deposits

- term deposits

- negotiated corporate deposits

Research should include Slovenian banks and relevant EU banks where corporate access by a Slovenian legal entity is realistic.

---

### 2. Money-Market Funds

Examples:

- EUR government liquidity funds

- public-debt money-market funds

- LVNAV funds

- VNAV funds

- institutional EUR liquidity funds

- treasury cash-management funds

Relevant institutional share classes should be considered where minimum subscription and corporate access are compatible with the treasury.

---

### 3. Cash and Money-Market ETFs

Examples:

- €STR-linked ETFs

- overnight-rate ETFs

- money-market ETFs

- cash-management ETFs

Both physical and synthetic structures may be discovered.

Structure must later be reflected in risk assessment.

---

### 4. Short-Duration Bond ETFs

Examples:

- ultrashort EUR bond ETFs

- 0–1 year government ETFs

- 0–1 year investment-grade corporate ETFs

- short-duration aggregate ETFs

- floating-rate bond ETFs

- enhanced-cash bond ETFs

Duration, credit exposure, liquidity, wrapper risk, and realistic execution costs must eventually be assessed.

---

### 5. Direct Sovereign Debt

Examples:

- German Bubills

- French BTFs

- Dutch DTCs

- Belgian Treasury Certificates

- Austrian Treasury bills

- Finnish Treasury bills

- other appropriate EUR sovereign bills

- short-dated EUR government bonds

Individual securities should be treated as distinct opportunities when maturity, yield, liquidity, or credit exposure differs materially.

---

### 6. Direct High-Grade Debt

Possible categories:

- supranational debt

- agency debt

- covered bonds

- very short-duration investment-grade corporate bonds

These opportunities should enter deeper research only when their incremental return plausibly compensates for their additional risk and complexity.

---

### 7. Tokenized / Real-World-Asset Products

Examples:

- tokenized Treasury bills

- tokenized government-bond funds

- tokenized money-market funds

- tokenized deposits

- tokenized cash-management products

- institutional RWA funds

- sufficiently relevant tokenized credit products

Headline yield alone is insufficient.

Corporate eligibility, jurisdiction, onboarding, custody, redemption, settlement, underlying assets, token structure, and access from Slovenia must be investigated.

---

### 8. DeFi Lending

Potential protocols include:

- Aave

- Morpho

- Spark

- other sufficiently credible lending protocols

The opportunity is not the protocol name alone.

A lending opportunity should ultimately identify:

```text

protocol

chain

asset

market or vault

return source

liquidity

position capacity

dependencies

```

For example:

```text

Aave V3

→ Base

→ EURC

→ supply market

```

is a different opportunity from another Aave asset or chain.

---

### 9. DeFi Fixed / Term Yield

Potential structures include:

- Pendle principal tokens

- fixed-rate lending markets

- maturity-based yield products

- other transparent term-yield structures

For Pendle-like products, the actual opportunity must identify:

- underlying yield-bearing asset

- principal token

- maturity

- entry price

- implied return

- redemption mechanics

- exit liquidity

- underlying protocol dependencies

- smart-contract dependencies

- chain

- corporate access path

Advertised APY is not sufficient.

---

### 10. DeFi Cash / Stablecoin Strategies

Possible candidates include:

- protocol-native savings products

- stablecoin savings rates

- yield-bearing stable assets

- transparent overcollateralized savings mechanisms

- other sufficiently liquid cash-like onchain strategies

EUR-denominated exposure is preferred.

USD-denominated opportunities do not satisfy the production mandate merely because their nominal yield is higher.

FX exposure must remain explicit.

---

### 11. Other Treasury Alternatives

Discovery may identify opportunities that do not fit the initial taxonomy.

A new category should be added only when the economic structure is materially different from existing categories.

The taxonomy should follow the opportunity universe rather than force every product into an inappropriate category.

---

## Opportunity Identity

Every opportunity should be understandable without specialist knowledge of its ticker, ISIN, token symbol, or protocol.

Minimum identity fields:

```text

key

display_name

full_name

ticker_or_symbol

isin_or_identifier

provider_or_issuer

category

subcategory

```

---

## Human-Readable Description

Every opportunity should eventually answer three questions.

### What is it?

A short description understandable by a business owner or CFO.

Example:

```text

ERNX — iShares € Ultrashort Bond UCITS ETF

A diversified ETF holding very short-duration,

investment-grade EUR bonds.

```

### What does the treasury economically own or fund?

This should describe the actual economic exposure rather than the product label.

Examples:

```text

German Bubill:

Direct short-term obligation of the Federal Republic

of Germany.

ERNX:

Portfolio of short-duration investment-grade EUR debt.

Aave EURC:

EURC supplied into an overcollateralized onchain

lending market.

Pendle principal token:

Principal claim on an underlying yield-bearing asset

at a defined maturity.

```

### Where does the return come from?

Examples:

```text

Bank deposit:

Interest paid by the bank.

Government bill:

Purchase discount converging to par at maturity.

Bond ETF:

Underlying bond income and price movement less fund costs.

DeFi lending:

Interest paid by borrowers.

Pendle principal token:

Difference between acquisition price and maturity

redemption value, subject to the underlying structure.

```

These descriptions are part of risk understanding, not merely presentation.

---

## Preliminary Discovery Fields

A discovered opportunity should capture as many of the following fields as can be supported.

Unknown values should remain unknown.

### Identity

```text

key

display_name

full_name

ticker_or_symbol

isin_or_identifier

provider_or_issuer

category

subcategory

```

### Understanding

```text

short_description

economic_description

return_source

```

### Preliminary Economics

```text

currency

headline_yield_pct

yield_type

yield_as_of

fees_pct

maturity_date

duration

variable_or_fixed

```

### Preliminary Access

```text

jurisdiction

possible_access_route

corporate_access_status

slovenian_doo_access_status

```

### Preliminary Liquidity

```text

liquidity_type

redemption_or_settlement

lockup

market_or_fund_size

```

### Risk Identity

```text

economic_exposure

principal_obligor

wrapper_or_structure

major_dependency

```

### Source

```text

primary_source

source_date

```

### Discovery Decision

```text

discovery_status

screening_reason

research_priority

```

---

## Discovery Status

Discovery status should remain simpler than full recommendation status.

Suggested values:

```text

discovered

screened_out

research_candidate

access_unknown

access_blocked

```

These are research-workflow states.

They must not replace the existing downstream eligibility or recommendation statuses.

---

## Research Priority

Suggested research-priority values:

```text

high

medium

low

```

High priority should generally mean:

- plausible access,

- mandate relevance,

- potentially competitive return,

- meaningful capacity,

- and a realistic chance of affecting the €5M allocation.

Low priority does not necessarily mean low quality.

It means deeper research is currently unlikely to change the treasury decision.

---

## Accessibility Principle

Accessibility remains a hard V1.1 constraint.

> No opportunity enters the actionable universe until both instrument economics and Slovenian-d.o.o. accessibility are sufficiently verified.

Discovery may contain inaccessible or uncertain products.

Recommendation-ready status may not.

Technical access alone is insufficient.

Research should distinguish:

```text

product exists

product accepts European investors

product accepts corporate investors

product accepts Slovenian corporate investors

treasury has a realistic operational access route

```

These are not equivalent statements.

---

## Position-Size Principle

Discovery-level headline yield is not the final return.

Any candidate promoted into full analysis must eventually be evaluated at arbitrary position size through the existing position-analysis architecture.

The standard:

```text

€100k

€500k

€1m

€2m

€5m

```

matrix remains a diagnostic tool.

Final portfolio allocations may use arbitrary sizes.

---

## Liquidity Principle

Entry capacity and exit liquidity remain separate.

```text

ENTRY CAPACITY != EXIT LIQUIDITY

```

Discovery may use preliminary liquidity indicators.

Recommendation readiness requires position-aware liquidity analysis sufficient for the mandate.

---

## Return Principle

The platform compares defensible return rather than advertised yield.

Conceptually:

```text

headline yield

- product costs

- access costs

- execution costs

- commissions

- spread / slippage

- network costs

- FX / hedging costs where relevant

- other material friction

=

defensible return

```

Risk remains separate from return.

---

## Source Standard

Primary and authoritative sources should be preferred where practical.

Examples:

- issuer documentation

- fund-manager documentation

- government debt-management agencies

- central banks

- official protocol data

- official smart-contract state

- official platform eligibility documentation

- official fee schedules

Aggregators may assist discovery.

They should not automatically become the final evidence source for recommendation-critical claims.

---

## Expansion Success Criterion

Universe expansion is successful when the project can reasonably defend that:

1. the major relevant opportunity categories have been systematically searched;

2. material candidate products within those categories have been identified;

3. obvious mandate mismatches have been screened without unnecessary deep research;

4. corporate accessibility has been investigated before an opportunity becomes actionable;

5. economically competitive candidates have been promoted into the existing full analytical pipeline;

6. arbitrary position-size analysis remains intact;

7. the expanded universe can be passed into the existing portfolio decision system;

8. the €5M recommendation is rerun against the broader universe; and

9. the resulting recommendation can explain both what each material opportunity is and why it was selected, excluded, blocked, or left awaiting evidence.

The target is not a predetermined number of opportunities.

The target is credible coverage of the relevant opportunity universe.

---

## Engineering Rule

Universe expansion does not automatically justify new infrastructure.

The existing rule remains:

> Add technology only when the project develops a problem that the technology solves.

If systematic discovery reveals that hand-maintained opportunity definitions have become the bottleneck, that will create a legitimate engineering requirement.

Until then:

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

---

## Milestone 13 Sequence

### 13A — Taxonomy and Discovery Specification

Define:

- relevant opportunity categories,

- discovery fields,

- human-readable descriptions,

- screening states,

- accessibility requirements,

- and research-priority rules.

### 13B — Systematic Market Discovery

Search each category for real current opportunities.

Produce a broad discovery universe before implementing large-scale production changes.

### 13C — Relevance and Accessibility Screen

Determine:

- which opportunities plausibly fit the mandate,

- which are accessible,

- which are blocked,

- and which require access evidence.

### 13D — Research Prioritization

Rank candidates for deeper research based on their probability of materially affecting the treasury allocation.

### 13E — Full Candidate Analysis

Promote high-value candidates into the existing:

```text

normalized opportunity

→ arbitrary position analysis

→ liquidity

→ eligibility

→ risk

→ evidence sufficiency

→ defensible return

→ portfolio candidate

```

pipeline.

### 13F — Expanded €5M Decision

Run the existing portfolio system across the sufficiently researched expanded universe.

Compare the result with the V1.0.0 benchmark:

```text

ERNX

€5,000,000

2.620%

€131,000 expected annual return

```

The purpose is to determine whether broader market coverage changes the recommended allocation and, either way, to increase confidence in the decision.