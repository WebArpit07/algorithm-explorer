"""Headless automated benchmark execution runner for Algorithm Explorer.

Executes controlled empirical trials for searching (Linear, Binary) and
sorting (Bubble, Insertion) algorithms across calibrated input sizes and
topological arrangements, saving raw and aggregated telemetry to `data/`.

Usage:
    python scripts/run_benchmarks.py [--seed 42] [--reps 30] [--quick]
"""

from __future__ import annotations

import argparse
import os
import sys
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.benchmarking.harness import (
    benchmark_search_scenario,
    benchmark_sorting_scenario,
    run_pilot_benchmark,
)
from src.benchmarking.telemetry import (
    export_metadata_to_json,
    export_summaries_to_csv,
    export_trials_to_csv,
    get_environment_metadata,
)
from src.visualization.plots import compute_growth_table


def run_all_benchmarks(seed: int = 42, repetitions: int = 30, quick: bool = False) -> None:
    """Executes the full suite of reproducible benchmarks."""
    start_time_all = time.perf_counter()
    print("=" * 70)
    print("ALGORITHM EXPLORER — EMPIRICAL BENCHMARKING SUITE")
    print("Academic Reference: Kenneth H. Rosen, Discrete Mathematics (8th Ed.)")
    print(f"Random Seed: {seed} | Repetitions per Configuration: {repetitions}")
    print("=" * 70)

    # 1. Environment & Pilot Verification
    print("\n[1/4] Running Environment Verification and Pilot Benchmark...")
    pilot_results = run_pilot_benchmark()
    for size_label, metrics in pilot_results.items():
        print(f"  Pilot {size_label}: BubbleSort={metrics['bubble_sort_ms']}ms, InsertionSort={metrics['insertion_sort_ms']}ms")

    # 2. Mathematical Growth Functions Data
    print("\n[2/4] Generating Mathematical Growth Table (Rosen §3.2)...")
    growth_csv = os.path.join(PROJECT_ROOT, "data", "processed", "growth_functions.csv")
    growth_df = compute_growth_table(growth_csv)
    print(f"  Growth function table saved to: {os.path.relpath(growth_csv, PROJECT_ROOT)} ({len(growth_df)} rows)")

    # 3. Search Benchmarks
    print("\n[3/4] Executing Search Benchmarks (Linear Search vs. Binary Search)...")
    if quick:
        search_sizes = [100, 1000, 10000]
    else:
        search_sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]

    search_scenarios = ["first", "middle", "last", "missing"]
    search_algorithms = ["linear_search", "binary_search"]

    all_search_trials = []
    all_search_summaries = []

    total_search_configs = len(search_algorithms) * len(search_sizes) * len(search_scenarios)
    current_search_idx = 0

    for alg in search_algorithms:
        for size in search_sizes:
            for scen in search_scenarios:
                current_search_idx += 1
                sys.stdout.write(f"\r  Progress: [{current_search_idx}/{total_search_configs}] {alg} (n={size}, {scen})...")
                sys.stdout.flush()

                trials, summary = benchmark_search_scenario(
                    algorithm_name=alg,
                    input_size=size,
                    scenario=scen,
                    repetitions=repetitions,
                    seed=seed,
                )
                all_search_trials.extend(trials)
                all_search_summaries.append(summary)

    print("\n  Search benchmarks completed successfully.")
    raw_search_path = os.path.join(PROJECT_ROOT, "data", "raw", "search_benchmark_trials.csv")
    proc_search_path = os.path.join(PROJECT_ROOT, "data", "processed", "search_benchmark_summary.csv")
    export_trials_to_csv(all_search_trials, raw_search_path)
    export_summaries_to_csv(all_search_summaries, proc_search_path)
    print(f"  Saved raw search trials: {os.path.relpath(raw_search_path, PROJECT_ROOT)} ({len(all_search_trials)} records)")
    print(f"  Saved search summary:    {os.path.relpath(proc_search_path, PROJECT_ROOT)} ({len(all_search_summaries)} records)")

    # 4. Sorting Benchmarks
    print("\n[4/4] Executing Sorting Benchmarks (Bubble Sort vs. Insertion Sort)...")
    if quick:
        sorting_sizes = [100, 500, 1000]
    else:
        sorting_sizes = [100, 250, 500, 1000, 2000, 3000]

    sorting_arrangements = ["sorted", "random", "reverse"]
    sorting_algorithms = ["bubble_sort", "insertion_sort"]

    all_sorting_trials = []
    all_sorting_summaries = []

    total_sort_configs = len(sorting_algorithms) * len(sorting_sizes) * len(sorting_arrangements)
    current_sort_idx = 0

    for alg in sorting_algorithms:
        for size in sorting_sizes:
            for arrg in sorting_arrangements:
                current_sort_idx += 1
                sys.stdout.write(f"\r  Progress: [{current_sort_idx}/{total_sort_configs}] {alg} (n={size}, {arrg})...")
                sys.stdout.flush()

                trials, summary = benchmark_sorting_scenario(
                    algorithm_name=alg,
                    input_size=size,
                    arrangement=arrg,
                    repetitions=repetitions,
                    seed=seed,
                )
                all_sorting_trials.extend(trials)
                all_sorting_summaries.append(summary)

    print("\n  Sorting benchmarks completed successfully.")
    raw_sort_path = os.path.join(PROJECT_ROOT, "data", "raw", "sorting_benchmark_trials.csv")
    proc_sort_path = os.path.join(PROJECT_ROOT, "data", "processed", "sorting_benchmark_summary.csv")
    export_trials_to_csv(all_sorting_trials, raw_sort_path)
    export_summaries_to_csv(all_sorting_summaries, proc_sort_path)
    print(f"  Saved raw sorting trials: {os.path.relpath(raw_sort_path, PROJECT_ROOT)} ({len(all_sorting_trials)} records)")
    print(f"  Saved sorting summary:    {os.path.relpath(proc_sort_path, PROJECT_ROOT)} ({len(all_sorting_summaries)} records)")

    # 5. Metadata JSON
    metadata = get_environment_metadata(random_seed=seed)
    metadata["benchmark_total_elapsed_sec"] = round(time.perf_counter() - start_time_all, 2)
    metadata["search_sizes"] = search_sizes
    metadata["sorting_sizes"] = sorting_sizes
    metadata["repetitions_per_case"] = repetitions
    metadata_path = os.path.join(PROJECT_ROOT, "data", "processed", "benchmark_metadata.json")
    export_metadata_to_json(metadata, metadata_path)
    print(f"  Saved benchmark metadata: {os.path.relpath(metadata_path, PROJECT_ROOT)}")

    total_elapsed = time.perf_counter() - start_time_all
    print("\n" + "=" * 70)
    print(f"ALL EXPERIMENTS COMPLETED IN {total_elapsed:.2f} SECONDS.")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run empirical algorithm benchmarks.")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed (default: 42)")
    parser.add_argument("--reps", type=int, default=30, help="Number of repetitions per configuration (default: 30)")
    parser.add_argument("--quick", action="store_true", help="Run smaller subset of sizes for rapid verification")
    args = parser.parse_args()

    run_all_benchmarks(seed=args.seed, repetitions=args.reps, quick=args.quick)
