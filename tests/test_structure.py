from repo_health.analyzers.structure import StructureAnalyzer
from repo_health.config import Settings
from pathlib import Path

def test_structure_analyzer():
    analyzer = StructureAnalyzer()
    assert analyzer.name == "structure"
