import pytest
from repo_health.analyzer import analyze_repo
from repo_health.scoring import calculate_score
import os

def test_analyze_repo_invalid_path():
    with pytest.raises(ValueError):
        analyze_repo("non_existent_path_12345")

def test_empty_repo(tmp_path):
    report = analyze_repo(str(tmp_path))
    assert 'score' in report
    assert 'metrics' in report
    assert report['metrics']['avg_complexity'] == 0
    assert report['metrics']['test_ratio'] == 0

def test_perfect_score():
    comp = {'avg_complexity': 2.0}
    func = {'long_functions': []}
    tests = {'test_ratio': 0.25}
    deps = {'circular_dependencies_count': 0}
    struct = {'missing_essential_files': []}
    config = {'min_test_ratio': 0.2}
    
    score, details = calculate_score(comp, func, tests, deps, struct, config)
    assert score == 100
