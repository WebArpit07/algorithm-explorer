"""Comprehensive test suite for Sorting Algorithms (Bubble Sort and Insertion Sort).

Verifies correctness, stability, in-place behavior, edge cases, and exact
theoretical comparison/swap/shift counts against Kenneth H. Rosen,
Discrete Mathematics and Its Applications (8th Edition), Chapter 3.
"""

from src.algorithms.sorting import (
    SortingMetrics,
    bubble_sort,
    bubble_sort_instrumented,
    insertion_sort,
    insertion_sort_instrumented,
)


class TestBubbleSort:
    """Test suite for standard fixed-pass Bubble Sort."""

    def test_empty_list(self):
        """Empty list is sorted with 0 comparisons and 0 swaps."""
        arr = []
        result = bubble_sort(arr)
        assert result == []
        assert result is arr

        arr2 = []
        res2, metrics = bubble_sort_instrumented(arr2)
        assert res2 == []
        assert res2 is arr2
        assert metrics.element_comparisons == 0
        assert metrics.swaps == 0
        assert metrics.right_shifts == 0

    def test_single_element_list(self):
        """Single element list is sorted with 0 comparisons and 0 swaps."""
        arr = [42]
        result = bubble_sort(arr)
        assert result == [42]
        assert result is arr

        arr2 = [42]
        res2, metrics = bubble_sort_instrumented(arr2)
        assert res2 == [42]
        assert metrics.element_comparisons == 0
        assert metrics.swaps == 0

    def test_already_sorted_list_comparisons_and_swaps(self):
        """Already sorted list: fixed-pass performs n(n-1)/2 comparisons and 0 swaps."""
        arr = [10, 20, 30, 40, 50]
        n = len(arr)
        expected_comparisons = n * (n - 1) // 2  # 5 * 4 / 2 = 10

        res, metrics = bubble_sort_instrumented(arr)
        assert res == [10, 20, 30, 40, 50]
        assert res is arr
        assert metrics.element_comparisons == expected_comparisons
        assert metrics.swaps == 0

    def test_reverse_sorted_list_comparisons_and_swaps(self):
        """Reverse sorted list: worst-case with n(n-1)/2 comparisons and n(n-1)/2 swaps."""
        arr = [50, 40, 30, 20, 10]
        n = len(arr)
        expected_ops = n * (n - 1) // 2  # 10

        res, metrics = bubble_sort_instrumented(arr)
        assert res == [10, 20, 30, 40, 50]
        assert metrics.element_comparisons == expected_ops
        assert metrics.swaps == expected_ops

    def test_randomly_ordered_list(self):
        """Arbitrary unsorted list produces properly ordered result."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        expected = sorted(arr)
        result = bubble_sort(arr)
        assert result == expected

    def test_duplicate_values_and_stability(self):
        """Preserves duplicate values and relative order of equal keys (stability)."""
        # Tuples where first element is key, second is original order tag
        arr = [(3, "first"), (1, "a"), (3, "second"), (2, "b"), (3, "third")]
        bubble_sort(arr)
        assert arr == [(1, "a"), (2, "b"), (3, "first"), (3, "second"), (3, "third")]

    def test_negative_values(self):
        """Correctly handles mixed negative, zero, and positive values."""
        arr = [0, -12, 45, -3, 2, -100, 18]
        expected = sorted(arr)
        assert bubble_sort(arr) == expected

    def test_in_place_mutation(self):
        """Verifies that the exact same list instance is mutated and returned."""
        arr = [5, 3, 1, 4, 2]
        original_id = id(arr)
        res = bubble_sort(arr)
        assert id(res) == original_id
        assert arr == [1, 2, 3, 4, 5]

    def test_fixed_pass_comparison_formula_across_various_sizes(self):
        """Elements comparison count is rigorously n(n-1)/2 for sizes 2 to 10."""
        for n in range(2, 11):
            arr = list(range(n))
            _, metrics = bubble_sort_instrumented(arr)
            assert metrics.element_comparisons == n * (n - 1) // 2


class TestInsertionSort:
    """Test suite for standard in-place Insertion Sort."""

    def test_empty_list(self):
        """Empty list is sorted with 0 comparisons and 0 shifts."""
        arr = []
        result = insertion_sort(arr)
        assert result == []
        assert result is arr

        arr2 = []
        res2, metrics = insertion_sort_instrumented(arr2)
        assert res2 == []
        assert res2 is arr2
        assert metrics.element_comparisons == 0
        assert metrics.right_shifts == 0
        assert metrics.swaps == 0

    def test_single_element_list(self):
        """Single element list is sorted with 0 comparisons and 0 shifts."""
        arr = [99]
        result = insertion_sort(arr)
        assert result == [99]
        assert result is arr

        arr2 = [99]
        res2, metrics = insertion_sort_instrumented(arr2)
        assert res2 == [99]
        assert metrics.element_comparisons == 0
        assert metrics.right_shifts == 0

    def test_already_sorted_list_best_case(self):
        """Already sorted list: best case performs exactly n - 1 comparisons and 0 shifts."""
        arr = [10, 20, 30, 40, 50]
        n = len(arr)
        expected_comparisons = n - 1  # 4

        res, metrics = insertion_sort_instrumented(arr)
        assert res == [10, 20, 30, 40, 50]
        assert res is arr
        assert metrics.element_comparisons == expected_comparisons
        assert metrics.right_shifts == 0

    def test_reverse_sorted_list_worst_case(self):
        """Reverse sorted list: worst case performs n(n-1)/2 comparisons and n(n-1)/2 shifts."""
        arr = [50, 40, 30, 20, 10]
        n = len(arr)
        expected_ops = n * (n - 1) // 2  # 10

        res, metrics = insertion_sort_instrumented(arr)
        assert res == [10, 20, 30, 40, 50]
        assert metrics.element_comparisons == expected_ops
        assert metrics.right_shifts == expected_ops

    def test_randomly_ordered_list(self):
        """Arbitrary unsorted list produces properly ordered result."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        expected = sorted(arr)
        result = insertion_sort(arr)
        assert result == expected

    def test_duplicate_values_and_stability(self):
        """Preserves duplicate values and relative order of equal keys (stability)."""
        arr = [(3, "first"), (1, "a"), (3, "second"), (2, "b"), (3, "third")]
        insertion_sort(arr)
        assert arr == [(1, "a"), (2, "b"), (3, "first"), (3, "second"), (3, "third")]

    def test_negative_values(self):
        """Correctly handles mixed negative, zero, and positive values."""
        arr = [-10, 5, -30, 0, 12, -2]
        expected = sorted(arr)
        assert insertion_sort(arr) == expected

    def test_in_place_mutation(self):
        """Verifies that the exact same list instance is mutated and returned."""
        arr = [9, 3, 7, 1]
        original_id = id(arr)
        res = insertion_sort(arr)
        assert id(res) == original_id
        assert arr == [1, 3, 7, 9]

    def test_best_and_worst_formulas_across_various_sizes(self):
        """Verifies exact comparison formulas for sizes 2 to 10."""
        for n in range(2, 11):
            # Best case: already sorted
            arr_best = list(range(n))
            _, m_best = insertion_sort_instrumented(arr_best)
            assert m_best.element_comparisons == n - 1
            assert m_best.right_shifts == 0

            # Worst case: reverse sorted
            arr_worst = list(range(n, 0, -1))
            _, m_worst = insertion_sort_instrumented(arr_worst)
            assert m_worst.element_comparisons == n * (n - 1) // 2
            assert m_worst.right_shifts == n * (n - 1) // 2
