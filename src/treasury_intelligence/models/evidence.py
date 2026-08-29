from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceGap:
    evidence_gap_id: str

    mandate_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float

    check_name: str
    evidence_type: str

    priority: str
    current_status: str

    required_evidence: str
    resolution_action: str

    blocking: bool

    current_evidence_level: str | None = None
    required_evidence_level: str | None = None
    evidence_level_gap: int | None = None

    notes: str | None = None