"""Deterministic input generators for empirical algorithm benchmarking.

Provides controlled, reproducible datasets of unique integers for searching
and sorting experiments, aligned with Kenneth H. Rosen, Discrete Mathematics
and Its Applications (8th Edition), Chapter 3.
"""

from __future__ import annotations

import random
from typing import Literal

SearchScenario = Literal["first", "middle", "last", "missing"]
SortArrangement = Literal["sorted", "reverse", "random"]


def generate_sorted_list(size: int, step: int = 10, start: int = 10) -> list[int]:
    """Generates a strictly increasing list of unique integers.

    Args:
        size: Number of elements (n >= 0).
        step: Arithmetic progression step between consecutive elements.
        start: First element value.

    Returns:
        A list of `size` sorted integers [start, start + step, ...].
    """
    if size < 0:
        raise ValueError(f"Size must be non-negative, got {size}")
    return [start + i * step for i in range(size)]


def generate_reverse_sorted_list(
    size: int, step: int = 10, start: int = 10
) -> list[int]:
    """Generates a strictly decreasing list of unique integers.

    Every pair constitutes an inversion: exactly n(n - 1) / 2 inversions.

    Args:
        size: Number of elements (n >= 0).
        step: Arithmetic progression step.
        start: Base offset.

    Returns:
        A list of `size` reverse-sorted integers.
    """
    if size < 0:
        raise ValueError(f"Size must be non-negative, got {size}")
    # Elements descending from (start + (size - 1) * step) down to start
    return [start + (size - 1 - i) * step for i in range(size)]


def generate_random_list(
    size: int, seed: int | None = None, step: int = 10, start: int = 10
) -> list[int]:
    """Generates a pseudo-random permutation of `size` distinct integers.

    Uses Fisher-Yates shuffle seeded with `seed` to guarantee deterministic
    reproducibility while ensuring distinct elements for unambiguous inversion
    and comparison analysis.

    Args:
        size: Number of elements (n >= 0).
        seed: Random seed for deterministic generation.
        step: Arithmetic progression step of base elements.
        start: Base offset.

    Returns:
        A randomly permuted list of unique integers.
    """
    arr = generate_sorted_list(size, step=step, start=start)
    rng = random.Random(seed)
    rng.shuffle(arr)
    return arr


def get_search_target(
    seq: list[int], scenario: SearchScenario, missing_offset: int = 5
) -> int:
    """Retrieves or synthesizes a search target for a specified scenario.

    Assumes `seq` is generated via standard generators with distinct values.

    Scenarios:
        - "first": target is at index 0 (best case for Linear Search).
        - "middle": target is at index len(seq) // 2 (initial midpoint for Binary Search).
        - "last": target is at index len(seq) - 1 (worst-case successful).
        - "missing": target does not exist in `seq` (unsuccessful search).

    Args:
        seq: Non-empty list of unique integers.
        scenario: One of "first", "middle", "last", "missing".
        missing_offset: Offset ensuring missing target is not present in seq.

    Returns:
        The target integer.
    """
    if not seq:
        if scenario == "missing":
            return -999
        raise ValueError("Cannot select present target from an empty sequence.")

    n = len(seq)
    if scenario == "first":
        return seq[0]
    elif scenario == "middle":
        return seq[n // 2]
    elif scenario == "last":
        return seq[n - 1]
    elif scenario == "missing":
        # Guaranteed absent: maximum element + missing_offset
        return max(seq) + missing_offset
    else:
        raise ValueError(f"Unknown search scenario: {scenario}")


def generate_sorting_dataset(
    size: int, arrangement: SortArrangement, seed: int | None = None
) -> list[int]:
    """Generates a sorting dataset for the specified arrangement.

    Args:
        size: Number of elements.
        arrangement: One of "sorted", "reverse", "random".
        seed: Random seed (relevant for "random").

    Returns:
        A list of `size` integers.
    """
    if arrangement == "sorted":
        return generate_sorted_list(size)
    elif arrangement == "reverse":
        return generate_reverse_sorted_list(size)
    elif arrangement == "random":
        return generate_random_list(size, seed=seed)
    else:
        raise ValueError(f"Unknown arrangement: {arrangement}")
