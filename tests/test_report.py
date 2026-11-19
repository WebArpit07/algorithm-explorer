"""
Unit and integration tests for Milestone M5 LaTeX Report & Asset Pipeline.
Verifies LaTeX sources, style packages, bibliography, table generators,
Overleaf distribution zip, and cross-reference integrity.
"""

from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = PROJECT_ROOT / "latex"
CHAPTERS_DIR = LATEX_DIR / "chapters"
TABLES_DIR = LATEX_DIR / "tables"
FIGURES_DIR = LATEX_DIR / "figures"
OVERLEAF_ZIP = PROJECT_ROOT / "Algorithm_Explorer_Report_Overleaf.zip"

EXPECTED_CHAPTERS = [
    "01_introduction.tex",
    "02_fundamentals_of_algorithms.tex",
    "03_growth_of_functions.tex",
    "04_asymptotic_notations.tex",
    "05_complexity_of_algorithms.tex",
    "06_analytical_study_of_algorithms.tex",
    "07_experimental_methodology.tex",
    "08_experimental_results.tex",
    "09_comparative_analysis.tex",
    "10_conclusion.tex",
    "appendix_a_code.tex",
    "appendix_b_tables.tex",
    "appendix_c_outputs.tex",
    "appendix_d_reproduction.tex",
]


def test_master_latex_files_exist():
    """Verify master LaTeX files and style definitions exist."""
    master = PROJECT_ROOT / "Algorithm_Explorer_Report.tex"
    assert master.is_file(), "Algorithm_Explorer_Report.tex not found in project root"
    assert master.stat().st_size > 1000, "Algorithm_Explorer_Report.tex appears incomplete"

    standalone = PROJECT_ROOT / "Algorithm_Explorer_Report_Standalone.tex"
    assert standalone.is_file(), "Algorithm_Explorer_Report_Standalone.tex not found"
    assert standalone.stat().st_size > 50000, "Algorithm_Explorer_Report_Standalone.tex appears incomplete"

    config = LATEX_DIR / "config.tex"
    assert config.is_file(), "latex/config.tex not found"

    style = LATEX_DIR / "styles" / "academic_report.sty"
    assert style.is_file(), "latex/styles/academic_report.sty not found"

    bib = LATEX_DIR / "references.bib"
    assert bib.is_file(), "latex/references.bib not found"
    bib_text = bib.read_text(encoding="utf-8")
    assert "rosen2019discrete" in bib_text, "Rosen citation missing from references.bib"
    assert "cormen2022introduction" in bib_text, "CLRS citation missing from references.bib"


def test_all_14_chapters_exist():
    """Verify all 10 core chapters and 4 appendices exist and have content."""
    for ch in EXPECTED_CHAPTERS:
        ch_path = CHAPTERS_DIR / ch
        assert ch_path.is_file(), f"Missing required chapter: {ch}"
        content = ch_path.read_text(encoding="utf-8")
        assert len(content.strip()) > 200, f"Chapter {ch} is unexpectedly short"


def test_prepare_report_assets_execution():
    """Verify prepare_report_assets.py executes cleanly and outputs valid tables."""
    script = PROJECT_ROOT / "scripts" / "prepare_report_assets.py"
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert res.returncode == 0, f"prepare_report_assets failed: {res.stderr}"

    expected_tables = [
        "growth_functions_table.tex",
        "search_worst_summary_table.tex",
        "sorting_random_summary_table.tex",
        "metadata_table.tex",
    ]
    for tbl in expected_tables:
        tbl_path = TABLES_DIR / tbl
        assert tbl_path.is_file(), f"Expected table {tbl} was not generated"
        text = tbl_path.read_text(encoding="utf-8")
        assert "\\begin{tabular}" in text or "\\begin{tabular*兼" or "tabular" in text


def test_figure_assets_synchronized():
    """Verify all 9 publication figures exist in both PDF and PNG formats in latex/figures/."""
    for i in range(1, 10):
        pdf_name = f"figure{i}_"
        matches_pdf = list(FIGURES_DIR.glob(f"{pdf_name}*.pdf"))
        assert len(matches_pdf) == 1, f"Missing PDF for figure {i} in latex/figures/"
        png_name = f"figure{i}_"
        matches_png = list(FIGURES_DIR.glob(f"{png_name}*.png"))
        assert len(matches_png) == 1, f"Missing PNG for figure {i} in latex/figures/"


def test_overleaf_zip_package_integrity():
    """Verify Overleaf zip package exists, is valid, and contains all needed assets."""
    assert OVERLEAF_ZIP.is_file(), "Algorithm_Explorer_Report_Overleaf.zip does not exist"
    assert OVERLEAF_ZIP.stat().st_size > 100_000, "Overleaf zip is smaller than expected"

    with zipfile.ZipFile(OVERLEAF_ZIP, "r") as z:
        names = z.namelist()
        assert "main.tex" in names
        assert "Algorithm_Explorer_Report.tex" in names
        assert "latex/config.tex" in names
        assert "latex/references.bib" in names
        assert "latex/styles/academic_report.sty" in names
        for ch in EXPECTED_CHAPTERS:
            assert f"latex/chapters/{ch}" in names, f"Chapter {ch} missing from Overleaf zip"
        figures = [n for n in names if n.startswith("latex/figures/") and (n.endswith(".pdf") or n.endswith(".png"))]
        assert len(figures) == 18, f"Expected 18 figure files in zip, found {len(figures)}"
