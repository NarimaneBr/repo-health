import ast
from pathlib import Path
from .base import BaseAnalyzer
from ..models import AnalysisResult, Metric, Issue
from ..config import Settings

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.functions.append(node)
        self.generic_visit(node)

class FunctionSizeAnalyzer(BaseAnalyzer):
    @property
    def name(self) -> str:
        return "functions"

    def run(self, root_path: Path, files: list[Path], settings: Settings) -> AnalysisResult:
        long_functions = []
        total_functions = 0
        issues = []
        
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                tree = ast.parse(content)
                visitor = FunctionVisitor()
                visitor.visit(tree)
                
                for func in visitor.functions:
                    total_functions += 1
                    end_lineno = getattr(func, 'end_lineno', func.lineno)
                    lines = end_lineno - func.lineno + 1
                    if lines > settings.max_function_lines:
                        lf_data = {
                            'name': func.name,
                            'file': str(file),
                            'lines': lines,
                            'line': func.lineno
                        }
                        long_functions.append(lf_data)
                        issues.append(Issue(
                            category="function_size",
                            message=f"Function '{func.name}' is too long ({lines} lines > {settings.max_function_lines})",
                            file_path=str(file),
                            line=func.lineno
                        ))
            except Exception:
                pass
                
        long_functions.sort(key=lambda x: x['lines'], reverse=True)
                
        metrics = [
            Metric(name="total_functions", value=total_functions),
            Metric(name="long_functions_count", value=len(long_functions))
        ]
        
        suggestions = []
        if issues:
            suggestions.append("Split long functions into smaller, reusable pieces")
            
        return AnalysisResult(
            analyzer_name=self.name,
            metrics=metrics,
            issues=issues,
            suggestions=suggestions,
            details={'long_functions': long_functions}
        )
