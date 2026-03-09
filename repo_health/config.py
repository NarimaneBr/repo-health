from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

@dataclass
class Settings:
    max_complexity: int = 10
    max_function_lines: int = 80
    min_test_ratio: float = 0.2
    fail_under_score: int = 0

def load_settings(root_path: Path) -> Settings:
    settings = Settings()
    config_path = root_path / "repo-health.toml"
    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                user_config = tomllib.load(f)
                for key, value in user_config.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)
        except Exception:
            pass
    return settings
