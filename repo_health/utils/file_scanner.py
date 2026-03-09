import os
from pathlib import Path

def find_python_files(root_path: Path) -> list[Path]:
    """Find all python files ignoring virtual environments and hidden directories."""
    ignored_dirs = {'.git', '.venv', 'venv', 'env', '__pycache__', '.tox', '.pytest_cache', 'node_modules'}
    python_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs and not d.startswith('.')]
        for f in filenames:
            if f.endswith('.py'):
                python_files.append(Path(dirpath) / f)
    return python_files
