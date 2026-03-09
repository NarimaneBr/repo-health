# 🩺 Repo Health

**A highly attractive open-source developer tool to analyze your repository's health in seconds.**

![Repo Health](https://img.shields.io/badge/repo--health-100-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Get actionable insights to improve your codebase, detect complex hotspots, and generate beautiful graphs. Built to feel like a real engineering devtool.

*Topics: `static-analysis` `code-quality` `python` `developer-tools` `cli-tool` `software-quality`*

---

### [Animated Demo Placeholder - Imagine a beautiful terminal GIF here]

---

## ✨ Features

- 🕵️ **Code Hotspot Detection**: Cross-references cyclomatic complexity with Git commit history (`--hotspots`) to find your most risky files!
- 🕸️ **Architecture Dependency Graph**: Parses Python imports and maps an SVG graph of your module layout (`--graph`).
- ⚡ **Pull Request / Diff Analysis**: Assesses only files modified on your working branch compared to `main` (`--diff main`). 
- 📝 **Markdown Report Generation**: Generates a fast `repo-health-report.md` for PR comments (`--md`).
- 🎖️ **Badge Generator**: Want to show off your repo score? Generate a `repo-health-badge.svg` directly (`--badge`).
- 🚦 **CI Pipeline Ready**: Break your un-healthy pipelines flawlessly with (`--fail-under 70`).
- 🎨 **Beautiful Developer Experience**: Powered by `rich` to print stunning health metrics.

---

## 🚀 Installation

Ensure you have Python 3.10+, and from the project root simply install via `pip`:

```bash
pip install repo-health
```
*(Or from source)*:
```bash
git clone https://github.com/NarimaneBr/repo-health.git
cd repo-health
pip install -e .
```

---

## 💻 Usage

Analyze your current project working directory:
```bash
repo-health .
```

### Advanced Analytics

**Discover Risky Hotspots** (the files modified the most often that are highly complex):
```bash
repo-health . --hotspots
```

**Generate Architecture Graph** (Requires `graphviz` to be installed on your system):
```bash
repo-health . --graph
```

**Pull Request Workflow** (Only analyze files differing from the `main` branch):
```bash
repo-health . --diff main
```

**Generate Markdown Report** (Outputs `repo-health-report.md`):
```bash
repo-health . --md
```

**Generate the Repo Health Badge** (Outputs `repo-health-badge.svg`):
```bash
repo-health . --badge
```

### Example Usage: Analyzing FastAPI

Curious about how a major Open-Source project performs? Let's analyze FastAPI:

```bash
git clone https://github.com/fastapi/fastapi.git
repo-health fastapi/ --hotspots --fail-under 70
```

*Output Example:*
```
╭─ Repository Health Report ─╮
│ Score: 87/100              │
╰────────────────────────────╯

Metrics
-------
  Avg complexity                  3.2
  Circular dependencies count     0
  Test ratio                      30%

Code Hotspots
=============
fastapi/routing.py
  complexity: 42
  commits: 156
  hotspot score: HIGH (6552 pts)
```

---

## ⚙️ Configuration

Customizing thresholds for your team is simple. Create a `repo-health.toml` in your root:

```toml
max_function_lines = 80
max_complexity = 10
min_test_ratio = 0.2
fail_under_score = 60
```

---

## 🤖 CI Integration (GitHub Actions)

Add Repo-Health into your GitHub Actions workflow `.github/workflows/repo-health.yml` so you never merge complex legacy code again! 

```yaml
name: Repo Health Check

on: [push, pull_request]

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0   # Important if you want --hotspots or --diff to access history
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install repo-health
      - name: Run Repo Health
        run: repo-health . --fail-under 70
```

---

## 🏗️ Architecture Design

```
repo-health
│
├── repo_health
│   ├── cli.py            # CLI entrypoint
│   ├── orchestrator.py   # Coordinate analyzers & diff logic
│   ├── scoring.py        # Global score compute definitions
│   ├── models.py         # Strong Data Contracts
│   ├── config.py         # TOML Configuration reader
│   │
│   ├── analyzers         # Extensible plugin-like analyzers
│   │   ├── complexity.py, functions.py, etc...
│   │
│   ├── reporters         # Isolated output strategies
│   │   ├── console.py, badge.py, graph.py, markdown_reporter.py
│   │
│   └── utils             # Generic helpers
```
