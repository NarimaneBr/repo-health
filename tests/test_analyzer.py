import pytest
from repo_health.orchestrator import RepositoryAnalyzer
from repo_health.scoring import ScoreCalculator
from repo_health.models import AnalysisResult, Metric
from repo_health.config import Settings
import os

def test_analyze_repo_invalid_path():
    analyzer = RepositoryAnalyzer(Settings())
    with pytest.raises(ValueError):
        analyzer.analyze("non_existent_path_12345")

def test_empty_repo(tmp_path):
    analyzer = RepositoryAnalyzer(Settings())
    score, results = analyzer.analyze(str(tmp_path))
    assert isinstance(score, int)
    assert len(results) > 0

def test_perfect_score():
    scorer = ScoreCalculator(Settings(min_test_ratio=0.2))
    
    comp = AnalysisResult(analyzer_name="complexity", metrics=[Metric("avg_complexity", 2.0)])
    func = AnalysisResult(analyzer_name="functions", metrics=[Metric("long_functions_count", 0)])
    tests = AnalysisResult(analyzer_name="tests", metrics=[Metric("test_ratio", 0.25)])
    deps = AnalysisResult(analyzer_name="dependencies", metrics=[Metric("circular_dependencies_count", 0)])
    struct = AnalysisResult(analyzer_name="structure", metrics=[Metric("missing_essential_files_count", 0)])
    
    score = scorer.compute([comp, func, tests, deps, struct])
    assert score == 100
