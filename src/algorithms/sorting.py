"""Sorting algorithms module.

Implementations of Bubble Sort and Insertion Sort in accordance with
Kenneth H. Rosen, Discrete Mathematics and Its Applications (8th Edition),
Chapter 3 (Sections 3.1, 3.2, and 3.3).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, MutableSequence


@dataclass(frozen=True, slots=True)
class SortingMetrics:
    """Telemetry metrics recorded during sorting algorithm execution.

    Attributes:
        element_comparisons: Number of comparisons between two list elements.
        swaps: Number of element swap operations performed (primarily Bubble Sort).
        right_shifts: Number of element displacement operations where an element
            is copied one index to the right to create space for insertion
            (Insertion Sort).
    """

    element_comparisons: int
    swaps: int = 0
    right_shifts: int = 0


def bubble_sort(arr: MutableSequence[Any]) -> MutableSequence[Any]:
    """Standard fixed-pass Bubble Sort algorithm (Rosen §3.1, Algorithm 4).

    Sorts a mutable sequence in place into non-decreasing order using adjacent
    element comparisons and pairwise exchanges.

    Per the core academic specification (Rosen §3.1, Algorithm 4), this primary
    implementation performs the exact fixed-pass iteration without early
    termination flags.

    Preconditions:
        - `arr` is a mutable sequence of mutually comparable elements.
    Postconditions:
        - `arr` is sorted in place: arr[0] <= arr[1] <= ... <= arr[n - 1].
        - Preserves the relative order of equal elements (stable sort).

    Complexity (Rosen §3.3):
        - Comparisons: Exactly n(n - 1) / 2 for ALL inputs of size n >= 1 (Θ(n²)).
        - Best-case swaps: 0 (when input is already sorted).
        - Worst-case swaps: n(n - 1) / 2 (when input is strictly descending with distinct items).
        - Average-case swaps: n(n - 1) / 4 (for random permutations of distinct items).
        - Auxiliary Space: Θ(1) (in-place).

    Args:
        arr: The mutable sequence to be sorted in place.

    Returns:
        The same sequence `arr`, sorted in non-decreasing order.
    """
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def bubble_sort_instrumented(
    arr: MutableSequence[Any],
) -> tuple[MutableSequence[Any], SortingMetrics]:
    """Instrumented Bubble Sort returning the sorted sequence and metrics telemetry.

    Sorts the sequence in place while accurately counting element comparisons
    and adjacent swap operations.

    Args:
        arr: The mutable sequence to sort in place.

    Returns:
        A tuple of (sorted_arr, SortingMetrics).
    """
    n = len(arr)
    element_comparisons = 0
    swaps = 0

    for i in range(n - 1):
        for j in range(n - 1 - i):
            element_comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return arr, SortingMetrics(
        element_comparisons=element_comparisons,
        swaps=swaps,
        right_shifts=0,
    )


def insertion_sort(arr: MutableSequence[Any]) -> MutableSequence[Any]:
    """Standard in-place Insertion Sort algorithm (Rosen §3.1, Algorithm 5).

    Iteratively expands a sorted prefix [0 .. j - 1] by inserting the next
    element arr[j] into its correct position within that prefix.

    Preconditions:
        - `arr` is a mutable sequence of mutually comparable elements.
    Postconditions:
        - `arr` is sorted in place: arr[0] <= arr[1] <= ... <= arr[n - 1].
        - Preserves the relative order of duplicate elements (stable sort).

    Complexity (Rosen §3.3):
        - Best Case Comparisons: n - 1 when already sorted (Θ(n)).
        - Worst Case Comparisons: n(n - 1) / 2 when reverse sorted (Θ(n²)).
        - Average Case Comparisons: Θ(n²).
        - Best Case Right Shifts: 0 (already sorted).
        - Worst Case Right Shifts: n(n - 1) / 2 (strictly reverse-sorted distinct elements).
        - Auxiliary Space: Θ(1) (in-place).

    Args:
        arr: The mutable sequence to sort in place.

    Returns:
        The same sequence `arr`, sorted in non-decreasing order.
    """
    n = len(arr)
    for j in range(1, n):
        key = arr[j]
        i = j - 1
        while i >= 0 and arr[i] > key:
            arr[i + 1] = arr[i]
            i -= 1
        arr[i + 1] = key
    return arr


def insertion_sort_instrumented(
    arr: MutableSequence[Any],
) -> tuple[MutableSequence[Any], SortingMetrics]:
    """Instrumented Insertion Sort returning the sorted sequence and metrics telemetry.

    Counting Convention Definition:
    - Element Comparison: Each time an element in the sorted prefix (arr[i])
      is compared against `key` (arr[i] > key).
      If `i >= 0`, `arr[i] > key` is evaluated. If True, the loop shifts arr[i]
      and decrements i. If False, the comparison still occurred, and the while
      loop breaks. If i reaches -1, loop termination is a short-circuit boundary
      check without comparing elements.
    - Right Shift: Moving an existing element one position to the right
      (`arr[i + 1] = arr[i]`). The final placement of `key` (`arr[i + 1] = key`)
      is an insertion, not a right shift.

    Args:
        arr: The mutable sequence to sort in place.

    Returns:
        A tuple of (sorted_arr, SortingMetrics).
    """
    n = len(arr)
    element_comparisons = 0
    right_shifts = 0

    for j in range(1, n):
        key = arr[j]
        i = j - 1
        while i >= 0:
            element_comparisons += 1
            if arr[i] > key:
                arr[i + 1] = arr[i]
                right_shifts += 1
                i -= 1
            else:
                break
        arr[i + 1] = key

    return arr, SortingMetrics(
        element_comparisons=element_comparisons,
        swaps=0,
        right_shifts=right_shifts,
    )
