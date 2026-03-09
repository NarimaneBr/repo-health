from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from typing import List
from pathlib import Path
from ..models import AnalysisResult

class ConsoleReporter:
    def __init__(self, settings):
        self.settings = settings
        self.console = Console()

    def _print_header(self, score: int):
        color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        self.console.print()
        self.console.print(Panel(
            f"[bold {color}]Score: {score}/100[/bold {color}]",
            title="[bold blue]Repository Health Report[/bold blue]",
            expand=False,
            box=box.ROUNDED
        ))
        
    def _print_metrics(self, results: List[AnalysisResult]):
        table = Table(title="Metrics", box=box.SIMPLE)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        for result in results:
            for metric in result.metrics:
                val = f"{metric.value:.2g}" if isinstance(metric.value, float) else str(metric.value)
                table.add_row(metric.name.replace('_', ' ').capitalize(), val)
        self.console.print(table)
        
    def _print_issues_and_suggestions(self, results: List[AnalysisResult]):
        issues = []
        suggestions = []
        for result in results:
            issues.extend(result.issues)
            suggestions.extend(result.suggestions)
            
        if issues:
            self.console.print("[bold red]Issues[/bold red]")
            for issue in issues:
                self.console.print(f"  [red]-[/red] {issue.message}")
            self.console.print()
            
        if suggestions:
            self.console.print("[bold green]Suggestions[/bold green]")
            for sug in list(dict.fromkeys(suggestions)):
                self.console.print(f"  [green]-[/green] {sug}")
            self.console.print()

    def _print_hotspots(self, results: List[AnalysisResult], root_path: Path):
        self.console.print("[bold yellow]Code Hotspots[/bold yellow]")
        self.console.print("=" * 13)
        
        from ..utils.hotspots import get_commit_counts
        commits = get_commit_counts(root_path)
        
        complexity_data = {}
        for result in results:
            if result.analyzer_name == "complexity":
                complexity_data = result.details.get("file_complexities", {})
                
        hotspot_scores = []
        for file_path, comp in complexity_data.items():
            commit_count = commits.get(file_path, 0)
            score = comp * commit_count
            if score > 0:
                hotspot_scores.append({
                    "file": file_path,
                    "complexity": comp,
                    "commits": commit_count,
                    "score": score
                })
                
        hotspot_scores.sort(key=lambda x: x["score"], reverse=True)
        
        if not hotspot_scores:
            self.console.print("No hotspots detected (are you in a git repository with commits?).\n")
        else:
            for hs in hotspot_scores[:5]:
                rel_path = str(Path(hs['file']).relative_to(root_path))
                self.console.print(f"\n[cyan]{rel_path}[/cyan]")
                self.console.print(f"  complexity: {hs['complexity']}")
                self.console.print(f"  commits: {hs['commits']}")
                self.console.print(f"  hotspot score: [bold red]HIGH[/bold red] ({hs['score']} pts)")
            self.console.print()

    def _print_verbose(self, results: List[AnalysisResult]):
        self.console.print("[bold blue]Detailed Breakdown[/bold blue]")
        table = Table(box=box.SIMPLE)
        table.add_column("Category", style="cyan")
        table.add_column("Points", style="magenta")
        for result in results:
            points = result.score
            if isinstance(points, float):
                points = round(points, 1)
            table.add_row(result.analyzer_name.capitalize(), str(points))
        self.console.print(table)

    def render(self, global_score: int, results: List[AnalysisResult], verbose: bool = False, hotspots: bool = False, root_path = None):
        self._print_header(global_score)
        self._print_metrics(results)
        self._print_issues_and_suggestions(results)
        if hotspots and root_path:
            self._print_hotspots(results, root_path)
        if verbose:
            self._print_verbose(results)
