"""Benchmarking harness and empirical data acquisition subpackage."""

from src.benchmarking.harness import (
    benchmark_search_scenario,
    benchmark_sorting_scenario,
    run_pilot_benchmark,
)
from src.benchmarking.input_generators import (
    SearchScenario,
    SortArrangement,
    generate_random_list,
    generate_reverse_sorted_list,
    generate_sorted_list,
    generate_sorting_dataset,
    get_search_target,
)
from src.benchmarking.telemetry import (
    SearchSummary,
    SearchTrial,
    SortingSummary,
    SortingTrial,
    calculate_statistics,
    export_metadata_to_json,
    export_summaries_to_csv,
    export_trials_to_csv,
    get_environment_metadata,
)

__all__ = [
    "generate_sorted_list",
    "generate_reverse_sorted_list",
    "generate_random_list",
    "get_search_target",
    "generate_sorting_dataset",
    "SearchScenario",
    "SortArrangement",
    "SearchTrial",
    "SearchSummary",
    "SortingTrial",
    "SortingSummary",
    "calculate_statistics",
    "get_environment_metadata",
    "export_trials_to_csv",
    "export_summaries_to_csv",
    "export_metadata_to_json",
    "benchmark_search_scenario",
    "benchmark_sorting_scenario",
    "run_pilot_benchmark",
]
