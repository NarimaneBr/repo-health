from repo_health.analyzers.complexity import ComplexityAnalyzer
from repo_health.config import Settings
from pathlib import Path

def test_complexity_analyzer():
    analyzer = ComplexityAnalyzer()
    assert analyzer.name == "complexity"
