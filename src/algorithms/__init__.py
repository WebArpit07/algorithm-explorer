"""Algorithms subpackage for Algorithm Explorer.

Exposes standard and instrumented implementations of:
- Linear Search
- Binary Search
- Bubble Sort
- Insertion Sort
"""

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

__all__ = [
    "SearchMetrics",
    "linear_search",
    "linear_search_instrumented",
    "binary_search",
    "binary_search_instrumented",
    "SortingMetrics",
    "bubble_sort",
    "bubble_sort_instrumented",
    "insertion_sort",
    "insertion_sort_instrumented",
]
