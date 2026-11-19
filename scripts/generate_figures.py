"""Batch publication figure generator for Algorithm Explorer.

Reads processed empirical benchmark summaries from `data/processed/` and
synthesizes all 9 publication-grade figures in dual format (.pdf vector and
300 DPI .png raster) into `figures/`.

Usage:
    python scripts/generate_figures.py [--output-dir figures]
"""

from __future__ import annotations

import argparse
import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd

from src.visualization.plots import (
    compute_growth_table,
    plot_figure1_common_growth_functions,
    plot_figure2_growth_hierarchy_log_scale,
    plot_figure3_search_operation_counts,
    plot_figure4_search_execution_times,
    plot_figure5_sorting_operation_counts,
    plot_figure6_sorting_execution_times,
    plot_figure7_insertion_sort_arrangements,
    plot_figure8_bubble_sort_arrangements,
    plot_figure9_theoretical_vs_experimental,
)


def generate_all_figures(output_dir: str = "figures") -> None:
    """Generates and saves all 9 academic figures."""
    full_output_dir = os.path.join(PROJECT_ROOT, output_dir)
    os.makedirs(full_output_dir, exist_ok=True)

    search_summary_path = os.path.join(PROJECT_ROOT, "data", "processed", "search_benchmark_summary.csv")
    sorting_summary_path = os.path.join(PROJECT_ROOT, "data", "processed", "sorting_benchmark_summary.csv")
    growth_path = os.path.join(PROJECT_ROOT, "data", "processed", "growth_functions.csv")

    if not os.path.exists(search_summary_path) or not os.path.exists(sorting_summary_path):
        print("ERROR: Processed benchmark datasets not found.")
        print("Please run benchmarks first: python scripts/run_benchmarks.py")
        sys.exit(1)

    print("=" * 70)
    print("ALGORITHM EXPLORER — PUBLICATION FIGURE GENERATION")
    print(f"Target Output Directory: {os.path.relpath(full_output_dir, PROJECT_ROOT)}")
    print("=" * 70)

    # Ingest data
    search_df = pd.read_csv(search_summary_path)
    sorting_df = pd.read_csv(sorting_summary_path)
    if not os.path.exists(growth_path):
        compute_growth_table(growth_path)

    generated_manifest = []

    # FIGURE 1
    print("\nGenerating Figure 1: Common Growth Functions...")
    pdf, png = plot_figure1_common_growth_functions(full_output_dir)
    generated_manifest.append(("Figure 1", "Common Growth Functions (Linear)", pdf, png))

    # FIGURE 2
    print("Generating Figure 2: Growth Hierarchy (Semi-Log Scale)...")
    pdf, png = plot_figure2_growth_hierarchy_log_scale(full_output_dir)
    generated_manifest.append(("Figure 2", "Growth Hierarchy (Semi-Log Scale)", pdf, png))

    # FIGURE 3
    print("Generating Figure 3: Linear vs. Binary Search Operation Counts...")
    pdf, png = plot_figure3_search_operation_counts(search_df, full_output_dir)
    generated_manifest.append(("Figure 3", "Search Operation Counts", pdf, png))

    # FIGURE 4
    print("Generating Figure 4: Linear vs. Binary Search Execution Times...")
    pdf, png = plot_figure4_search_execution_times(search_df, full_output_dir)
    generated_manifest.append(("Figure 4", "Search Execution Times", pdf, png))

    # FIGURE 5
    print("Generating Figure 5: Bubble vs. Insertion Sort Operation Counts...")
    pdf, png = plot_figure5_sorting_operation_counts(sorting_df, full_output_dir)
    generated_manifest.append(("Figure 5", "Sorting Operation Counts", pdf, png))

    # FIGURE 6
    print("Generating Figure 6: Bubble vs. Insertion Sort Execution Times...")
    pdf, png = plot_figure6_sorting_execution_times(sorting_df, full_output_dir)
    generated_manifest.append(("Figure 6", "Sorting Execution Times", pdf, png))

    # FIGURE 7
    print("Generating Figure 7: Insertion Sort Across Arrangements...")
    pdf, png = plot_figure7_insertion_sort_arrangements(sorting_df, full_output_dir)
    generated_manifest.append(("Figure 7", "Insertion Sort Arrangements", pdf, png))

    # FIGURE 8
    print("Generating Figure 8: Bubble Sort Invariance and Swaps...")
    pdf, png = plot_figure8_bubble_sort_arrangements(sorting_df, full_output_dir)
    generated_manifest.append(("Figure 8", "Bubble Sort Invariance and Swaps", pdf, png))

    # FIGURE 9
    print("Generating Figure 9: Theoretical vs. Experimental Telemetry...")
    pdf, png = plot_figure9_theoretical_vs_experimental(search_df, sorting_df, full_output_dir)
    generated_manifest.append(("Figure 9", "Theoretical vs. Experimental Overlay", pdf, png))

    print("\n" + "=" * 70)
    print("FIGURE GENERATION SUMMARY:")
    print("=" * 70)
    for fig_id, desc, pdf_f, png_f in generated_manifest:
        pdf_size = os.path.getsize(pdf_f) / 1024
        png_size = os.path.getsize(png_f) / 1024
        print(f"{fig_id:<10} | {desc:<40} | PDF: {pdf_size:>6.1f} KB | PNG: {png_size:>6.1f} KB")
    print("=" * 70)
    print(f"Total Figures Created: {len(generated_manifest)} (18 files: 9 PDF + 9 PNG)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate publication-grade figures.")
    parser.add_argument("--output-dir", type=str, default="figures", help="Directory to save figures (default: figures)")
    args = parser.parse_args()

    generate_all_figures(output_dir=args.output_dir)
