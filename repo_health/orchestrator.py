import subprocess
from pathlib import Path
from typing import List, Tuple
from .models import AnalysisResult
from .config import Settings
from .analyzers.base import BaseAnalyzer
from .analyzers.complexity import ComplexityAnalyzer
from .analyzers.functions import FunctionSizeAnalyzer
from .analyzers.tests import TestsAnalyzer
from .analyzers.dependencies import DependenciesAnalyzer
from .analyzers.structure import StructureAnalyzer
from .scoring import ScoreCalculator
from .utils.file_scanner import find_python_files
from .logger import get_logger

logger = get_logger("orchestrator")

class RepositoryAnalyzer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.analyzers: List[BaseAnalyzer] = [
            ComplexityAnalyzer(),
            FunctionSizeAnalyzer(),
            TestsAnalyzer(),
            DependenciesAnalyzer(),
            StructureAnalyzer()
        ]
        self.scorer = ScoreCalculator(settings)

    def _get_changed_files(self, root_path: Path, branch: str) -> List[Path]:
        try:
            output = subprocess.check_output(
                ["git", "diff", "--name-only", branch],
                cwd=str(root_path),
                text=True
            )
            files = []
            for line in output.splitlines():
                if line.strip() and line.endswith('.py'):
                    full_path = root_path / line.strip()
                    if full_path.exists():
                        files.append(full_path.resolve())
            return files
        except subprocess.CalledProcessError:
            print(f"Warning: Could not get diff for branch '{branch}'. Are you in a git repo?")
            return []

    def analyze(self, path: str, diff_branch: str = None) -> Tuple[int, List[AnalysisResult]]:
        root_path = Path(path).resolve()
        
        if not root_path.exists() or not root_path.is_dir():
            logger.error(f"Analysis failed: Directory not found: {path}")
            raise ValueError(f"Directory not found: {path}")
            
        logger.debug(f"Scanning python files in: {root_path}")
        files = find_python_files(root_path)
        logger.debug(f"Found {len(files)} python files.")
        
        if diff_branch:
            logger.info(f"Running diff analysis against branch: '{diff_branch}'")
            changed_files = self._get_changed_files(root_path, diff_branch)
            files = [f for f in files if f in changed_files]
            logger.debug(f"Files to analyze after diff filter: {len(files)}")
        
        results = []
        for analyzer in self.analyzers:
            logger.debug(f"Running '{analyzer.name}' analyzer...")
            result = analyzer.run(root_path, files, self.settings)
            results.append(result)
            
        logger.debug("Computing final global score...")
        global_score = self.scorer.compute(results)
        logger.debug(f"Global score calculated: {global_score}")
        
        return global_score, results
