# Treasury Intelligence Platform

Data and decision infrastructure for corporate and institutional treasury allocation.

## Business Problem

A company has approximately €5 million of excess cash on its balance sheet.

The treasury wants to deploy that capital while prioritizing:

- capital preservation

- high liquidity

- minimal or no FX exposure

- minimal lockup

- approximately 3–5% annualized yield where justified by market conditions

- the ability to access capital quickly for inventory or operating needs

- approximately monthly review and reallocation

The core question is:

> What liquid yield opportunities exist, what can they realistically yield on €5 million, how much capital can they absorb, what risks exist, how quickly can the position be exited, and has a materially better opportunity appeared?

## Product Principle

This is not a generic DeFi yield dashboard.

The platform follows the treasury problem across both traditional and onchain markets.

Potential opportunity classes include:

- EUR money-market instruments

- short-duration government instruments

- tokenized money-market funds

- tokenized government debt

- onchain lending markets

- EUR stablecoin lending

- other highly liquid institutional-grade opportunities

## V1 Decision

Given a specified amount of EUR corporate treasury capital at time T:

> Which currently available opportunities can accept the allocation while satisfying liquidity, currency, capacity, and risk constraints, and what return can realistically be expected after accounting for position size?

## V1 Principles

1. EUR first.

2. Capital preservation and liquidity before yield.

3. Measure yield relative to an appropriate EUR cash benchmark.

4. Evaluate achievable yield at a specific position size, not headline APY alone.

5. Separate opportunity eligibility from opportunity ranking.

6. Preserve raw historical observations so decisions can later be evaluated through time.

7. Add technology only when the project develops a problem that the technology solves.

## Initial Scope

Reference source:

- ECB euro short-term rate (€STR)

First opportunity source to investigate:

- Aave

Initial opportunity:

- EUR-denominated lending markets

- EURC as the first asset to investigate

Initial treasury position:

- €5,000,000

Initial analytical output:

- `treasury_opportunity_snapshot`

## Engineering Philosophy

This project intentionally does not begin with a predetermined data stack.

Technologies such as PostgreSQL, dbt, Prefect, Docker, cloud warehouses, dashboards, and CI/CD will be introduced only when an actual project requirement justifies them.