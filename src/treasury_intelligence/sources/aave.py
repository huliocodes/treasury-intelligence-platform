from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from web3 import Web3

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
)


BASE_RPC_URL = "https://mainnet.base.org"

AAVE_V3_BASE_DATA_PROVIDER = Web3.to_checksum_address(
    "0x0F43731EB8d45A581f4a36DD74F5f358bc90C73A"
)

EURC_BASE = Web3.to_checksum_address(
    "0x60a3E35Cc302bFA44Cb288Bc5a4F316Fdb1adb42"
)

EURC_DECIMALS = 6

RAY = 10**27
SECONDS_PER_YEAR = 31_536_000


AAVE_DATA_PROVIDER_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "asset",
                "type": "address",
            }
        ],
        "name": "getReserveData",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "unbacked",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "accruedToTreasuryScaled",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "totalAToken",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "totalStableDebt",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "totalVariableDebt",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "liquidityRate",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "variableBorrowRate",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "stableBorrowRate",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "averageStableBorrowRate",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "liquidityIndex",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "variableBorrowIndex",
                "type": "uint256",
            },
            {
                "internalType": "uint40",
                "name": "lastUpdateTimestamp",
                "type": "uint40",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "asset",
                "type": "address",
            }
        ],
        "name": "getReserveCaps",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "borrowCap",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "supplyCap",
                "type": "uint256",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


@dataclass(frozen=True)
class AaveReserveObservation:
    protocol: str
    version: str
    chain: str
    asset: str
    supply_apy_pct: float
    total_supplied: float
    total_borrowed: float
    available_liquidity: float
    utilization_pct: float
    supply_cap: float | None
    observed_at: datetime


@dataclass(frozen=True)
class AavePositionSupport:
    position_size: float
    entry_supported: bool
    remaining_entry_capacity: float | None
    immediate_exit_coverage_pct: float


def _ray_apr_to_apy_pct(rate_ray: int) -> float:
    apr = rate_ray / RAY

    apy = (
        1 + apr / SECONDS_PER_YEAR
    ) ** SECONDS_PER_YEAR - 1

    return apy * 100


def fetch_aave_v3_base_eurc() -> AaveReserveObservation:
    web3 = Web3(
        Web3.HTTPProvider(
            BASE_RPC_URL,
            request_kwargs={"timeout": 30},
        )
    )

    if not web3.is_connected():
        raise ConnectionError(
            "Could not connect to Base RPC"
        )

    contract = web3.eth.contract(
        address=AAVE_V3_BASE_DATA_PROVIDER,
        abi=AAVE_DATA_PROVIDER_ABI,
    )

    reserve_data = contract.functions.getReserveData(
        EURC_BASE
    ).call()

    _, supply_cap_raw = (
        contract.functions.getReserveCaps(
            EURC_BASE
        ).call()
    )

    total_supplied_raw = reserve_data[2]
    total_stable_debt_raw = reserve_data[3]
    total_variable_debt_raw = reserve_data[4]
    liquidity_rate_ray = reserve_data[5]

    scale = 10**EURC_DECIMALS

    total_supplied = total_supplied_raw / scale

    total_borrowed = (
        total_stable_debt_raw
        + total_variable_debt_raw
    ) / scale

    available_liquidity = max(
        total_supplied - total_borrowed,
        0.0,
    )

    if total_supplied > 0:
        utilization_pct = (
            total_borrowed / total_supplied
        ) * 100
    else:
        utilization_pct = 0.0

    supply_cap = (
        None
        if supply_cap_raw == 0
        else float(supply_cap_raw)
    )

    latest_block = web3.eth.get_block("latest")

    observed_at = datetime.fromtimestamp(
        latest_block["timestamp"],
        tz=timezone.utc,
    )

    return AaveReserveObservation(
        protocol="Aave",
        version="V3",
        chain="Base",
        asset="EURC",
        supply_apy_pct=_ray_apr_to_apy_pct(
            liquidity_rate_ray
        ),
        total_supplied=total_supplied,
        total_borrowed=total_borrowed,
        available_liquidity=available_liquidity,
        utilization_pct=utilization_pct,
        supply_cap=supply_cap,
        observed_at=observed_at,
    )


def analyze_position_support(
    observation: AaveReserveObservation,
    position_size: float,
) -> AavePositionSupport:
    if position_size <= 0:
        raise ValueError(
            "position_size must be greater than zero"
        )

    if observation.supply_cap is None:
        remaining_entry_capacity = None
        entry_supported = True
    else:
        remaining_entry_capacity = max(
            observation.supply_cap
            - observation.total_supplied,
            0.0,
        )

        entry_supported = (
            position_size
            <= remaining_entry_capacity
        )

    immediate_exit_coverage_pct = min(
        observation.available_liquidity
        / position_size
        * 100,
        100.0,
    )

    return AavePositionSupport(
        position_size=position_size,
        entry_supported=entry_supported,
        remaining_entry_capacity=(
            remaining_entry_capacity
        ),
        immediate_exit_coverage_pct=(
            immediate_exit_coverage_pct
        ),
    )


AAVE_V3_BASE_EURC_INSTRUMENT = Instrument(
    instrument_id="aave_v3_base_eurc",
    provider="Aave",
    name="Aave V3 Base EURC Supply",
    instrument_type="defi_lending",
    legal_structure="onchain_lending_position",
    currency="EURC",
    yield_source="defi_borrower_demand",
    contract_address=(
        "0x60a3E35Cc302bFA44Cb288Bc5a4F316Fdb1adb42"
    ),
)


AAVE_V3_BASE_EURC_MARKET = Market(
    market_id="aave_v3_base_eurc_market",
    instrument_id=AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id,
    venue="Aave V3 Base",
    venue_type="defi_protocol",
    trading_currency="EURC",
)


AAVE_V3_BASE_EURC_DIRECT_ACCESS = AccessRoute(
    access_route_id="aave_v3_base_eurc_direct",
    market_id=AAVE_V3_BASE_EURC_MARKET.market_id,
    provider="Direct corporate wallet",
    route_type="onchain_self_custody",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


AAVE_V3_BASE_EURC_ACCESSIBILITY = Accessibility(
    access_route_id=(
        AAVE_V3_BASE_EURC_DIRECT_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="unverified",
    status="research_eligible_not_actionable",
    evidence_level="technical_access_only",
    notes=(
        "Aave market access is technically available, "
        "but the complete Slovenian corporate EUR bank "
        "account -> EURC -> Aave -> EUR -> corporate "
        "bank account operational and legal path has "
        "not yet been verified."
    ),
)    