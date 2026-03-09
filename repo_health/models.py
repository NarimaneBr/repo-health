from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Issue:
    category: str
    message: str
    file_path: Optional[str] = None
    line: Optional[int] = None

@dataclass
class Metric:
    name: str
    value: float | int | str

@dataclass
class AnalysisResult:
    analyzer_name: str
    metrics: List[Metric] = field(default_factory=list)
    issues: List[Issue] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)
    score: int = 0
