from __future__ import annotations

from collections import Counter

from treasury_intelligence.analytics.discovery_screening import (
    screen_discovery_universe,
)
from treasury_intelligence.models.discovery_screening import (
    DiscoveryOpportunity,
    DiscoveryScreeningContext,
)


def build_screening_context() -> DiscoveryScreeningContext:
    return DiscoveryScreeningContext(
        base_currency="EUR",
        treasury_capital_eur=5_000_000.0,
        minimum_useful_allocation_eur=100_000.0,
        allowed_currencies=("EUR",),
        require_verified_corporate_access=True,
    )


def build_diagnostic_opportunities() -> tuple[
    DiscoveryOpportunity,
    ...,
]:
    return (
        DiscoveryOpportunity(
            opportunity_id="slovenia_tbill_dz125",
            strategy_id="slovenia_sovereign_bills",
            implementation_id="dz125",
            display_name="Slovenia DZ125",
            full_name="Republic of Slovenia 12-Month Treasury Bill DZ125",
            category="direct_sovereign_bill",
            short_description=(
                "Short-term EUR debt issued directly by the "
                "Republic of Slovenia."
            ),
            economic_description=(
                "The treasury owns a direct debt claim against the "
                "Republic of Slovenia."
            ),
            return_source=(
                "Discount yield earned as the Treasury bill converges "
                "toward redemption at maturity."
            ),
            currency="EUR",
            issuer_manager_protocol="Republic of Slovenia",
            possible_access_route=(
                "Primary auction through an eligible primary dealer "
                "or subsequent secondary-market access."
            ),
            slovenian_doo_access_status="verified",
            access_evidence_sufficient=True,
            discovery_priority="high",
            mandate_relevance="high",
            minimum_investment_eur=1_000.0,
            maximum_plausible_allocation_eur=None,
            preliminary_yield_pct=None,
            yield_as_of=None,
            maturity_date="2027-09-09",
            liquidity_summary=(
                "Short-dated home-market sovereign security; exact "
                "position-aware liquidity requires full research."
            ),
            source_summary=(
                "Slovenian Ministry of Finance issuance information."
            ),
        ),
        DiscoveryOpportunity(
            opportunity_id="blackrock_ics_euro_core_acc",
            strategy_id="blackrock_ics_euro_liquidity",
            implementation_id="core_acc",
            display_name="BlackRock ICS Euro Liquidity Core Acc",
            full_name="BlackRock ICS Euro Liquidity Fund Core Acc",
            category="institutional_money_market_fund",
            short_description=(
                "Institutional EUR liquidity fund designed for "
                "short-term cash management."
            ),
            economic_description=(
                "The treasury owns fund shares backed by diversified "
                "short-term EUR money-market instruments and deposits."
            ),
            return_source=(
                "Interest earned by the underlying short-term portfolio "
                "after fund expenses."
            ),
            currency="EUR",
            issuer_manager_protocol="BlackRock",
            possible_access_route=(
                "Institutional fund subscription through an eligible "
                "distribution or custody route."
            ),
            slovenian_doo_access_status="plausible",
            access_evidence_sufficient=False,
            discovery_priority="high",
            mandate_relevance="high",
            minimum_investment_eur=1_000_000.0,
            maximum_plausible_allocation_eur=5_000_000.0,
            preliminary_yield_pct=2.21,
            yield_as_of="2026-08-31",
            maturity_date=None,
            liquidity_summary="Daily dealing with approximately T+1 settlement.",
            source_summary="BlackRock product materials.",
        ),
        DiscoveryOpportunity(
            opportunity_id="blackrock_ics_euro_premier",
            strategy_id="blackrock_ics_euro_liquidity",
            implementation_id="premier",
            display_name="BlackRock ICS Euro Liquidity Premier",
            full_name="BlackRock ICS Euro Liquidity Fund Premier Share Class",
            category="institutional_money_market_fund",
            short_description=(
                "Higher-tier institutional share class of the "
                "BlackRock EUR liquidity strategy."
            ),
            economic_description=(
                "The treasury would own a share class of the same "
                "underlying EUR institutional money-market fund."
            ),
            return_source=(
                "Interest from the underlying money-market portfolio "
                "after share-class expenses."
            ),
            currency="EUR",
            issuer_manager_protocol="BlackRock",
            possible_access_route=(
                "Institutional fund subscription."
            ),
            slovenian_doo_access_status="plausible",
            access_evidence_sufficient=False,
            discovery_priority="low",
            mandate_relevance="high",
            minimum_investment_eur=500_000_000.0,
            maximum_plausible_allocation_eur=None,
            preliminary_yield_pct=2.31,
            yield_as_of="2026-08-31",
            maturity_date=None,
            liquidity_summary="Daily dealing.",
            source_summary="BlackRock product materials.",
        ),
        DiscoveryOpportunity(
            opportunity_id="ernx",
            strategy_id="eur_ultrashort_investment_grade_bonds",
            implementation_id="ernx_xetra",
            display_name="ERNX",
            full_name="iShares € Ultrashort Bond UCITS ETF",
            category="short_duration_bond_etf",
            short_description=(
                "Diversified ETF holding very short-duration "
                "investment-grade EUR bonds."
            ),
            economic_description=(
                "The treasury owns ETF shares backed by a diversified "
                "portfolio of short-duration fixed-income securities."
            ),
            return_source=(
                "Underlying bond income and price convergence less "
                "fund and execution costs."
            ),
            currency="EUR",
            issuer_manager_protocol="BlackRock / iShares",
            possible_access_route="IBKR corporate account via Xetra.",
            slovenian_doo_access_status="verified",
            access_evidence_sufficient=True,
            discovery_priority="high",
            mandate_relevance="high",
            minimum_investment_eur=None,
            maximum_plausible_allocation_eur=5_000_000.0,
            preliminary_yield_pct=2.91,
            yield_as_of="2026-08-28",
            maturity_date=None,
            liquidity_summary=(
                "Large UCITS ETF with position-aware liquidity "
                "already researched in V1."
            ),
            source_summary="Existing V1 evidence package.",
        ),
        DiscoveryOpportunity(
            opportunity_id="icslo",
            strategy_id="slovenian_public_equities",
            implementation_id="icslo_ljse",
            display_name="ICSLO",
            full_name="InterCapital SBITOP TR UCITS ETF",
            category="equity_etf",
            short_description=(
                "ETF providing exposure to major Slovenian listed equities."
            ),
            economic_description=(
                "The treasury owns equity ETF shares whose value "
                "moves with Slovenian public companies."
            ),
            return_source=(
                "Equity price appreciation and dividends."
            ),
            currency="EUR",
            issuer_manager_protocol="InterCapital",
            possible_access_route="Ljubljana Stock Exchange brokerage.",
            slovenian_doo_access_status="verified",
            access_evidence_sufficient=True,
            discovery_priority="low",
            mandate_relevance="low",
            minimum_investment_eur=None,
            maximum_plausible_allocation_eur=None,
            preliminary_yield_pct=None,
            yield_as_of=None,
            maturity_date=None,
            liquidity_summary="Exchange traded.",
            known_hard_mandate_conflict=True,
            known_hard_mandate_conflict_reason=(
                "Equity market risk is incompatible with the current "
                "very-high capital-preservation treasury mandate."
            ),
            source_summary="Ljubljana Stock Exchange product information.",
        ),
        DiscoveryOpportunity(
            opportunity_id="morpho_small_eurc_vault",
            strategy_id="morpho_eurc_lending",
            implementation_id="small_eurc_vault_fixture",
            display_name="Morpho Small EURC Vault",
            full_name="Morpho EURC Vault Diagnostic Fixture",
            category="defi_lending",
            short_description=(
                "Curated onchain EURC lending vault."
            ),
            economic_description=(
                "The treasury would own vault shares representing "
                "EURC allocated into collateralized Morpho lending markets."
            ),
            return_source=(
                "Borrower interest generated in underlying lending "
                "markets after applicable fees."
            ),
            currency="EUR",
            issuer_manager_protocol="Morpho",
            possible_access_route=(
                "Corporate bank EUR to EURC to onchain vault."
            ),
            slovenian_doo_access_status="unknown",
            access_evidence_sufficient=False,
            discovery_priority="low",
            mandate_relevance="medium",
            minimum_investment_eur=None,
            maximum_plausible_allocation_eur=1_038.0,
            preliminary_yield_pct=2.8,
            yield_as_of="2026-09-01",
            maturity_date=None,
            liquidity_summary=(
                "Displayed vault size is far below the mandate's "
                "minimum useful allocation."
            ),
            source_summary="Morpho application discovery research.",
        ),
        DiscoveryOpportunity(
            opportunity_id="eu_bill_aug_2027",
            strategy_id="eu_supranational_bills",
            implementation_id="EU000A4EYPS6",
            display_name="EU-Bill Aug 2027",
            full_name="European Union Bill EU000A4EYPS6",
            category="supranational_bill",
            short_description=(
                "Short-term EUR debt issued directly by the European Union."
            ),
            economic_description=(
                "The treasury owns a direct debt claim against the "
                "European Union."
            ),
            return_source=(
                "Discount yield earned as the bill converges toward "
                "redemption at maturity."
            ),
            currency="EUR",
            issuer_manager_protocol="European Union",
            possible_access_route=(
                "Secondary-market bond access through a corporate broker."
            ),
            slovenian_doo_access_status="unknown",
            access_evidence_sufficient=False,
            discovery_priority="high",
            mandate_relevance="high",
            minimum_investment_eur=None,
            maximum_plausible_allocation_eur=5_000_000.0,
            preliminary_yield_pct=2.704,
            yield_as_of="2026-08-05",
            maturity_date="2027-08-06",
            liquidity_summary=(
                "Multi-billion-euro institutional issue; exact "
                "secondary-market execution requires full research."
            ),
            source_summary="European Commission auction results.",
        ),
        DiscoveryOpportunity(
            opportunity_id="aave_base_eurc",
            strategy_id="aave_eur_lending",
            implementation_id="aave_v3_base_eurc",
            display_name="Aave V3 Base EURC",
            full_name="Aave V3 Base EURC Supply Market",
            category="defi_lending",
            short_description=(
                "EURC supplied into Aave V3's overcollateralized "
                "lending market on Base."
            ),
            economic_description=(
                "The treasury owns an onchain lending position "
                "representing supplied EURC plus accrued variable interest."
            ),
            return_source="Variable interest paid by borrowers.",
            currency="EUR",
            issuer_manager_protocol="Aave",
            possible_access_route=(
                "Bank EUR to EURC to Aave on Base and back to bank EUR."
            ),
            slovenian_doo_access_status="unknown",
            access_evidence_sufficient=False,
            discovery_priority="medium",
            mandate_relevance="medium",
            minimum_investment_eur=None,
            maximum_plausible_allocation_eur=5_000_000.0,
            preliminary_yield_pct=1.74,
            yield_as_of="2026-09-01",
            maturity_date=None,
            liquidity_summary=(
                "Existing V1 research found insufficient immediate "
                "exit coverage for the full €5 million."
            ),
            source_summary="Existing V1 Aave evidence package.",
        ),
    )


