"""
Integration and validation tests for Milestone M6 Web Dashboard.
Tests HTML structure, CSS rules, JavaScript algorithm implementation,
benchmark data integrity, and GitHub Actions deployment configuration.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
DATA_DIR = DASHBOARD_DIR / "data"
JS_DIR = DASHBOARD_DIR / "js"
CSS_DIR = DASHBOARD_DIR / "css"


def test_dashboard_files_exist():
    """Verify all required dashboard assets and documents exist."""
    assert (DASHBOARD_DIR / "index.html").is_file(), "index.html missing"
    assert (CSS_DIR / "style.css").is_file(), "style.css missing"
    assert (JS_DIR / "algorithms.js").is_file(), "algorithms.js missing"
    assert (JS_DIR / "visualizations.js").is_file(), "visualizations.js missing"
    assert (JS_DIR / "charts.js").is_file(), "charts.js missing"
    assert (JS_DIR / "app.js").is_file(), "app.js missing"
    assert (DATA_DIR / "benchmark_data.json").is_file(), "benchmark_data.json missing"
    assert (DATA_DIR / "benchmark_data.js").is_file(), "benchmark_data.js missing"
    assert (DASHBOARD_DIR / "README.md").is_file(), "dashboard/README.md missing"
    assert (PROJECT_ROOT / ".github" / "workflows" / "deploy.yml").is_file(), "deploy.yml missing"


def test_index_html_structure():
    """Verify semantic sections, lab IDs, and script inclusions in index.html."""
    html = (DASHBOARD_DIR / "index.html").read_text(encoding="utf-8")
    expected_ids = [
        "overview",
        "explorer",
        "searching-lab",
        "sorting-lab",
        "comparison-lab",
        "growth-lab",
        "benchmarks",
        "references",
        "search-algo-select",
        "search-array-container",
        "sort-algo-select",
        "sorting-canvas-container",
        "growth-chart-svg",
        "bm-search-table",
        "bm-sort-table",
    ]
    for eid in expected_ids:
        assert f'id="{eid}"' in html, f"Missing element with ID '{eid}' in index.html"

    # Verify script loading order
    assert 'src="data/benchmark_data.js"' in html
    assert 'src="js/algorithms.js"' in html
    assert 'src="js/visualizations.js"' in html
    assert 'src="js/charts.js"' in html
    assert 'src="js/app.js"' in html


def test_benchmark_data_json_integrity():
    """Verify benchmark_data.json conforms to schema and matches Python M3 telemetry."""
    json_path = DATA_DIR / "benchmark_data.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "metadata" in data
    assert "growth_functions" in data
    assert "search_summary" in data
    assert "sorting_summary" in data
    assert "highlighted_comparisons" in data

    # Verify Inversion Equivalence in data
    inv_data = data["highlighted_comparisons"]["sorting_at_3k"]["inversion_equivalence"]
    assert inv_data["are_equal"] is True
    assert inv_data["bubble_swaps_random"] == inv_data["insertion_shifts_random"] == 2296691


def test_dashboard_algorithms_node_execution():
    """Run Node.js automated test runner for algorithms.js."""
    script = PROJECT_ROOT / "scripts" / "test_dashboard_algorithms.js"
    res = subprocess.run(["node", str(script)], capture_output=True, text=True)
    assert res.returncode == 0, f"Node test runner failed:\n{res.stderr or res.stdout}"
    assert "ALL 5 DASHBOARD ALGORITHM TEST SUITES PASSED!" in res.stdout
