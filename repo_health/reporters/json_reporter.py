import json
from dataclasses import asdict
from typing import List
from ..models import AnalysisResult

class JsonReporter:
    def render(self, global_score: int, results: List[AnalysisResult]) -> str:
        report = {
            "score": global_score,
            "results": [asdict(r) for r in results]
        }
        return json.dumps(report, indent=2)
