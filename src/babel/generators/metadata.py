from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ImplementationLevel = Literal["canonical", "lightweight", "mock", "theoretical"]


@dataclass(frozen=True)
class ModelMetadata:
    mode_id: str
    stage_number: int | None
    display_name: str
    article_model_name: str
    formula: str
    implementation_level: ImplementationLevel
    required_data: list[str] = field(default_factory=list)
    theoretical_basis: str = ""
    limitations: list[str] = field(default_factory=list)
