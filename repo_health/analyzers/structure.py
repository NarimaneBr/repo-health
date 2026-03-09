from pathlib import Path
from .base import BaseAnalyzer
from ..models import AnalysisResult, Metric, Issue
from ..config import Settings
from ..logger import get_logger

logger = get_logger("analyzers.structure")

class StructureAnalyzer(BaseAnalyzer):
    @property
    def name(self) -> str:
        return "structure"

    def run(self, root_path: Path, files: list[Path], settings: Settings) -> AnalysisResult:
        has_readme = (root_path / 'README.md').exists() or (root_path / 'README.txt').exists() or (root_path / 'README.rst').exists() or (root_path / 'README').exists()
        has_reqs = (root_path / 'requirements.txt').exists() or (root_path / 'pyproject.toml').exists()
        has_tests = (root_path / 'tests').is_dir() or (root_path / 'test').is_dir()
        has_gitignore = (root_path / '.gitignore').exists()
        
        missing = []
        if not has_readme: missing.append("README.md")
        if not has_reqs: missing.append("requirements.txt or pyproject.toml")
        if not has_tests: missing.append("tests/ folder")
        if not has_gitignore: missing.append(".gitignore")
        
        if missing:
            logger.debug(f"Missing essential files: {missing}")
        else:
            logger.debug("All essential files present.")
        
        issues = []
        suggestions = []
        if missing:
            issues.append(Issue(
                category="structure",
                message=f"Missing essential files: {', '.join(missing)}"
            ))
            suggestions.append(f"Add missing files: {', '.join(missing)}")
            
        metrics = [
            Metric(name="missing_essential_files_count", value=len(missing))
        ]
        
        return AnalysisResult(
            analyzer_name=self.name,
            metrics=metrics,
            issues=issues,
            suggestions=suggestions,
            details={
                'has_readme': has_readme,
                'has_requirements_or_pyproject': has_reqs,
                'has_tests_folder': has_tests,
                'has_gitignore': has_gitignore,
                'missing_essential_files': missing
            }
        )
