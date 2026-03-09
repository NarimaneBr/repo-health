import argparse
import sys
from pathlib import Path
from .config import load_settings
from .orchestrator import RepositoryAnalyzer
from .reporters.console import ConsoleReporter
from .reporters.json_reporter import JsonReporter
from .reporters.badge import generate_badge
from .reporters.graph import generate_graph

def main():
    parser = argparse.ArgumentParser(description="A CLI that analyzes the health of your repository and provides actionable insights.")
    parser.add_argument("path", help="Path to the repository to analyze")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed report")
    parser.add_argument("--json", action="store_true", help="Output report in JSON format")
    parser.add_argument("--badge", action="store_true", help="Generate a repo-health-badge.svg")
    parser.add_argument("--graph", action="store_true", help="Generate an architecture dependency graph")
    parser.add_argument("--diff", type=str, metavar="BRANCH", help="Analyze only files changed compared to given branch")
    parser.add_argument("--fail-under", type=int, help="Exit code 1 if score is lower than threshold")
    parser.add_argument("--hotspots", action="store_true", help="Show code hotspots using git history")
    
    args = parser.parse_args()
    
    root_path = Path(args.path).resolve()
    settings = load_settings(root_path)
    
    analyzer = RepositoryAnalyzer(settings)
    
    try:
        global_score, results = analyzer.analyze(args.path, diff_branch=args.diff)
    except Exception as e:
        print(f"Error analyzing repository: {e}", file=sys.stderr)
        sys.exit(2)
        
    if args.json:
        reporter = JsonReporter()
        print(reporter.render(global_score, results))
    else:
        reporter = ConsoleReporter(settings)
        reporter.render(global_score, results, verbose=args.verbose, hotspots=args.hotspots, root_path=root_path if args.hotspots else None)
        
    if args.badge:
        badge_path = root_path / "repo-health-badge.svg"
        try:
            generate_badge(global_score, badge_path)
            print(f"\nBadge successfully generated at {badge_path}")
        except Exception as e:
            print(f"Error generating badge: {e}", file=sys.stderr)
            
    if args.graph:
        graph_path = root_path / "architecture-graph.svg"
        try:
            generate_graph(results, graph_path)
            print(f"\nDependency graph successfully generated at {graph_path}")
        except Exception as e:
            print(f"Error generating graph: {e}. You might need graphviz installed.", file=sys.stderr)

    threshold = args.fail_under if args.fail_under is not None else settings.fail_under_score
    if global_score < threshold:
        print(f"\nError: Score {global_score} is below the threshold of {threshold}. Failing.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
