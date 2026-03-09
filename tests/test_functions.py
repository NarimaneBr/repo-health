from repo_health.analyzers.functions import FunctionSizeAnalyzer
from repo_health.config import Settings
from pathlib import Path

def test_functions_analyzer():
    analyzer = FunctionSizeAnalyzer()
    assert analyzer.name == "functions"
