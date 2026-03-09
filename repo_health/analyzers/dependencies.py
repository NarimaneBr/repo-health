import ast
import networkx as nx
from pathlib import Path
from .base import BaseAnalyzer
from ..models import AnalysisResult, Metric, Issue
from ..config import Settings

def get_module_name(file_path: Path, root_path: Path):
    try:
        rel_path = file_path.relative_to(root_path)
        parts = list(rel_path.with_suffix('').parts)
        if parts and parts[-1] == '__init__':
            parts.pop()
        return '.'.join(parts)
    except ValueError:
        return file_path.stem

class DependenciesAnalyzer(BaseAnalyzer):
    """Analyze internal Python imports and detect circular dependencies.
    
    This analyzer builds a directed graph of local module imports and reports
    import cycles that may hurt maintainability.
    """
    
    @property
    def name(self) -> str:
        return "dependencies"

    def _process_import(self, node: ast.Import, mod_name: str, module_to_file: dict, G: nx.DiGraph):
        for alias in node.names:
            imported = alias.name
            if imported in module_to_file:
                G.add_edge(mod_name, imported)

    def _process_import_from(self, node: ast.ImportFrom, mod_name: str, module_to_file: dict, G: nx.DiGraph):
        if node.level == 0:
            if node.module and node.module in module_to_file:
                G.add_edge(mod_name, node.module)
        elif node.level > 0:
            parts = mod_name.split('.')
            base_idx = len(parts) - node.level
            if base_idx >= 0:
                base_mod = '.'.join(parts[:base_idx])
                target = f"{base_mod}.{node.module}" if (base_mod and node.module) else (base_mod or node.module)
                if target in module_to_file:
                    G.add_edge(mod_name, target)

    def _build_graph(self, root_path: Path, files: list[Path]) -> tuple[nx.DiGraph, dict]:
        G = nx.DiGraph()
        module_to_file = {}
        for f in files:
            mod_name = get_module_name(f, root_path)
            if mod_name:
                module_to_file[mod_name] = f
                G.add_node(mod_name)
                
        for mod_name, file_path in module_to_file.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        self._process_import(node, mod_name, module_to_file, G)
                    elif isinstance(node, ast.ImportFrom):
                        self._process_import_from(node, mod_name, module_to_file, G)
            except Exception:
                continue
        return G, module_to_file

    def run(self, root_path: Path, files: list[Path], settings: Settings) -> AnalysisResult:
        G, _ = self._build_graph(root_path, files)
        
        try:
            cycles = [c for c in nx.simple_cycles(G) if len(c) > 1]
        except Exception:
            cycles = []
            
        metrics = [Metric(name="circular_dependencies_count", value=len(cycles))]
        
        issues = []
        suggestions = []
        if cycles:
            issues.append(Issue(category="dependencies", message=f"{len(cycles)} circular dependencies detected"))
            suggestions.append("Refactor module imports to remove circular dependencies")
            
        return AnalysisResult(
            analyzer_name=self.name,
            metrics=metrics,
            issues=issues,
            suggestions=suggestions,
            details={'circular_dependencies': cycles[:10], 'nx_graph': G}
        )
