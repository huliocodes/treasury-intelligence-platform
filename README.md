# # Treasury Intelligence Platform

Data and decision infrastructure for corporate treasury allocation across traditional, tokenized, and onchain markets.

## Business Problem

A EUR-based corporate treasury may have €1 million, €5 million, €20 million, or substantially more in excess capital available for deployment.

The treasury does not need to allocate all capital to one opportunity. Individual allocations may begin around €50,000–€100,000 and scale upward depending on market capacity, liquidity, risk, and expected return.

The treasury wants to prioritize:

- capital preservation
- high liquidity
- minimal or no FX exposure
- minimal lockup
- attractive yield relative to the EUR cash benchmark
- the ability to recover capital for operating needs
- periodic review and reallocation as market conditions change

An initial target such as 3–5% is a preference, not a hard eligibility threshold.

The platform should show what additional risk must be accepted to earn additional yield.

## Core Question

Given a EUR corporate treasury mandate:

> Which currently available opportunities are investable at a specified allocation size, what can that allocation realistically earn, how liquid is it, what risks are being accepted, and how much incremental return is being earned relative to the EUR cash benchmark?

## Product Principle

This is not a generic DeFi yield dashboard.

The platform follows the treasury problem across markets.

Potential opportunity classes include:

- EUR money-market funds
- short-duration government instruments
- enhanced cash products
- tokenized money-market funds
- tokenized government debt
- onchain lending markets
- EUR stablecoin lending
- other liquid institutional-grade opportunities
- higher-risk strategies in later versions

## Treasury Mandate

Treasury size is an input, not a hardcoded assumption.

Example inputs may include:

- total treasury capital
- base currency
- minimum useful allocation
- target yield
- liquidity requirement
- risk tolerance

A typical initial mandate may use:

- base currency: EUR
- treasury capital: €1M–€20M+
- minimum useful allocation: approximately €50k–€100k
- target yield: approximately 3–5%
- liquidity preference: high
- risk preference: conservative

## V1 Decision Model

The platform separates three concepts.

### Benchmark

The initial EUR cash benchmark is the ECB euro short-term rate (€STR).

### Opportunity

An opportunity represents an investable product or market independently of any particular treasury size.

Examples:

- a specific EUR money-market fund share class
- a specific sovereign security
- a tokenized money-market fund
- Aave EURC on a specific protocol version and chain

### Position Analysis

A treasury mandate is applied to an opportunity at a specified position size.

The analysis should eventually answer:

- Is the position supported?
- What percentage of the market would the position represent?
- What yield is realistically achievable at that size?
- Does the allocation itself affect yield?
- What annual income is expected?
- How much entry capacity exists?
- How much exit liquidity exists?
- How quickly can the position be exited?
- What incremental yield is earned relative to €STR?
- What additional risks are being accepted for that spread?

## V1 Risk Philosophy

Risk should not initially be collapsed into one opaque numerical score.

Relevant dimensions include:

- credit risk
- market risk
- liquidity risk
- currency and asset risk
- counterparty and structural risk
- technical risk
- operational risk

Observable risk data should remain separate from assessed risk classifications.

Risk may also depend on position size.

## Data Principles

1. EUR first.
2. Capital preservation and liquidity before yield.
3. Treasury size and position size are parameters.
4. Minimum useful allocations may be much smaller than total treasury capital.
5. Compare opportunities against an appropriate EUR cash benchmark.
6. Measure achievable yield at a specific position size, not headline yield alone.
7. Keep entry capacity separate from exit liquidity.
8. Keep raw observations separate from derived metrics and assessed risk.
9. Preserve source provenance and observation timestamps.
10. Separate opportunity eligibility from opportunity ranking.
11. Do not assume differently defined yield measures are directly comparable.
12. Prefer authoritative or primary sources where practical.
13. Add technology only when the project develops a problem that the technology solves.

## Initial Source Feasibility

Before choosing a data architecture, the project will test whether authoritative data can be retrieved and normalized from very different financial systems.

### Milestone 1A

ECB €STR benchmark.

Objective:

- retrieve recent €STR observations from the official ECB Data API
- validate the response
- normalize the latest observation
- print a small readable result

### Milestone 1B

Aave EURC market.

Objective:

- identify a meaningful live EURC lending market
- retrieve authoritative market state
- inspect yield, supply, borrow, utilization, liquidity, and capacity
- evaluate whether position-size-adjusted yield can be calculated

Only after both experiments are validated will the project introduce a shared canonical data model.

## Engineering Philosophy

This project intentionally does not begin with a predetermined data stack.

Technologies such as PostgreSQL, dbt, dlt, Prefect, Docker, cloud warehouses, Goldsky, dashboards, and CI/CD will be introduced only when an actual project requirement justifies them.