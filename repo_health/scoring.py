from typing import List
from .models import AnalysisResult
from .config import Settings

class ScoreCalculator:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _score_complexity(self, result: AnalysisResult) -> int:
        avg_comp = next((m.value for m in result.metrics if m.name == "avg_complexity"), 0)
        return max(0, 25 - max(0, (avg_comp - 5) * 2.5))
        
    def _score_functions(self, result: AnalysisResult) -> int:
        long_count = next((m.value for m in result.metrics if m.name == "long_functions_count"), 0)
        return max(0, 20 - (long_count * 4))
        
    def _score_tests(self, result: AnalysisResult) -> int:
        ratio = next((m.value for m in result.metrics if m.name == "test_ratio"), 0)
        min_ratio = self.settings.min_test_ratio
        if ratio >= min_ratio:
            return 25
        elif ratio >= min_ratio / 2:
            return 15
        elif ratio > 0:
            return 5
        return 0
        
    def _score_structure(self, result: AnalysisResult) -> int:
        struct_score = 15
        missing_count = next((m.value for m in result.metrics if m.name == "missing_essential_files_count"), 0)
        return max(0, struct_score - (missing_count * 3))
        
    def _score_dependencies(self, result: AnalysisResult) -> int:
        cycles = next((m.value for m in result.metrics if m.name == "circular_dependencies_count"), 0)
        return max(0, 15 - (cycles * 5))

    def compute(self, results: List[AnalysisResult]) -> int:
        score = 0
        
        scorers = {
            "complexity": self._score_complexity,
            "functions": self._score_functions,
            "tests": self._score_tests,
            "structure": self._score_structure,
            "dependencies": self._score_dependencies
        }
        
        for result in results:
            scorer = scorers.get(result.analyzer_name)
            if scorer:
                result.score = scorer(result)
                score += result.score
            else:
                result.score = 0

        return round(score)
