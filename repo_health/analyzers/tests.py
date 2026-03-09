import os
from pathlib import Path
from .base import BaseAnalyzer
from ..models import AnalysisResult, Metric, Issue
from ..config import Settings
from ..logger import get_logger

logger = get_logger("analyzers.tests")

class TestsAnalyzer(BaseAnalyzer):
    @property
    def name(self) -> str:
        return "tests"

    def run(self, root_path: Path, files: list[Path], settings: Settings) -> AnalysisResult:
        test_files = 0
        test_folders_found = False
        
        for f in files:
            if f.name.startswith('test_') or f.name.endswith('_test.py'):
                test_files += 1
                
        for dirpath, dirnames, _ in os.walk(root_path):
            if 'tests' in dirnames or 'test' in dirnames:
                test_folders_found = True
                break
                
        total_files = len(files)
        test_ratio = test_files / total_files if total_files > 0 else 0
        logger.debug(f"Test files: {test_files}/{total_files}, ratio: {test_ratio:.1%}")
        
        metrics = [
            Metric(name="test_files_count", value=test_files),
            Metric(name="test_ratio", value=test_ratio)
        ]
        
        issues = []
        suggestions = []
        
        if test_ratio < settings.min_test_ratio:
            issues.append(Issue(
                category="tests",
                message=f"Low test coverage (ratio: {test_ratio:.1%}, min expected: {settings.min_test_ratio:.1%})"
            ))
            suggestions.append("Increase unit test coverage")
            
        return AnalysisResult(
            analyzer_name=self.name,
            metrics=metrics,
            issues=issues,
            suggestions=suggestions,
            details={'test_folders_found': test_folders_found}
        )
