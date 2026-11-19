"""Benchmarking execution harness for searching and sorting algorithms.

Provides high-resolution execution-time measurements using `time.perf_counter_ns()`,
strict isolation of instrumentation overhead from timing, automated replication,
and statistical telemetry aggregation.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Sequence

from src.algorithms.search import (
    SearchMetrics,
    binary_search,
    binary_search_instrumented,
    linear_search,
    linear_search_instrumented,
)
from src.algorithms.sorting import (
    SortingMetrics,
    bubble_sort,
    bubble_sort_instrumented,
    insertion_sort,
    insertion_sort_instrumented,
)
from src.benchmarking.input_generators import (
    SearchScenario,
    SortArrangement,
    generate_random_list,
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
)


def benchmark_search_scenario(
    algorithm_name: str,
    input_size: int,
    scenario: SearchScenario,
    repetitions: int = 30,
    seed: int = 42,
) -> tuple[list[SearchTrial], SearchSummary]:
    """Benchmarks a specific search algorithm, size, and scenario.

    Methodology:
    1. Operates on a pre-generated sorted list so that both Linear and Binary
       Search query identical datasets.
    2. Uses instrumented execution once to obtain exact, deterministic
       comparison and loop evaluation counts.
    3. Uses unadorned, uninstrumented execution for timing measurements.
    4. For fast operations (e.g. Binary Search or Best Case), evaluates in
       calibrated batches to defeat timer quantization and OS scheduling jitter.

    Args:
        algorithm_name: "linear_search" or "binary_search".
        input_size: Number of elements in the search sequence.
        scenario: "first", "middle", "last", or "missing".
        repetitions: Number of independent measurement trials (default 30).
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (list_of_trials, summary_record).
    """
    dataset = generate_sorted_list(input_size)
    target = get_search_target(dataset, scenario)

    # 1. Operation Count Telemetry (Instrumented Execution)
    if algorithm_name == "linear_search":
        _, metrics = linear_search_instrumented(dataset, target)
        search_fn = linear_search
    elif algorithm_name == "binary_search":
        _, metrics = binary_search_instrumented(dataset, target)
        search_fn = binary_search
    else:
        raise ValueError(f"Unknown search algorithm: {algorithm_name}")

    # 2. Timing Calibration: determine batch size if operation is sub-microsecond
    # Binary search and early linear search complete in under 500ns, where
    # timer granularity and clock call overhead can skew single-shot measurements.
    probe_start = time.perf_counter_ns()
    search_fn(dataset, target)
    probe_duration = time.perf_counter_ns() - probe_start

    batch_size = 1
    if probe_duration < 5_000:  # less than 5 microseconds
        batch_size = 50
    if probe_duration < 500:
        batch_size = 200

    trials: list[SearchTrial] = []
    durations: list[float] = []

    # 3. Repeated Measurement Trials
    for trial_idx in range(repetitions):
        start_ns = time.perf_counter_ns()
        if batch_size == 1:
            search_fn(dataset, target)
        else:
            for _ in range(batch_size):
                search_fn(dataset, target)
        end_ns = time.perf_counter_ns()

        duration_per_call = (end_ns - start_ns) / batch_size
        durations.append(duration_per_call)

        trials.append(
            SearchTrial(
                algorithm=algorithm_name,
                input_size=input_size,
                scenario=scenario,
                trial_id=trial_idx,
                duration_ns=duration_per_call,
                key_comparisons=metrics.key_comparisons,
                equality_comparisons=metrics.equality_comparisons,
                ordering_comparisons=metrics.ordering_comparisons,
                loop_evaluations=metrics.loop_evaluations,
            )
        )

    stats = calculate_statistics(durations)
    summary = SearchSummary(
        algorithm=algorithm_name,
        input_size=input_size,
        scenario=scenario,
        repetitions=repetitions,
        mean_duration_ns=stats["mean"],
        median_duration_ns=stats["median"],
        std_dev_duration_ns=stats["std_dev"],
        min_duration_ns=stats["min"],
        max_duration_ns=stats["max"],
        q25_duration_ns=stats["q25"],
        q75_duration_ns=stats["q75"],
        iqr_duration_ns=stats["iqr"],
        key_comparisons=metrics.key_comparisons,
        equality_comparisons=metrics.equality_comparisons,
        ordering_comparisons=metrics.ordering_comparisons,
        loop_evaluations=metrics.loop_evaluations,
    )

    return trials, summary


def benchmark_sorting_scenario(
    algorithm_name: str,
    input_size: int,
    arrangement: SortArrangement,
    repetitions: int = 30,
    seed: int = 42,
) -> tuple[list[SortingTrial], SortingSummary]:
    """Benchmarks a specific sorting algorithm, size, and arrangement.

    Methodology:
    1. Pre-generates the base dataset using deterministic seed.
    2. Runs instrumented execution once on a separate copy to record exact
       comparisons, swaps, and right shifts.
    3. For timing, iterates `repetitions` times. Before each timed run, creates
       a fresh copy `list(base_dataset)` outside the timing block.
    4. Measures execution time strictly across `sort_fn(arr_copy)`.

    Args:
        algorithm_name: "bubble_sort" or "insertion_sort".
        input_size: Number of elements in the array.
        arrangement: "sorted", "reverse", or "random".
        repetitions: Number of measurement trials.
        seed: Random seed for random arrangements.

    Returns:
        Tuple of (list_of_trials, summary_record).
    """
    base_dataset = generate_sorting_dataset(
        input_size, arrangement=arrangement, seed=seed
    )

    # 1. Operation Count Telemetry
    if algorithm_name == "bubble_sort":
        _, metrics = bubble_sort_instrumented(list(base_dataset))
        sort_fn = bubble_sort
    elif algorithm_name == "insertion_sort":
        _, metrics = insertion_sort_instrumented(list(base_dataset))
        sort_fn = insertion_sort
    else:
        raise ValueError(f"Unknown sorting algorithm: {algorithm_name}")

    trials: list[SortingTrial] = []
    durations: list[float] = []

    # 2. Timing Measurements
    for trial_idx in range(repetitions):
        # Prepare fresh copy outside timing measurement
        arr_to_sort = list(base_dataset)

        start_ns = time.perf_counter_ns()
        sort_fn(arr_to_sort)
        end_ns = time.perf_counter_ns()

        duration = float(end_ns - start_ns)
        durations.append(duration)

        trials.append(
            SortingTrial(
                algorithm=algorithm_name,
                input_size=input_size,
                arrangement=arrangement,
                trial_id=trial_idx,
                duration_ns=duration,
                element_comparisons=metrics.element_comparisons,
                swaps=metrics.swaps,
                right_shifts=metrics.right_shifts,
            )
        )

    stats = calculate_statistics(durations)
    summary = SortingSummary(
        algorithm=algorithm_name,
        input_size=input_size,
        arrangement=arrangement,
        repetitions=repetitions,
        mean_duration_ns=stats["mean"],
        median_duration_ns=stats["median"],
        std_dev_duration_ns=stats["std_dev"],
        min_duration_ns=stats["min"],
        max_duration_ns=stats["max"],
        q25_duration_ns=stats["q25"],
        q75_duration_ns=stats["q75"],
        iqr_duration_ns=stats["iqr"],
        element_comparisons=metrics.element_comparisons,
        swaps=metrics.swaps,
        right_shifts=metrics.right_shifts,
    )

    return trials, summary


def run_pilot_benchmark() -> dict[str, Any]:
    """Runs a fast pilot benchmark across small inputs to assess timing feasibility.

    Returns:
        Dict summarizing sample durations.
    """
    results = {}
    test_sizes = [100, 500, 1000, 2000]
    for size in test_sizes:
        arr = generate_random_list(size, seed=999)
        # Bubble sort
        t0 = time.perf_counter_ns()
        bubble_sort(list(arr))
        b_time = (time.perf_counter_ns() - t0) / 1e6  # ms

        # Insertion sort
        t0 = time.perf_counter_ns()
        insertion_sort(list(arr))
        i_time = (time.perf_counter_ns() - t0) / 1e6  # ms

        results[f"n={size}"] = {
            "bubble_sort_ms": round(b_time, 3),
            "insertion_sort_ms": round(i_time, 3),
        }
    return results