def main() -> None:
    context = build_screening_context()
    opportunities = build_diagnostic_opportunities()

    results = screen_discovery_universe(
        opportunities=opportunities,
        context=context,
    )

    status_counts = Counter(
        result.status
        for result in results
    )

    print("===== DISCOVERY SCREENING DIAGNOSTIC =====")
    print(
        f"treasury_capital_eur={context.treasury_capital_eur:,.0f}"
    )
    print(
        "minimum_useful_allocation_eur="
        f"{context.minimum_useful_allocation_eur:,.0f}"
    )
    print(
        f"require_verified_corporate_access="
        f"{context.require_verified_corporate_access}"
    )
    print()

    for result in results:
        print(
            f"{result.opportunity_id}: "
            f"{result.status} | "
            f"priority={result.research_priority} | "
            f"full_research={result.suitable_for_full_research}"
        )

        for reason in result.screening_reasons:
            print(f"  reason: {reason}")

        for requirement in result.evidence_requirements:
            print(f"  evidence: {requirement}")

    print()
    print("===== STATUS COUNTS =====")

    for status in (
        "research_candidate",
        "access_unknown",
        "access_blocked",
        "screened_out",
        "discovered",
    ):
        print(
            f"{status}={status_counts.get(status, 0)}"
        )

    research_candidates = [
        result
        for result in results
        if result.suitable_for_full_research
    ]

    print()
    print(
        "research_candidate_count="
        f"{len(research_candidates)}"
    )

    print(
        "research_candidates="
        + ",".join(
            result.opportunity_id
            for result in research_candidates
        )
    )


if __name__ == "__main__":
    main()