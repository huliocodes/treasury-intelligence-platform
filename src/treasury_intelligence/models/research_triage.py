from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PriorAnalysisStatus = Literal[
    "none",
    "partial",
    "complete",
]

ResearchAction = Literal[
    "reuse_existing_analysis",
    "refresh_existing_analysis",
    "complete_missing_analysis",
]

EvidenceDimension = Literal[
    "identity",
    "corporate_access",
    "current_market_return",
    "realistic_net_return",
    "position_liquidity",
    "execution_cost",
    "risk_evidence",
]


@dataclass(frozen=True)
class ResearchEvidenceState:
    opportunity_id: str
    prior_analysis_status: PriorAnalysisStatus

    identity_evidence_sufficient: bool
    corporate_access_evidence_sufficient: bool
    current_market_return_evidence_sufficient: bool
    realistic_net_return_evidence_sufficient: bool
    position_liquidity_evidence_sufficient: bool
    execution_cost_evidence_sufficient: bool
    risk_evidence_sufficient: bool

    reusable_analysis_summary: str | None = None
    evidence_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.opportunity_id.strip():
            raise ValueError("opportunity_id must not be blank")

        if self.prior_analysis_status == "complete":
            required_complete_fields = (
                self.identity_evidence_sufficient,
                self.corporate_access_evidence_sufficient,
                self.current_market_return_evidence_sufficient,
                self.realistic_net_return_evidence_sufficient,
                self.position_liquidity_evidence_sufficient,
                self.execution_cost_evidence_sufficient,
                self.risk_evidence_sufficient,
            )

            if not all(required_complete_fields):
                raise ValueError(
                    "A complete prior analysis must have sufficient evidence "
                    "across all required research dimensions."
                )


@dataclass(frozen=True)
class ResearchTriageResult:
    opportunity_id: str
    display_name: str
    discovery_priority: Literal["high", "medium", "low"]
    action: ResearchAction

    missing_evidence: tuple[EvidenceDimension, ...]
    reusable_evidence: tuple[EvidenceDimension, ...]

    research_required: bool
    research_rank: int | None

    rationale: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.opportunity_id.strip():
            raise ValueError("opportunity_id must not be blank")

        if not self.display_name.strip():
            raise ValueError("display_name must not be blank")

        if self.action == "reuse_existing_analysis":
            if self.research_required:
                raise ValueError(
                    "reuse_existing_analysis must not require new research"
                )

            if self.research_rank is not None:
                raise ValueError(
                    "reuse_existing_analysis must not have a research rank"
                )

            if self.missing_evidence:
                raise ValueError(
                    "reuse_existing_analysis must not have missing evidence"
                )

        else:
            if not self.research_required:
                raise ValueError(
                    "Research actions other than reuse_existing_analysis "
                    "must require research"
                )

            if self.research_rank is None or self.research_rank <= 0:
                raise ValueError(
                    "Research-required results must have a positive rank"
                )

            if not self.missing_evidence:
                raise ValueError(
                    "Research-required results must identify missing evidence"
                )