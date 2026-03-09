# Repo Health

Repo Health is a Python CLI that analyzes repository maintainability using static analysis.

It evaluates projects by detecting complexity issues, test presence, circular dependencies, and missing architectural standards. Rather than linting syntax, it uses heuristics to surface structural technical debt across a codebase and calculates an aggregate maintainability score.

## Installation

Install using pip:

```bash
pip install repo-health
```

Or install from source:

```bash
git clone https://github.com/NarimaneBr/repo-health.git
cd repo-health
pip install -e .
```

## Usage

Analyze the current directory:

```bash
repo-health .
```

Generate a markdown report and a repository badge SVG:

```bash
repo-health . --md --badge
```

Analyze only files changed compared to a specific Git branch (useful for pull requests):

```bash
repo-health . --diff main
```

Identify hotspots by cross-referencing cyclomatic complexity with Git commit frequency:

```bash
repo-health . --hotspots
```

Generate an architecture dependency graph (requires `graphviz`):

```bash
repo-health . --graph
```

## Example output

```text
╭─ Repository Health Report ─╮
│ Score: 87/100              │
╰────────────────────────────╯

Metrics
-------
  Avg complexity                  3.2
  Circular dependencies count     0
  Test ratio                      0.30

Code Hotspots
=============
fastapi/routing.py
  complexity: 42
  commits: 156
  hotspot score: HIGH (6552 pts)
```

## How scoring works

The tool assigns a global score between 0 and 100 based on the weighted aggregation of multiple heuristics:

- **Cyclomatic Complexity**: Penalizes projects where the average cyclomatic complexity (computed via `radon`) exceeds a baseline.
- **Function Size**: Deducts points for functions longer than 80 lines (parsed via Python `ast`).
- **Test Ratio**: Evaluates the ratio of detected test files against standard code files.
- **Dependencies**: Penalizes the detection of circular import cycles (computed via `networkx`).
- **Structure**: Checks for the existence of standard files (e.g., `README.md`, `tests/` directory).

You can configure thresholds globally by creating a `repo-health.toml` file in your repository base:

```toml
max_function_lines = 80
max_complexity = 10
min_test_ratio = 0.2
fail_under_score = 70
```

## CI usage

Repo Health can run in CI pipelines to block merging if a project's maintainability score degrades. Use the `--fail-under` flag. If the computed score is lower than the threshold, the process exits with code 1.

Example GitHub Actions workflow (`.github/workflows/repo-health.yml`):

```yaml
name: Repo Health Check

on: [push, pull_request]

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install
        run: pip install repo-health
      - name: Run analysis
        run: repo-health . --fail-under 70
```

## Limitations

- **Heuristic based**: Metrics like test ratio and hotspots rely on heuristics. The test ratio is calculated purely on file counts, not line coverage or branch execution.
- **Dependency graph limits**: Circular dependency detection relies on static AST parsing of local modules. It may not resolve complex dynamic imports, `sys.path` modifications, or aliased re-exports.
- **Python only**: Currently, the AST-based function analysis and import parsers support only Python source code formatting.

## Development

To develop or test locally:

```bash
git clone https://github.com/NarimaneBr/repo-health.git
cd repo-health
pip install -e .
pytest
```

## License

MIT License.
