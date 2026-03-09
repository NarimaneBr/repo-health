from repo_health.analyzers.dependencies import DependenciesAnalyzer
from repo_health.config import Settings
from pathlib import Path

def test_dependencies_analyzer():
    analyzer = DependenciesAnalyzer()
    assert analyzer.name == "dependencies"
