from pathlib import Path
from radon.complexity import cc_visit
from .base import BaseAnalyzer
from ..models import AnalysisResult, Metric, Issue
from ..config import Settings

class ComplexityAnalyzer(BaseAnalyzer):
    @property
    def name(self) -> str:
        return "complexity"

    def run(self, root_path: Path, files: list[Path], settings: Settings) -> AnalysisResult:
        total_complexity = 0
        total_blocks = 0
        complex_functions = []
        issues = []
        file_complexities = {}
        
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                blocks = cc_visit(content)
                file_comp_sum = 0
                for block in blocks:
                    if hasattr(block, "complexity"):
                        total_complexity += block.complexity
                        file_comp_sum += block.complexity
                        total_blocks += 1
                        if block.complexity > settings.max_complexity:
                            complex_functions.append({
                                'name': block.name,
                                'file': str(file),
                                'complexity': block.complexity,
                                'line': getattr(block, 'lineno', 0)
                            })
                            issues.append(Issue(
                                category="complexity",
                                message=f"Function '{block.name}' has complexity {block.complexity} > {settings.max_complexity}",
                                file_path=str(file),
                                line=getattr(block, 'lineno', 0)
                            ))
                file_complexities[str(file)] = file_comp_sum
            except Exception:
                pass
                
        avg_complexity = total_complexity / total_blocks if total_blocks > 0 else 0
        complex_functions.sort(key=lambda x: x['complexity'], reverse=True)
        
        metrics = [
            Metric(name="avg_complexity", value=avg_complexity),
            Metric(name="complex_functions_count", value=len(complex_functions))
        ]
        
        suggestions = []
        if issues:
            suggestions.append("Simplify complex functions (e.g., extract methods)")
            
        return AnalysisResult(
            analyzer_name=self.name,
            metrics=metrics,
            issues=issues,
            suggestions=suggestions,
            details={
                "complex_functions": complex_functions,
                "file_complexities": file_complexities
            }
        )
