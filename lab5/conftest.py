import pytest
from pathlib import Path

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"


@pytest.fixture(autouse=True)
def artifacts_dir():
    """Ensure artifacts directory exists."""
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    return ARTIFACTS_DIR
