"""
Algorithm Explorer — Automated LaTeX Report Builder & Overleaf Packager
Milestone M5 — Academic Report Compilation and Asset Packaging System

This script verifies all LaTeX report assets, executes preparation routines,
detects available TeX compilation engines, compiles the academic monograph to PDF
if an engine is present, and packages a complete, self-contained Overleaf bundle.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


# Project Root Directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = PROJECT_ROOT / "latex"
FIGURES_DIR = LATEX_DIR / "figures"
TABLES_DIR = LATEX_DIR / "tables"
CHAPTERS_DIR = LATEX_DIR / "chapters"
MAIN_TEX = PROJECT_ROOT / "Algorithm_Explorer_Report.tex"
MAIN_TEX_ALT = LATEX_DIR / "main.tex"
OUTPUT_PDF = PROJECT_ROOT / "Algorithm_Explorer_Report.pdf"
OVERLEAF_ZIP = PROJECT_ROOT / "Algorithm_Explorer_Report_Overleaf.zip"

REQUIRED_CHAPTERS = [
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

AUX_EXTENSIONS = [
    ".aux", ".bbl", ".blg", ".log", ".out", ".toc",
    ".lof", ".lot", ".fls", ".fdb_latexmk", ".synctex.gz"
]


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Execute a system command and return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd or PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"


def verify_prerequisites() -> bool:
    """Verify that all prerequisite source files, chapters, and templates exist."""
    print("=" * 70)
    print("STEP 1: Verifying LaTeX Report Prerequisites")
    print("=" * 70)

    missing = []
    if not MAIN_TEX.is_file():
        missing.append(str(MAIN_TEX))
    if not (LATEX_DIR / "config.tex").is_file():
        missing.append(str(LATEX_DIR / "config.tex"))
    if not (LATEX_DIR / "styles" / "academic_report.sty").is_file():
        missing.append(str(LATEX_DIR / "styles" / "academic_report.sty"))
    if not (LATEX_DIR / "references.bib").is_file():
        missing.append(str(LATEX_DIR / "references.bib"))

    for ch in REQUIRED_CHAPTERS:
        ch_path = CHAPTERS_DIR / ch
        if not ch_path.is_file():
            missing.append(str(ch_path))

    if missing:
        print("[ERROR] Missing required LaTeX source files:")
        for m in missing:
            print(f"  - {m}")
        return False

    print(f"  [OK] Master LaTeX document verified: {MAIN_TEX.name}")
    print(f"  [OK] LaTeX style package verified: academic_report.sty")
    print(f"  [OK] Bibliography database verified: references.bib")
    print(f"  [OK] All {len(REQUIRED_CHAPTERS)} modular chapters verified in {CHAPTERS_DIR.name}/")
    return True


def prepare_assets() -> bool:
    """Run prepare_report_assets.py to ensure fresh tables and figure synchronization."""
    print("\n" + "=" * 70)
    print("STEP 2: Synchronizing LaTeX Tables and Figures")
    print("=" * 70)

    prep_script = PROJECT_ROOT / "scripts" / "prepare_report_assets.py"
    if not prep_script.is_file():
        print(f"[ERROR] Asset preparation script not found: {prep_script}")
        return False

    ret, stdout, stderr = run_command([sys.executable, str(prep_script)])
    if ret != 0:
        print(f"[ERROR] Asset preparation failed with return code {ret}:")
        print(stderr or stdout)
        return False

    for line in stdout.strip().splitlines():
        print(f"  {line}")
    return True


def detect_tex_engine() -> str | None:
    """Detect available LaTeX compilation engines on PATH."""
    engines = ["latexmk", "pdflatex", "xelatex", "lualatex"]
    for eng in engines:
        path = shutil.which(eng)
        if path:
            return eng
    return None


def clean_auxiliary_files():
    """Remove LaTeX auxiliary files from project root and latex directory."""
    print("\n" + "=" * 70)
    print("Cleaning Auxiliary Build Files")
    print("=" * 70)
    cleaned = 0
    for directory in [PROJECT_ROOT, LATEX_DIR]:
        for item in directory.glob("*"):
            if item.is_file() and item.suffix.lower() in AUX_EXTENSIONS:
                try:
                    item.unlink()
                    cleaned += 1
                except Exception as e:
                    print(f"  [WARN] Failed to delete {item.name}: {e}")
    print(f"  Removed {cleaned} auxiliary build file(s).")


def build_overleaf_package() -> Path:
    """Create a self-contained, 1-click Overleaf distribution zip archive."""
    print("\n" + "=" * 70)
    print("Packaging Self-Contained Overleaf Distribution Archive")
    print("=" * 70)

    if OVERLEAF_ZIP.exists():
        OVERLEAF_ZIP.unlink()

    file_count = 0
    with zipfile.ZipFile(OVERLEAF_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Include main master files at root of zip for seamless Overleaf detection
        zipf.write(MAIN_TEX, arcname="Algorithm_Explorer_Report.tex")
        zipf.write(MAIN_TEX, arcname="main.tex")
        standalone_path = PROJECT_ROOT / "Algorithm_Explorer_Report_Standalone.tex"
        if standalone_path.is_file():
            zipf.write(standalone_path, arcname="Algorithm_Explorer_Report_Standalone.tex")
            file_count += 1
        file_count += 2

        # Include root mirrors of style, bibliography, and config for flat compilers
        if (LATEX_DIR / "styles" / "academic_report.sty").is_file():
            zipf.write(LATEX_DIR / "styles" / "academic_report.sty", arcname="academic_report.sty")
            file_count += 1
        if (LATEX_DIR / "references.bib").is_file():
            zipf.write(LATEX_DIR / "references.bib", arcname="references.bib")
            file_count += 1
        if (LATEX_DIR / "config.tex").is_file():
            zipf.write(LATEX_DIR / "config.tex", arcname="config.tex")
            file_count += 1

        # Include latex/ subtree
        for root, _, files in os.walk(LATEX_DIR):
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix.lower() in AUX_EXTENSIONS:
                    continue
                rel_path = filepath.relative_to(PROJECT_ROOT)
                zipf.write(filepath, arcname=str(rel_path).replace("\\", "/"))
                file_count += 1

        # Also include figures/ at root so \graphicspath{{latex/figures/}{figures/}} resolves anywhere
        fig_dir = PROJECT_ROOT / "figures"
        if fig_dir.is_dir():
            for fig_file in fig_dir.glob("*"):
                if fig_file.is_file():
                    zipf.write(fig_file, arcname=f"figures/{fig_file.name}")
                    file_count += 1

    zip_size_mb = OVERLEAF_ZIP.stat().st_size / (1024 * 1024)
    print(f"  [SUCCESS] Overleaf archive packaged: {OVERLEAF_ZIP.name}")
    print(f"  Archive Size: {zip_size_mb:.2f} MB")
    print(f"  Files Included: {file_count} (source tex, bib, styles, tables, and vector/raster figures)")
    print(f"  Destination Path: {OVERLEAF_ZIP.resolve()}")
    return OVERLEAF_ZIP


def compile_pdf(engine: str) -> bool:
    """Compile LaTeX document to PDF using detected engine."""
    print("\n" + "=" * 70)
    print(f"STEP 3: Compiling Master LaTeX Report with '{engine}'")
    print("=" * 70)

    master_stem = "Algorithm_Explorer_Report"

    if engine == "latexmk":
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"{master_stem}.tex"]
        print(f"  Executing: {' '.join(cmd)}")
        ret, stdout, stderr = run_command(cmd, cwd=PROJECT_ROOT)
        if ret != 0:
            print("[ERROR] latexmk compilation failed:")
            print(stdout[-1500:])
            return False
    else:
        # Standard multi-pass cycle: Engine -> BibTeX -> Engine -> Engine
        passes = [
            ([engine, "-interaction=nonstopmode", "-halt-on-error", f"{master_stem}.tex"], "Pass 1/3 (Initial compilation)"),
            (["bibtex", master_stem], "BibTeX Citation Processing"),
            ([engine, "-interaction=nonstopmode", "-halt-on-error", f"{master_stem}.tex"], "Pass 2/3 (Resolving cross-references)"),
            ([engine, "-interaction=nonstopmode", "-halt-on-error", f"{master_stem}.tex"], "Pass 3/3 (Finalizing TOC, LOT, LOF)"),
        ]

        for cmd, label in passes:
            print(f"  Running: {label} ({cmd[0]})...")
            ret, stdout, stderr = run_command(cmd, cwd=PROJECT_ROOT)
            if ret != 0 and cmd[0] != "bibtex":
                print(f"[ERROR] {label} failed with exit code {ret}:")
                # Print last lines of log
                log_file = PROJECT_ROOT / f"{master_stem}.log"
                if log_file.is_file():
                    with open(log_file, "r", encoding="utf-8", errors="ignore") as lf:
                        lines = lf.readlines()
                        print("".join(lines[-30:]))
                return False

    if OUTPUT_PDF.is_file() and OUTPUT_PDF.stat().st_size > 0:
        pdf_size_mb = OUTPUT_PDF.stat().st_size / (1024 * 1024)
        print(f"\n  [SUCCESS] Academic PDF generated: {OUTPUT_PDF.name}")
        print(f"  PDF File Size: {pdf_size_mb:.2f} MB")
        print(f"  Destination Path: {OUTPUT_PDF.resolve()}")
        return True
    else:
        print("[ERROR] PDF was not generated or has zero bytes.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Algorithm Explorer LaTeX Report Builder")
    parser.add_argument("--clean", action="store_true", help="Clean LaTeX auxiliary files")
    parser.add_argument("--package", action="store_true", help="Package Overleaf zip archive only")
    parser.add_argument("--compile", action="store_true", help="Force PDF compilation attempt")
    args = parser.parse_args()

    if args.clean:
        clean_auxiliary_files()
        return 0

    if not verify_prerequisites():
        return 1

    if not prepare_assets():
        return 1

    # Always generate/update the Overleaf package so users have instant access
    build_overleaf_package()

    if args.package:
        print("\nPackage operation requested. Build complete.")
        return 0

    engine = detect_tex_engine()
    if engine:
        print(f"\nDetected local TeX engine: '{engine}'")
        success = compile_pdf(engine)
        if success:
            print("\n[COMPLETE] Report compilation finished successfully.")
            return 0
        else:
            print("\n[WARNING] Local compilation encountered errors. Overleaf bundle is ready as fallback.")
            return 1
    else:
        print("\n" + "=" * 70)
        print("LOCAL TEX ENGINE DETECTION STATUS: NONE DETECTED ON PATH")
        print("=" * 70)
        print("No local LaTeX engine (pdflatex, latexmk, xelatex, lualatex) was detected on your Windows PATH.")
        print("\nTo view and generate the publication PDF, you have two guaranteed methods:\n")
        print("METHOD 1: 1-Click Upload to Overleaf (Recommended - No Local Install Needed)")
        print("-" * 70)
        print(f"1. Open https://www.overleaf.com/project in your web browser.")
        print(f"2. Click 'New Project' -> 'Upload Project'.")
        print(f"3. Select the packaged zip archive created by this script:")
        print(f"   {OVERLEAF_ZIP.resolve()}")
        print(f"4. Click 'Recompile'. Overleaf automatically compiles with standard TeX Live.")
        print("\nMETHOD 2: Install Local TeX Engine (Windows)")
        print("-" * 70)
        print("If you prefer local PDF compilation, install MiKTeX or TeX Live via Windows Package Manager:")
        print("   winget install MiKTeX.MiKTeX")
        print("   -- OR --")
        print("   choco install miktex")
        print("After installation, reopen your PowerShell/Command Prompt terminal and run:")
        print("   python scripts/build_report.py")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    sys.exit(main())
