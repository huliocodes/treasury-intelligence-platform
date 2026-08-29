from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.portfolio import (
    blocked_candidates,
    build_portfolio_candidate_assessment,
    evidence_blocked_candidates,
    recommendation_ready_candidates,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_DIRECT_ACCESS,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_IBKR_ACCESS,
    BTF_2027_03_10_MARKET,
)

from treasury_intelligence.sources.ishares import (
    ERNX_IBKR_ACCESS,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


POSITION_SIZE_EUR = 500_000


def build_candidates():
    aave = (
        build_portfolio_candidate_assessment(
            assessment_id=(
                "aave_eurc_500k_portfolio_candidate"
            ),
            mandate_id=(
                MODEL_COMPANY_MANDATE.mandate_id
            ),
            instrument_id=(
                AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
            ),
            market_id=(
                AAVE_V3_BASE_EURC_MARKET.market_id
            ),
            access_route_id=(
                AAVE_V3_BASE_EURC_DIRECT_ACCESS.access_route_id
            ),
            label="Aave V3 Base EURC",
            position_size_eur=(
                POSITION_SIZE_EUR
            ),
            eligibility_status="ineligible",
            liquidity_position_status="supported",
            economics_status="incomplete",
            base_risk_unknown_dimension_count=7,
            defensible_return_pct=1.835,
            defensible_return_measure=(
                "Observed variable supply APY before "
                "unresolved execution frictions"
            ),
            blocking_reasons=(
                "Corporate operational access for the "
                "Slovenian d.o.o. execution path is "
                "unverified.",
            ),
            evidence_requirements=(
                "Quantify EUR-to-EURC entry cost, "
                "EURC-to-EUR exit cost, and Base "
                "transaction cost.",
            ),
            notes=(
                "Immediate liquidity is supported for "
                "the modeled EUR 500k position, but "
                "corporate accessibility fails the "
                "current V1 mandate."
            ),
        )
    )

    btf = (
        build_portfolio_candidate_assessment(
            assessment_id=(
                "btf_500k_portfolio_candidate"
            ),
            mandate_id=(
                MODEL_COMPANY_MANDATE.mandate_id
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            access_route_id=(
                BTF_2027_03_10_IBKR_ACCESS.access_route_id
            ),
            label="French BTF 10 Mar 2027",
            position_size_eur=(
                POSITION_SIZE_EUR
            ),
            eligibility_status="needs_evidence",
            liquidity_position_status="unknown",
            economics_status="incomplete",
            base_risk_unknown_dimension_count=4,
            defensible_return_pct=2.731,
            defensible_return_measure=(
                "Model-derived annualized yield from "
                "delayed public price before unresolved "
                "execution frictions"
            ),
            evidence_requirements=(
                "Obtain position-size executable "
                "secondary-market liquidity evidence.",
                "Confirm broker/access costs and "
                "secondary-market execution friction.",
            ),
            notes=(
                "Issue size and public price observation "
                "do not establish immediate executable "
                "liquidity."
            ),
        )
    )

    xeon = (
        build_portfolio_candidate_assessment(
            assessment_id=(
                "xeon_500k_portfolio_candidate"
            ),
            mandate_id=(
                MODEL_COMPANY_MANDATE.mandate_id
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=(
                XEON_MARKET.market_id
            ),
            access_route_id=(
                XEON_IBKR_ACCESS.access_route_id
            ),
            label="XEON",
            position_size_eur=(
                POSITION_SIZE_EUR
            ),
            eligibility_status="needs_evidence",
            liquidity_position_status="unknown",
            economics_status="incomplete",
            base_risk_unknown_dimension_count=4,
            defensible_return_pct=2.073,
            defensible_return_measure=(
                "365-day scenario return after currently "
                "known fund fee and published Fixed "
                "SmartRouting commission, before unknown "
                "spread, market impact, and residual "
                "access costs"
            ),
            evidence_requirements=(
                "Obtain position-size executable "
                "bid/ask and depth evidence.",
                "Resolve XEON spread, slippage, and "
                "market-impact economics.",
                "Confirm actual corporate brokerage "
                "pricing and residual access costs.",
            ),
            notes=(
                "2.073% is not a realistic executable "
                "return. It is only the return after "
                "currently known costs in the 365-day "
                "scenario."
            ),
        )
    )

    ernx = (
        build_portfolio_candidate_assessment(
            assessment_id=(
                "ernx_500k_portfolio_candidate"
            ),
            mandate_id=(
                MODEL_COMPANY_MANDATE.mandate_id
            ),
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=(
                ERNX_MARKET.market_id
            ),
            access_route_id=(
                ERNX_IBKR_ACCESS.access_route_id
            ),
            label="ERNX",
            position_size_eur=(
                POSITION_SIZE_EUR
            ),
            eligibility_status="needs_evidence",
            liquidity_position_status="unknown",
            economics_status="incomplete",
            base_risk_unknown_dimension_count=3,
            defensible_return_pct=2.790,
            defensible_return_measure=(
                "Published weighted-average YTM less "
                "published TER, before unresolved trading "
                "and access frictions"
            ),
            evidence_requirements=(
                "Obtain position-size executable "
                "bid/ask and depth evidence.",
                "Resolve ETF trading and access costs.",
            ),
            notes=(
                "2.790% is not an APY or guaranteed "
                "holding-period return."
            ),
        )
    )

    return (
        aave,
        btf,
        xeon,
        ernx,
    )


def print_candidate(
    candidate,
) -> None:
    print(candidate.label)
    print()

    print(
        f"Position size:                "
        f"EUR {candidate.position_size_eur:,.0f}"
    )

    print(
        f"Candidate status:             "
        f"{candidate.candidate_status}"
    )

    print(
        f"Recommendation ready:         "
        f"{candidate.recommendation_ready}"
    )

    print(
        f"Eligibility:                  "
        f"{candidate.eligibility_status}"
    )

    print(
        f"Position liquidity:           "
        f"{candidate.liquidity_position_status}"
    )

    print(
        f"Economics:                    "
        f"{candidate.economics_status}"
    )

    print(
        f"Unknown base-risk dimensions: "
        f"{candidate.base_risk_unknown_dimension_count}"
    )

    if candidate.defensible_return_pct is None:
        print(
            "Defensible return measure:     UNKNOWN"
        )
    else:
        print(
            f"Defensible return measure:     "
            f"{candidate.defensible_return_pct:.3f}%"
        )

        print(
            f"Return measure context:        "
            f"{candidate.defensible_return_measure}"
        )

    if candidate.blocking_reasons:
        print()
        print("BLOCKING REASONS")

        for reason in (
            candidate.blocking_reasons
        ):
            print(
                f"  - {reason}"
            )

    if candidate.evidence_requirements:
        print()
        print("EVIDENCE REQUIRED")

        for requirement in (
            candidate.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )

    print()
    print("-" * 110)
    print()


def main() -> None:
    candidates = build_candidates()

    print("PORTFOLIO CANDIDATE GATE")
    print()

    print(
        "An opportunity must clear mandate eligibility, "
        "position-size constraints, and economics evidence "
        "before it can enter a portfolio recommendation."
    )

    print(
        "Observed or partially defensible return figures "
        "are not automatically comparable executable "
        "returns."
    )

    print()
    print("-" * 110)
    print()

    for candidate in candidates:
        print_candidate(candidate)

    blocked = blocked_candidates(
        candidates
    )

    evidence_blocked = (
        evidence_blocked_candidates(
            candidates
        )
    )

    ready = (
        recommendation_ready_candidates(
            candidates
        )
    )

    print("PORTFOLIO GATE SUMMARY")
    print()

    print(
        f"Total candidates:          "
        f"{len(candidates)}"
    )

    print(
        f"Blocked:                   "
        f"{len(blocked)}"
    )

    print(
        f"Needs evidence:            "
        f"{len(evidence_blocked)}"
    )

    print(
        f"Recommendation ready:      "
        f"{len(ready)}"
    )

    print()

    if not ready:
        print(
            "No current candidate is ready to enter an "
            "allocation recommendation."
        )

        print(
            "The correct portfolio action at this stage "
            "is to resolve blocking evidence rather than "
            "force an allocation."
        )

    print()
    print("INTERPRETATION")
    print()

    print(
        "Candidate status is a portfolio-entry gate, "
        "not a ranking score."
    )

    print(
        "A higher displayed yield does not override "
        "eligibility, liquidity, risk evidence, or "
        "execution-economics requirements."
    )

    print(
        "Unknown qualitative risk dimensions are exposed "
        "but are not automatically rejected until the "
        "treasury mandate defines explicit risk limits."
    )


if __name__ == "__main__":
    main()