from typing import List
from .models import AnalysisResult
from .config import Settings

class ScoreCalculator:
    def __init__(self, settings: Settings):
        self.settings = settings

    def compute(self, results: List[AnalysisResult]) -> int:
        score = 0
        
        for result in results:
            if result.analyzer_name == "complexity":
                avg_comp = next((m.value for m in result.metrics if m.name == "avg_complexity"), 0)
                comp_score = max(0, 25 - max(0, (avg_comp - 5) * 2.5))
                result.score = comp_score
                score += comp_score
                
            elif result.analyzer_name == "functions":
                long_count = next((m.value for m in result.metrics if m.name == "long_functions_count"), 0)
                func_score = max(0, 20 - (long_count * 4))
                result.score = func_score
                score += func_score
                
            elif result.analyzer_name == "tests":
                ratio = next((m.value for m in result.metrics if m.name == "test_ratio"), 0)
                min_ratio = self.settings.min_test_ratio
                if ratio >= min_ratio:
                    test_score = 25
                elif ratio >= min_ratio / 2:
                    test_score = 15
                elif ratio > 0:
                    test_score = 5
                else:
                    test_score = 0
                result.score = test_score
                score += test_score
                
            elif result.analyzer_name == "structure":
                struct_score = 15
                missing_count = next((m.value for m in result.metrics if m.name == "missing_essential_files_count"), 0)
                struct_score -= (missing_count * 3)
                struct_score = max(0, struct_score)
                result.score = struct_score
                score += struct_score
                
            elif result.analyzer_name == "dependencies":
                cycles = next((m.value for m in result.metrics if m.name == "circular_dependencies_count"), 0)
                dep_score = max(0, 15 - (cycles * 5))
                result.score = dep_score
                score += dep_score
                
            else:
                result.score = 0

        return round(score)
