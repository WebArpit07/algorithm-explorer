"""Asset preparation script for the Algorithm Explorer LaTeX academic report.

Generates automated, publication-grade LaTeX tables from processed CSV datasets
and copies vector graphics into `latex/figures/` for seamless compilation.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd


def escape_latex(val: object) -> str:
    """Escapes special LaTeX characters in strings."""
    s = str(val)
    return (
        s.replace("\\", r"\textbackslash{}")
        .replace("_", r"\_")
        .replace("%", r"\%")
        .replace("&", r"\&")
        .replace("#", r"\#")
    )


def generate_latex_tables() -> None:
    """Generates modular LaTeX table files in latex/tables/."""
    tables_dir = PROJECT_ROOT / "latex" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    # 1. Growth functions table
    growth_csv = PROJECT_ROOT / "data" / "processed" / "growth_functions.csv"
    if growth_csv.exists():
        gdf = pd.read_csv(growth_csv)
        lines = [
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Numerical Evaluation of Standard Growth Functions (Rosen §3.2)}",
            r"\label{tab:growth_functions}",
            r"\small",
            r"\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}rrrrrrrr}",
            r"\toprule",
            r"$n$ & $\mathcal{O}(1)$ & $\mathcal{O}(\log_2 n)$ & $\mathcal{O}(n)$ & $\mathcal{O}(n \log_2 n)$ & $\mathcal{O}(n^2)$ & $\mathcal{O}(2^n)$ & $\mathcal{O}(n!)$ \\",
            r"\midrule",
        ]
        for _, r in gdf.iterrows():
            n = int(r["n"])
            c_val = "1"
            log_v = f"{r['logarithmic_log2_n']:.2f}"
            lin_v = f"{int(r['linear_n'])}"
            linlog_v = f"{r['linearithmic_n_log2_n']:.2f}"
            quad_v = f"{int(r['quadratic_n2'])}"
            exp_v = f"{r['exponential_2n']:.2e}" if r['exponential_2n'] > 1e6 else f"{int(r['exponential_2n'])}"
            fact_v = f"{r['factorial_n_fact']:.2e}" if r['factorial_n_fact'] > 1e6 else f"{int(r['factorial_n_fact'])}"
            lines.append(f"{n} & {c_val} & {log_v} & {lin_v} & {linlog_v} & {quad_v} & {exp_v} & {fact_v} \\\\")
        lines.extend([
            r"\bottomrule",
            r"\end{tabular*}",
            r"\end{table}",
        ])
        with open(tables_dir / "growth_functions_table.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("  Generated: latex/tables/growth_functions_table.tex")

    # 2. Search Worst-Case Summary Table
    search_csv = PROJECT_ROOT / "data" / "processed" / "search_benchmark_summary.csv"
    if search_csv.exists():
        sdf = pd.read_csv(search_csv)
        worst_sdf = sdf[sdf["scenario"] == "missing"].sort_values(["input_size", "algorithm"])
        lines = [
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Searching Algorithms Worst-Case Empirical Telemetry (Missing Target)}",
            r"\label{tab:search_worst_summary}",
            r"\small",
            r"\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrr}",
            r"\toprule",
            r"\textbf{Algorithm} & $n$ & \textbf{Key Comps} & \textbf{Median ($\mu$s)} & \textbf{Mean ($\mu$s)} & \textbf{Std Dev ($\mu$s)} & \textbf{IQR ($\mu$s)} \\",
            r"\midrule",
        ]
        for _, r in worst_sdf.iterrows():
            alg = "Linear Search" if r["algorithm"] == "linear_search" else "Binary Search"
            n_val = int(r["input_size"])
            comps = int(r["key_comparisons"])
            med_us = f"{r['median_duration_ns'] / 1000:.2f}"
            mean_us = f"{r['mean_duration_ns'] / 1000:.2f}"
            std_us = f"{r['std_dev_duration_ns'] / 1000:.2f}"
            iqr_us = f"{r['iqr_duration_ns'] / 1000:.2f}"
            lines.append(f"{alg} & {n_val} & {comps} & {med_us} & {mean_us} & {std_us} & {iqr_us} \\\\")
        lines.extend([
            r"\bottomrule",
            r"\end{tabular*}",
            r"\end{table}",
        ])
        with open(tables_dir / "search_worst_summary_table.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("  Generated: latex/tables/search_worst_summary_table.tex")

    # 3. Sorting Summary Table (Random Permutations)
    sort_csv = PROJECT_ROOT / "data" / "processed" / "sorting_benchmark_summary.csv"
    if sort_csv.exists():
        sqdf = pd.read_csv(sort_csv)
        rand_sqdf = sqdf[sqdf["arrangement"] == "random"].sort_values(["input_size", "algorithm"])
        lines = [
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Sorting Algorithms Empirical Telemetry on Random Permutations}",
            r"\label{tab:sorting_random_summary}",
            r"\small",
            r"\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrr}",
            r"\toprule",
            r"\textbf{Algorithm} & $n$ & \textbf{Comparisons} & \textbf{Swaps / Shifts} & \textbf{Median (ms)} & \textbf{Mean (ms)} & \textbf{Std Dev (ms)} \\",
            r"\midrule",
        ]
        for _, r in rand_sqdf.iterrows():
            alg = "Bubble Sort" if r["algorithm"] == "bubble_sort" else "Insertion Sort"
            n_val = int(r["input_size"])
            comps = int(r["element_comparisons"])
            moves = int(r["swaps"]) if r["algorithm"] == "bubble_sort" else int(r["right_shifts"])
            med_ms = f"{r['median_duration_ns'] / 1e6:.2f}"
            mean_ms = f"{r['mean_duration_ns'] / 1e6:.2f}"
            std_ms = f"{r['std_dev_duration_ns'] / 1e6:.2f}"
            lines.append(f"{alg} & {n_val} & {comps:,} & {moves:,} & {med_ms} & {mean_ms} & {std_ms} \\\\")
        lines.extend([
            r"\bottomrule",
            r"\end{tabular*}",
            r"\end{table}",
        ])
        with open(tables_dir / "sorting_random_summary_table.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("  Generated: latex/tables/sorting_random_summary_table.tex")

    # 4. Metadata table
    meta_json = PROJECT_ROOT / "data" / "processed" / "benchmark_metadata.json"
    if meta_json.exists():
        with open(meta_json, "r") as f:
            meta = json.load(f)
        
        timer_clean = escape_latex(meta.get('timing_timer', 'time.perf_counter_ns'))
        seed_clean = escape_latex(meta.get('random_seed', '42'))
        os_clean = escape_latex(f"{meta.get('operating_system')} {meta.get('os_release')}")
        arch_clean = escape_latex(meta.get('machine_architecture', 'AMD64'))
        proc_clean = escape_latex(meta.get('processor', ''))
        py_clean = escape_latex(f"{meta.get('python_version', '').split()[0]} ({meta.get('python_implementation', 'CPython')})")

        lines = [
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Empirical Hardware, Software, and Benchmark Execution Environment}",
            r"\label{tab:environment_metadata}",
            r"\small",
            r"\begin{tabularx}{\textwidth}{l X}",
            r"\toprule",
            r"\textbf{Environment Parameter} & \textbf{Recorded Value} \\",
            r"\midrule",
            f"Operating System & {os_clean} (Build {meta.get('os_version')}) \\\\",
            f"Host Architecture & {arch_clean} ({proc_clean}) \\\\",
            f"Logical CPU Cores & {meta.get('cpu_count_logical')} Cores \\\\",
            f"Python Runtime & {py_clean} \\\\",
            f"High-Resolution Timer & \\texttt{{{timer_clean}}} (Resolution: {meta.get('timing_resolution_ns')} ns) \\\\",
            f"Replication Factor & $k = {meta.get('repetitions_per_case')}$ Independent Iterations per Configuration \\\\",
            f"Deterministic Seed & \\texttt{{{seed_clean}}} \\\\",
            f"Total Benchmark Suite Duration & {meta.get('benchmark_total_elapsed_sec')} seconds \\\\",
            r"\bottomrule",
            r"\end{tabularx}",
            r"\end{table}",
        ]
        with open(tables_dir / "metadata_table.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("  Generated: latex/tables/metadata_table.tex")


def copy_figures_to_latex() -> None:
    """Copies all vector PDFs and raster PNGs to latex/figures/."""
    src_fig = PROJECT_ROOT / "figures"
    dest_fig = PROJECT_ROOT / "latex" / "figures"
    dest_fig.mkdir(parents=True, exist_ok=True)

    if src_fig.exists():
        for item in src_fig.iterdir():
            if item.is_file():
                shutil.copy2(item, dest_fig / item.name)
        print(f"  Copied {len(list(dest_fig.iterdir()))} figure assets to: latex/figures/")


if __name__ == "__main__":
    print("Preparing LaTeX report tables and assets...")
    generate_latex_tables()
    copy_figures_to_latex()
    print("LaTeX assets preparation complete.")
