from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


DiscoveryPriority = Literal["high", "medium", "low"]
DiscoveryStatus = Literal[
    "discovered",
    "screened_out",
    "research_candidate",
    "access_unknown",
    "access_blocked",
]
CorporateAccessStatus = Literal[
    "verified",
    "plausible",
    "unknown",
    "blocked",
]
MandateRelevance = Literal[
    "high",
    "medium",
    "low",
    "none",
]


@dataclass(frozen=True)
class DiscoveryScreeningContext:
    base_currency: str
    treasury_capital_eur: float
    minimum_useful_allocation_eur: float
    allowed_currencies: tuple[str, ...]
    require_verified_corporate_access: bool

    def __post_init__(self) -> None:
        if not self.base_currency.strip():
            raise ValueError("base_currency must not be blank")

        if self.treasury_capital_eur <= 0:
            raise ValueError("treasury_capital_eur must be greater than zero")

        if self.minimum_useful_allocation_eur <= 0:
            raise ValueError(
                "minimum_useful_allocation_eur must be greater than zero"
            )

        if self.minimum_useful_allocation_eur > self.treasury_capital_eur:
            raise ValueError(
                "minimum_useful_allocation_eur cannot exceed treasury_capital_eur"
            )

        if not self.allowed_currencies:
            raise ValueError("allowed_currencies must not be empty")


@dataclass(frozen=True)
class DiscoveryOpportunity:
    opportunity_id: str
    strategy_id: str
    implementation_id: str
    display_name: str
    full_name: str
    category: str

    short_description: str
    economic_description: str
    return_source: str

    currency: str | None
    issuer_manager_protocol: str | None

    possible_access_route: str | None
    slovenian_doo_access_status: CorporateAccessStatus
    access_evidence_sufficient: bool

    discovery_priority: DiscoveryPriority
    mandate_relevance: MandateRelevance

    minimum_investment_eur: float | None = None
    maximum_plausible_allocation_eur: float | None = None

    preliminary_yield_pct: float | None = None
    yield_as_of: str | None = None
    maturity_date: str | None = None

    liquidity_summary: str | None = None

    known_hard_mandate_conflict: bool = False
    known_hard_mandate_conflict_reason: str | None = None

    source_summary: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        required_text_fields = {
            "opportunity_id": self.opportunity_id,
            "strategy_id": self.strategy_id,
            "implementation_id": self.implementation_id,
            "display_name": self.display_name,
            "full_name": self.full_name,
            "category": self.category,
            "short_description": self.short_description,
            "economic_description": self.economic_description,
            "return_source": self.return_source,
        }

        for field_name, value in required_text_fields.items():
            if not value.strip():
                raise ValueError(f"{field_name} must not be blank")

        if (
            self.minimum_investment_eur is not None
            and self.minimum_investment_eur < 0
        ):
            raise ValueError(
                "minimum_investment_eur cannot be negative"
            )

        if (
            self.maximum_plausible_allocation_eur is not None
            and self.maximum_plausible_allocation_eur < 0
        ):
            raise ValueError(
                "maximum_plausible_allocation_eur cannot be negative"
            )

        if (
            self.known_hard_mandate_conflict
            and not self.known_hard_mandate_conflict_reason
        ):
            raise ValueError(
                "known_hard_mandate_conflict_reason is required "
                "when known_hard_mandate_conflict is True"
            )


@dataclass(frozen=True)
class DiscoveryScreeningResult:
    opportunity_id: str
    display_name: str
    category: str

    status: DiscoveryStatus
    research_priority: DiscoveryPriority

    screening_reasons: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

    corporate_access_status: CorporateAccessStatus
    access_evidence_sufficient: bool

    suitable_for_full_research: bool

    def __post_init__(self) -> None:
        if not self.opportunity_id.strip():
            raise ValueError("opportunity_id must not be blank")

        if not self.display_name.strip():
            raise ValueError("display_name must not be blank")

        if not self.category.strip():
            raise ValueError("category must not be blank")

        if self.status == "research_candidate":
            if not self.suitable_for_full_research:
                raise ValueError(
                    "research_candidate must be suitable_for_full_research"
                )

            if self.evidence_requirements:
                raise ValueError(
                    "research_candidate cannot have unresolved "
                    "screening evidence requirements"
                )

        if self.status != "research_candidate":
            if self.suitable_for_full_research:
                raise ValueError(
                    "only research_candidate may be "
                    "suitable_for_full_research"
                )