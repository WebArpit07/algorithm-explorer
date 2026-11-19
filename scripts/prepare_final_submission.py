"""Script to construct, sanitize, and verify the clean FINAL_SUBMISSION package.
Follows Faculty Submission Requirements for MSc IT Discrete Mathematics (Rosen Ch. 3).
"""

import os
import shutil
from pathlib import Path
import zipfile

PROJECT_ROOT = Path("D:/DiscreteMathsProject_202612120")
SUBMISSION_DIR = PROJECT_ROOT / "FINAL_SUBMISSION"
ZIP_PATH = PROJECT_ROOT / "Algorithm_Explorer_Final_Submission.zip"

def build_submission():
    print(f"Preparing clean FINAL_SUBMISSION directory at: {SUBMISSION_DIR}")

    # Remove existing directory if present to guarantee zero stale files
    if SUBMISSION_DIR.exists():
        shutil.rmtree(SUBMISSION_DIR)
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Required Deliverable A: Final Academic PDF
    pdf_src = PROJECT_ROOT / "Algorithm_Explorer_Report.pdf"
    if not pdf_src.exists():
        raise FileNotFoundError(f"Missing {pdf_src}")
    shutil.copy2(pdf_src, SUBMISSION_DIR / "Algorithm_Explorer_Report.pdf")
    print("  [OK] Copied Algorithm_Explorer_Report.pdf")

    # 2. Required Deliverable B: Master LaTeX Source
    tex_src = PROJECT_ROOT / "Algorithm_Explorer_Report.tex"
    if not tex_src.exists():
        raise FileNotFoundError(f"Missing {tex_src}")
    shutil.copy2(tex_src, SUBMISSION_DIR / "Algorithm_Explorer_Report.tex")
    print("  [OK] Copied Algorithm_Explorer_Report.tex")

    # 3. Required Deliverable C: Executed Jupyter Notebook
    ipynb_src = PROJECT_ROOT / "notebooks" / "algorithm_explorer.ipynb"
    if not ipynb_src.exists():
        raise FileNotFoundError(f"Missing {ipynb_src}")
    shutil.copy2(ipynb_src, SUBMISSION_DIR / "algorithm_explorer.ipynb")
    print("  [OK] Copied algorithm_explorer.ipynb")

    # 4. LaTeX & Notebook Figure Dependencies
    figures_dest = SUBMISSION_DIR / "figures"
    figures_dest.mkdir(parents=True, exist_ok=True)
    for i in range(1, 10):
        # List of expected filenames
        names = [
            f"figure{i}_common_growth_functions.pdf",
            f"figure{i}_growth_hierarchy_log_scale.pdf",
            f"figure{i}_search_operation_counts.pdf",
            f"figure{i}_search_execution_times.pdf",
            f"figure{i}_sorting_operation_counts.pdf",
            f"figure{i}_sorting_execution_times.pdf",
            f"figure{i}_insertion_sort_arrangements.pdf",
            f"figure{i}_bubble_sort_arrangements.pdf",
            f"figure{i}_theoretical_vs_experimental.pdf",
        ]
        for name in names:
            src = PROJECT_ROOT / "figures" / name
            if src.exists():
                shutil.copy2(src, figures_dest / name)
                # Also copy png companion if present
                png_src = src.with_suffix(".png")
                if png_src.exists():
                    shutil.copy2(png_src, figures_dest / png_src.name)
                print(f"  [OK] Copied figure asset: {name}")

    # 5. Supporting Python Modules: src/
    src_dest = SUBMISSION_DIR / "src"
    for module in ["algorithms", "benchmarking", "visualization"]:
        mod_src = PROJECT_ROOT / "src" / module
        mod_dest = src_dest / module
        shutil.copytree(
            mod_src,
            mod_dest,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
        )
        print(f"  [OK] Copied module: src/{module}")
    # Root __init__.py for src
    init_src = PROJECT_ROOT / "src" / "__init__.py"
    if init_src.exists():
        shutil.copy2(init_src, src_dest / "__init__.py")

    # 6. Supporting Benchmark Datasets: data/
    data_dest = SUBMISSION_DIR / "data"
    for sub in ["raw", "processed"]:
        data_src = PROJECT_ROOT / "data" / sub
        sub_dest = data_dest / sub
        shutil.copytree(data_src, sub_dest)
        print(f"  [OK] Copied dataset directory: data/{sub}")

    # 7. Requirements specification
    req_src = PROJECT_ROOT / "requirements.txt"
    if req_src.exists():
        shutil.copy2(req_src, SUBMISSION_DIR / "requirements.txt")
        print("  [OK] Copied requirements.txt")

    print("\nFINAL_SUBMISSION directory successfully built.")

if __name__ == "__main__":
    build_submission()
