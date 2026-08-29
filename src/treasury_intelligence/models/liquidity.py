from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidityEvidenceAssessment:
    assessment_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float

    evidence_level: str
    evidence_rank: int

    market_activity_observed: bool
    displayed_quote_observed: bool
    displayed_size_observed: bool
    executable_quote_observed: bool
    position_depth_observed: bool

    immediate_liquidity_supported: bool | None

    sufficient_for_immediate_liquidity: bool

    strongest_supported_claim: str

    missing_evidence: str | None = None
    notes: str | None = None