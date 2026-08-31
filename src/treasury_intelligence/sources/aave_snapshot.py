from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    OpportunitySnapshot,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_DIRECT_ACCESS,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
    AaveReserveObservation,
)


def build_aave_eurc_snapshot(
    observation: AaveReserveObservation,
) -> OpportunitySnapshot:
    if observation.supply_apy_pct < 0:
        raise ValueError(
            "Aave supply APY cannot be negative."
        )

    if observation.total_supplied < 0:
        raise ValueError(
            "Aave total supplied cannot be negative."
        )

    if observation.total_borrowed < 0:
        raise ValueError(
            "Aave total borrowed cannot be negative."
        )

    if observation.available_liquidity < 0:
        raise ValueError(
            "Aave available liquidity cannot be negative."
        )

    observed_at = observation.observed_at

    if observed_at.tzinfo is None:
        raise ValueError(
            "Aave observation timestamp must be timezone-aware."
        )

    observed_date = (
        observed_at.date().isoformat()
    )

    snapshot_timestamp = (
        observed_at.strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )

    return OpportunitySnapshot(
        snapshot_id=(
            "aave_v3_base_eurc_"
            f"{snapshot_timestamp}"
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
        observed_date=observed_date,
        yield_measure="protocol_supply_apy",
        yield_value_pct=observation.supply_apy_pct,
        yield_basis=(
            "Current Aave V3 Base EURC supply APY derived "
            "from the reserve liquidity rate observed "
            "onchain. The rate is variable and can change "
            "with protocol utilization and borrower demand."
        ),
        annual_fee_pct=None,
        early_exit_possible=True,
        source="Aave V3 Base onchain reserve data",
        source_url=None,
        notes=(
            "The snapshot records the current protocol "
            "supply APY as the reference return. Structural "
            "withdrawal functionality exists, but actual "
            "immediate exit capacity is evaluated separately "
            "from available reserve liquidity at the proposed "
            "position size. EURC acquisition, redemption, "
            "network, execution, operational and corporate "
            "access costs are not implied to be zero."
        ),
    )