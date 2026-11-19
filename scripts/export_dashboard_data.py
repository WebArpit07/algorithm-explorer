"""
Export processed Python benchmark results to JSON for the Algorithm Explorer Web Dashboard.
Milestone M6 — Integration of M3 Experimental Datasets.
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DASHBOARD_DATA_DIR = PROJECT_ROOT / "dashboard" / "data"


def export_data():
    DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_file = DASHBOARD_DATA_DIR / "benchmark_data.json"

    # 1. Metadata
    meta_path = PROCESSED_DIR / "benchmark_metadata.json"
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # 2. Growth Functions
    growth_df = pd.read_csv(PROCESSED_DIR / "growth_functions.csv")
    growth_records = growth_df.to_dict(orient="records")

    # 3. Search Benchmark Summary
    search_df = pd.read_csv(PROCESSED_DIR / "search_benchmark_summary.csv")
    search_records = search_df.to_dict(orient="records")

    # 4. Sorting Benchmark Summary
    sorting_df = pd.read_csv(PROCESSED_DIR / "sorting_benchmark_summary.csv")
    sorting_records = sorting_df.to_dict(orient="records")

    # 5. Derived analytical summary points
    search_worst_100k = search_df[(search_df["input_size"] == 100000) & (search_df["scenario"] == "missing")]
    linear_worst_100k = search_worst_100k[search_worst_100k["algorithm"] == "linear_search"].iloc[0]
    binary_worst_100k = search_worst_100k[search_worst_100k["algorithm"] == "binary_search"].iloc[0]

    sorting_3k = sorting_df[sorting_df["input_size"] == 3000]
    bubble_rand_3k = sorting_3k[(sorting_3k["algorithm"] == "bubble_sort") & (sorting_3k["arrangement"] == "random")].iloc[0]
    insertion_rand_3k = sorting_3k[(sorting_3k["algorithm"] == "insertion_sort") & (sorting_3k["arrangement"] == "random")].iloc[0]
    insertion_sorted_3k = sorting_3k[(sorting_3k["algorithm"] == "insertion_sort") & (sorting_3k["arrangement"] == "sorted")].iloc[0]
    bubble_sorted_3k = sorting_3k[(sorting_3k["algorithm"] == "bubble_sort") & (sorting_3k["arrangement"] == "sorted")].iloc[0]

    dashboard_payload = {
        "source": "Python 3.14.7 — M3 Experimental Microbenchmark Harness",
        "reference": "Kenneth H. Rosen, Discrete Mathematics and Its Applications, 8th Edition, Chapter 3",
        "metadata": metadata,
        "growth_functions": growth_records,
        "search_summary": search_records,
        "sorting_summary": sorting_records,
        "highlighted_comparisons": {
            "search_at_100k": {
                "linear": {
                    "comparisons": int(linear_worst_100k["key_comparisons"]),
                    "median_time_ms": round(linear_worst_100k["median_duration_ns"] / 1e6, 3),
                },
                "binary": {
                    "comparisons": int(binary_worst_100k["key_comparisons"]),
                    "median_time_ms": round(binary_worst_100k["median_duration_ns"] / 1e6, 6),
                },
                "speedup_factor": round(linear_worst_100k["median_duration_ns"] / binary_worst_100k["median_duration_ns"], 1),
            },
            "sorting_at_3k": {
                "inversion_equivalence": {
                    "bubble_swaps_random": int(bubble_rand_3k["swaps"]),
                    "insertion_shifts_random": int(insertion_rand_3k["right_shifts"]),
                    "are_equal": int(bubble_rand_3k["swaps"]) == int(insertion_rand_3k["right_shifts"]),
                },
                "sorted_adaptation": {
                    "bubble_sorted_ms": round(bubble_sorted_3k["median_duration_ns"] / 1e6, 2),
                    "insertion_sorted_ms": round(insertion_sorted_3k["median_duration_ns"] / 1e6, 2),
                    "speedup_factor": round(bubble_sorted_3k["median_duration_ns"] / insertion_sorted_3k["median_duration_ns"], 1),
                }
            }
        }
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, indent=2)

    # Also export benchmark_data.js for direct file:// browser support without CORS friction
    out_js = DASHBOARD_DATA_DIR / "benchmark_data.js"
    with open(out_js, "w", encoding="utf-8") as f:
        f.write("/** Auto-generated from Python M3 experimental benchmarks **/\n")
        f.write("window.BENCHMARK_DATA = ")
        json.dump(dashboard_payload, f, indent=2)
        f.write(";\n")

    print(f"Exported benchmark data to {out_file} ({out_file.stat().st_size} bytes)")
    print(f"Exported browser-ready script to {out_js} ({out_js.stat().st_size} bytes)")


if __name__ == "__main__":
    export_data()
