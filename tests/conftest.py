
import json
import pytest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "reports" / "quality_results.json"


@pytest.fixture(scope="session")
def quality_results(request):
    """Collect quality results throughout the pytest session."""

    results = []
    request.config._quality_results = results

    return results


def pytest_sessionfinish(session, exitstatus):
    """Save collected quality results after the test session."""

    results = getattr(session.config, "_quality_results", [])

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"\nQuality results saved to: {REPORT_PATH}")
