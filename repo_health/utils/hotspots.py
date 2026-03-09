import subprocess
from collections import Counter
from pathlib import Path

def get_commit_counts(root_path: Path) -> Counter:
    """Gets the number of commits pointing to each file in this git repo."""
    try:
        output = subprocess.check_output(
            ["git", "log", "--name-only", "--pretty=format:"],
            cwd=str(root_path),
            text=True
        )
        counts = Counter()
        for line in output.splitlines():
            line = line.strip()
            if line and line.endswith('.py'):
                # Store full normalized path strictly matching what complexity analyzer stores
                full_path = str((root_path / line).resolve())
                counts[full_path] += 1
        return counts
    except Exception:
        return Counter()
