"""Telemetry, statistics, and experimental data structures.

Captures hardware/environment metadata, trial-level raw measurements,
and aggregate statistical distributions (mean, median, std dev, IQR, 95% CI).
"""

from __future__ import annotations

import csv
import json
import math
import os
import platform
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any, Sequence


@dataclass(frozen=True, slots=True)
class SearchTrial:
    """Raw record for a single search benchmark trial."""

    algorithm: str
    input_size: int
    scenario: str
    trial_id: int
    duration_ns: float
    key_comparisons: int
    equality_comparisons: int
    ordering_comparisons: int
    loop_evaluations: int


@dataclass(frozen=True, slots=True)
class SearchSummary:
    """Aggregated statistics for a set of search trials."""

    algorithm: str
    input_size: int
    scenario: str
    repetitions: int
    mean_duration_ns: float
    median_duration_ns: float
    std_dev_duration_ns: float
    min_duration_ns: float
    max_duration_ns: float
    q25_duration_ns: float
    q75_duration_ns: float
    iqr_duration_ns: float
    key_comparisons: int
    equality_comparisons: int
    ordering_comparisons: int
    loop_evaluations: int


@dataclass(frozen=True, slots=True)
class SortingTrial:
    """Raw record for a single sorting benchmark trial."""

    algorithm: str
    input_size: int
    arrangement: str
    trial_id: int
    duration_ns: float
    element_comparisons: int
    swaps: int
    right_shifts: int


@dataclass(frozen=True, slots=True)
class SortingSummary:
    """Aggregated statistics for a set of sorting trials."""

    algorithm: str
    input_size: int
    arrangement: str
    repetitions: int
    mean_duration_ns: float
    median_duration_ns: float
    std_dev_duration_ns: float
    min_duration_ns: float
    max_duration_ns: float
    q25_duration_ns: float
    q75_duration_ns: float
    iqr_duration_ns: float
    element_comparisons: int
    swaps: int
    right_shifts: int


def calculate_statistics(values: Sequence[float]) -> dict[str, float]:
    """Computes robust descriptive statistics for a sequence of observations.

    Args:
        values: Non-empty sequence of numerical measurements.

    Returns:
        Dict mapping metric name to calculated value.
    """
    if not values:
        raise ValueError("Cannot calculate statistics on empty sequence.")

    n = len(values)
    s_vals = sorted(values)

    mean_val = sum(values) / n
    variance = (
        sum((x - mean_val) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
    )
    std_dev = math.sqrt(variance)

    # Median (50th percentile)
    if n % 2 == 1:
        median_val = s_vals[n // 2]
    else:
        median_val = (s_vals[n // 2 - 1] + s_vals[n // 2]) / 2.0

    # Quartiles (linear interpolation)
    def percentile(p: float) -> float:
        if n == 1:
            return s_vals[0]
        idx = p * (n - 1)
        low = int(math.floor(idx))
        high = int(math.ceil(idx))
        weight = idx - low
        return s_vals[low] * (1.0 - weight) + s_vals[high] * weight

    q25 = percentile(0.25)
    q75 = percentile(0.75)
    iqr = q75 - q25

    return {
        "mean": mean_val,
        "median": median_val,
        "std_dev": std_dev,
        "min": s_vals[0],
        "max": s_vals[-1],
        "q25": q25,
        "q75": q75,
        "iqr": iqr,
    }


def get_environment_metadata(random_seed: int) -> dict[str, Any]:
    """Captures system hardware, runtime, and experiment parameters."""
    return {
        "benchmark_date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "random_seed": random_seed,
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine_architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_count_logical": os.cpu_count(),
        "timing_timer": "time.perf_counter_ns",
        "timing_resolution_ns": time.get_clock_info("perf_counter").resolution
        * 1e9,
    }


def export_trials_to_csv(trials: Sequence[Any], file_path: str) -> None:
    """Exports raw trial dataclasses to CSV."""
    if not trials:
        return
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    fields = list(asdict(trials[0]).keys())
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for t in trials:
            writer.writerow(asdict(t))


def export_summaries_to_csv(summaries: Sequence[Any], file_path: str) -> None:
    """Exports summary statistics dataclasses to CSV."""
    if not summaries:
        return
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    fields = list(asdict(summaries[0]).keys())
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in summaries:
            writer.writerow(asdict(s))


def export_metadata_to_json(metadata: dict[str, Any], file_path: str) -> None:
    """Exports environment metadata to formatted JSON."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
