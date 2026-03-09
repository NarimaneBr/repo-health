import argparse
import sys
from pathlib import Path
from .config import load_settings
from .orchestrator import RepositoryAnalyzer
from .reporters.console import ConsoleReporter
from .reporters.json_reporter import JsonReporter
from .reporters.markdown_reporter import MarkdownReporter
from .reporters.badge import generate_badge
from .reporters.graph import generate_graph

def main():
    parser = argparse.ArgumentParser(description="A CLI that analyzes the health of your repository and provides actionable insights.")
    parser.add_argument("path", help="Path to the repository to analyze")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed report")
    parser.add_argument("--json", action="store_true", help="Output report in JSON format")
    parser.add_argument("--md", action="store_true", help="Output report in Markdown format (repo-health-report.md)")
    parser.add_argument("--badge", action="store_true", help="Generate a repo-health-badge.svg")
    parser.add_argument("--graph", action="store_true", help="Generate an architecture dependency graph")
    parser.add_argument("--diff", type=str, metavar="BRANCH", help="Analyze only files changed compared to given branch")
    parser.add_argument("--fail-under", type=int, help="Exit code 1 if score is lower than threshold")
    parser.add_argument("--hotspots", action="store_true", help="Show code hotspots using git history")
    
    args = parser.parse_args()
    
    from .logger import setup_logger, get_logger
    setup_logger(args.verbose)
    logger = get_logger("cli")
    
    root_path = Path(args.path).resolve()
    logger.debug(f"Loading settings for path: {root_path}")
    settings = load_settings(root_path)
    
    analyzer = RepositoryAnalyzer(settings)
    
    try:
        logger.info("Starting repository analysis...")
        global_score, results = analyzer.analyze(args.path, diff_branch=args.diff)
        logger.info("Analysis completed successfully.")
    except Exception as e:
        logger.exception(f"Error analyzing repository: {e}")
        sys.exit(2)
        
    if args.json:
        logger.debug("Rendering JSON report")
        reporter = JsonReporter()
        print(reporter.render(global_score, results))
    else:
        logger.debug("Rendering Console report")
        reporter = ConsoleReporter(settings)
        reporter.render(global_score, results, verbose=args.verbose, hotspots=args.hotspots, root_path=root_path if args.hotspots else None)
        
    if args.md:
        md_path = root_path / "repo-health-report.md"
        try:
            logger.debug(f"Generating markdown report at {md_path}")
            MarkdownReporter().render(global_score, results, md_path)
            logger.info(f"Markdown report successfully generated at {md_path}")
        except Exception as e:
            logger.error(f"Error generating markdown report: {e}")
            
    if args.badge:
        badge_path = root_path / "repo-health-badge.svg"
        try:
            logger.debug(f"Generating badge at {badge_path}")
            generate_badge(global_score, badge_path)
            logger.info(f"Badge successfully generated at {badge_path}")
        except Exception as e:
            logger.error(f"Error generating badge: {e}")
            
    if args.graph:
        graph_path = root_path / "architecture-graph.svg"
        try:
            logger.debug(f"Generating architecture graph at {graph_path}")
            generate_graph(results, graph_path)
            logger.info(f"Dependency graph successfully generated at {graph_path}")
        except Exception as e:
            logger.warning(f"Error generating graph (graphviz might be missing): {e}")

    threshold = args.fail_under if args.fail_under is not None else settings.fail_under_score
    if global_score < threshold:
        logger.error(f"Score {global_score} is below the threshold of {threshold}. Failing.")
        sys.exit(1)

if __name__ == "__main__":
    main()
