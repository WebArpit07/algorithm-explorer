"""Search algorithms module.

Implementations of Linear Search and Binary Search in accordance with
Kenneth H. Rosen, Discrete Mathematics and Its Applications (8th Edition),
Chapter 3 (Sections 3.1, 3.2, and 3.3).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class SearchMetrics:
    """Telemetry metrics recorded during search algorithm execution.

    Attributes:
        key_comparisons: Total comparisons made between sequence elements
            and the search target (equality + ordering).
        equality_comparisons: Comparisons specifically testing equality
            (e.g., element == target).
        ordering_comparisons: Comparisons specifically testing relative order
            (e.g., element < target or target < element).
        loop_evaluations: Number of times the primary loop continuation
            condition was evaluated.
    """

    key_comparisons: int
    equality_comparisons: int
    ordering_comparisons: int = 0
    loop_evaluations: int = 0


def linear_search(seq: Sequence[Any], target: Any) -> int:
    """Sequential search algorithm (Rosen §3.1, Algorithm 2).

    Sequentially inspects elements of `seq` from index 0 to n - 1, returning
    the index of the first occurrence of `target`. If `target` is not present,
    returns -1.

    Preconditions:
        - `seq` is an indexable sequence of comparable items.
    Postconditions:
        - Returns index i such that seq[i] == target and no j < i has seq[j] == target.
        - Returns -1 if for all j in range(len(seq)), seq[j] != target.
        - The input sequence `seq` is never modified.

    Complexity (Rosen §3.3):
        - Best Case: Θ(1) key comparisons (target is at index 0, n > 0).
        - Worst Case: Θ(n) key comparisons (target at index n - 1 or absent).
        - Average Case (successful, uniform distribution): (n + 1) / 2 key comparisons, Θ(n).
        - Unsuccessful Search: exactly n key comparisons.

    Args:
        seq: The sequence to search.
        target: The value to locate.

    Returns:
        The 0-based index of the first matching element, or -1 if not found.
    """
    for index, item in enumerate(seq):
        if item == target:
            return index
    return -1


def linear_search_instrumented(
    seq: Sequence[Any], target: Any
) -> tuple[int, SearchMetrics]:
    """Instrumented Linear Search returning the match index and metrics telemetry.

    Executes identical algorithmic logic to `linear_search`, with exact counting
    of element-target key comparisons and loop evaluations.

    Args:
        seq: The sequence to search.
        target: The value to locate.

    Returns:
        A tuple of (matched_index, SearchMetrics).
    """
    n = len(seq)
    key_comparisons = 0
    equality_comparisons = 0
    loop_evaluations = 0

    for index in range(n):
        loop_evaluations += 1
        equality_comparisons += 1
        key_comparisons += 1
        if seq[index] == target:
            return index, SearchMetrics(
                key_comparisons=key_comparisons,
                equality_comparisons=equality_comparisons,
                ordering_comparisons=0,
                loop_evaluations=loop_evaluations,
            )

    # Loop termination evaluation (when range exhausted)
    loop_evaluations += 1

    return -1, SearchMetrics(
        key_comparisons=key_comparisons,
        equality_comparisons=equality_comparisons,
        ordering_comparisons=0,
        loop_evaluations=loop_evaluations,
    )


def binary_search(
    seq: Sequence[Any], target: Any, *, check_sorted: bool = False
) -> int:
    """Iterative Binary Search algorithm (Rosen §3.1, Algorithm 3).

    Locates `target` in a sorted sequence by repeatedly bisecting the search
    interval [low, high].

    Preconditions:
        - The input sequence MUST be sorted in non-decreasing order:
          seq[0] <= seq[1] <= ... <= seq[n - 1].
        - If `check_sorted=True`, an explicit O(n) validation is performed
          and ValueError is raised if the sequence is not sorted.

    Postconditions:
        - Returns a valid 0-based index i such that seq[i] == target.
        - Returns -1 if `target` is not present in `seq`.
        - The input sequence `seq` is never modified.

    Complexity (Rosen §3.3):
        - Best Case: Θ(1) key comparisons (target is at the initial midpoint).
        - Worst Case: Θ(log n) key comparisons (target missing or at deepest branch).
        - Average Case: Θ(log n) key comparisons under uniform target distribution.
        - Auxiliary Space: Θ(1) (iterative implementation).

    Args:
        seq: A sorted sequence to search.
        target: The value to locate.
        check_sorted: If True, asserts sorted precondition at O(n) cost.

    Raises:
        ValueError: If check_sorted is True and `seq` is not sorted.

    Returns:
        An index of `target` in `seq`, or -1 if not found.
    """
    if check_sorted:
        for i in range(len(seq) - 1):
            if seq[i] > seq[i + 1]:
                raise ValueError("Precondition violated: sequence must be sorted.")

    low = 0
    high = len(seq) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = seq[mid]
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def binary_search_instrumented(
    seq: Sequence[Any], target: Any, *, check_sorted: bool = False
) -> tuple[int, SearchMetrics]:
    """Instrumented Binary Search returning the match index and metrics telemetry.

    Derivation of Counting Convention:
    Each iteration evaluates the loop continuation condition (low <= high).
    Inside the loop, two distinct element-target comparisons may occur:
    1. Equality test: seq[mid] == target (1 equality comparison).
       - If equal, the search terminates immediately.
    2. Ordering test: seq[mid] < target (1 ordering comparison).
       - Evaluated only when equality test is False, deciding whether to
         narrow to the right subsegment [mid + 1, high] or left [low, mid - 1].

    Thus, a successful probe terminating at midpoint performs 1 key comparison;
    every other step performs 2 key comparisons (1 equality + 1 ordering).
    Loop-condition evaluations are tracked separately in `loop_evaluations`.

    Args:
        seq: A sorted sequence to search.
        target: The value to locate.
        check_sorted: If True, validates non-decreasing order before searching.

    Returns:
        A tuple of (matched_index, SearchMetrics).
    """
    if check_sorted:
        for i in range(len(seq) - 1):
            if seq[i] > seq[i + 1]:
                raise ValueError("Precondition violated: sequence must be sorted.")

    low = 0
    high = len(seq) - 1

    key_comparisons = 0
    equality_comparisons = 0
    ordering_comparisons = 0
    loop_evaluations = 0

    while True:
        loop_evaluations += 1
        if low > high:
            break

        mid = (low + high) // 2
        mid_val = seq[mid]

        # 1. Equality comparison between element and target
        equality_comparisons += 1
        key_comparisons += 1
        if mid_val == target:
            return mid, SearchMetrics(
                key_comparisons=key_comparisons,
                equality_comparisons=equality_comparisons,
                ordering_comparisons=ordering_comparisons,
                loop_evaluations=loop_evaluations,
            )

        # 2. Ordering comparison between element and target
        ordering_comparisons += 1
        key_comparisons += 1
        if mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, SearchMetrics(
        key_comparisons=key_comparisons,
        equality_comparisons=equality_comparisons,
        ordering_comparisons=ordering_comparisons,
        loop_evaluations=loop_evaluations,
    )
