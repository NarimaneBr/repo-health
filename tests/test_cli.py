from repo_health.cli import main
import pytest
from unittest.mock import patch

def test_cli():
    with patch("sys.argv", ["repo-health", "--help"]):
        with pytest.raises(SystemExit):
            main()
