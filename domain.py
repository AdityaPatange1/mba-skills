from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class ScenarioPlan:
    name: str
    context: str
    competencies: List[str]
    stressor: str
    evaluation_focus: List[str] = field(default_factory=list)
