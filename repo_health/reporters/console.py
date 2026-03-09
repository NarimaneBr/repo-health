from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from typing import List
from ..models import AnalysisResult
from ..config import Settings

class ConsoleReporter:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.console = Console()

    def render(self, global_score: int, results: List[AnalysisResult], verbose: bool = False, hotspots: bool = False, root_path = None):
        color = "green" if global_score >= 80 else "yellow" if global_score >= 60 else "red"
        
        self.console.print()
        self.console.print(Panel(
            f"[bold {color}]Score: {global_score}/100[/bold {color}]",
            title="[bold blue]Repository Health Report[/bold blue]",
            expand=False,
            box=box.ROUNDED
        ))
        
        metrics_table = Table(title="Metrics", box=box.SIMPLE)
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="magenta")
        
        issues = []
        suggestions = []
        
        for result in results:
            for metric in result.metrics:
                if isinstance(metric.value, float):
                    metrics_table.add_row(metric.name.replace('_', ' ').capitalize(), f"{metric.value:.2g}")
                else:
                    metrics_table.add_row(metric.name.replace('_', ' ').capitalize(), str(metric.value))
                    
            issues.extend(result.issues)
            suggestions.extend(result.suggestions)
            
        self.console.print(metrics_table)
        
        if issues:
            self.console.print("[bold red]Issues[/bold red]")
            for issue in issues:
                self.console.print(f"  [red]-[/red] {issue.message}")
            self.console.print()
            
        if suggestions:
            self.console.print("[bold green]Suggestions[/bold green]")
            # Deduplicate suggestions
            for sug in list(dict.fromkeys(suggestions)):
                self.console.print(f"  [green]-[/green] {sug}")
            self.console.print()

        if hotspots and root_path:
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

        if verbose:
            self.console.print("[bold blue]Detailed Breakdown[/bold blue]")
            breakdown_table = Table(box=box.SIMPLE)
            breakdown_table.add_column("Category", style="cyan")
            breakdown_table.add_column("Points", style="magenta")
            
            for result in results:
                points = result.score
                if isinstance(points, float):
                    points = round(points, 1)
                breakdown_table.add_row(result.analyzer_name.capitalize(), str(points))
                
            self.console.print(breakdown_table)
