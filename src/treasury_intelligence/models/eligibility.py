from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EligibilityCheck:
    check_name: str
    status: str

    required: bool

    actual_value: str | None = None
    required_value: str | None = None

    reason: str | None = None


@dataclass(frozen=True)
class EligibilityResult:
    result_id: str

    mandate_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float

    overall_status: str

    checks: tuple[EligibilityCheck, ...]