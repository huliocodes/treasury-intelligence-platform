from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EvidenceRefreshCapability = Literal[
    "automatic",
    "manual",
    "supplied",
    "unsupported",
]


@dataclass(frozen=True)
class EvidenceRefreshCapabilityAssessment:
    source_reference: str
    capability: EvidenceRefreshCapability

    adapter_reference: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.source_reference.strip():
            raise ValueError(
                "source_reference is required."
            )

        if (
            self.capability == "automatic"
            and not self.adapter_reference
        ):
            raise ValueError(
                "Automatic refresh capability requires "
                "an adapter_reference."
            )

        if (
            self.capability != "automatic"
            and self.adapter_reference is not None
        ):
            raise ValueError(
                "Only automatic refresh capability may "
                "declare an adapter_reference."
            )
