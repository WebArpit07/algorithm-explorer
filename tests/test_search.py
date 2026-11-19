"""Comprehensive test suite for Search Algorithms (Linear and Binary Search).

Verifies correctness, boundary behavior, pre/postconditions, and exact
theoretical comparison counts against Kenneth H. Rosen, Discrete Mathematics
and Its Applications (8th Edition), Chapter 3.
"""

import pytest

from src.algorithms.search import (
    SearchMetrics,
    binary_search,
    binary_search_instrumented,
    linear_search,
    linear_search_instrumented,
)


class TestLinearSearch:
    """Test suite for Linear Search."""

    def test_empty_sequence(self):
        """Empty sequence returns -1 with 0 key comparisons."""
        seq = []
        target = 42
        assert linear_search(seq, target) == -1

        index, metrics = linear_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == 0
        assert metrics.equality_comparisons == 0
        assert metrics.loop_evaluations == 1

    def test_single_element_present(self):
        """Single-element sequence where target is present (best case)."""
        seq = [10]
        target = 10
        assert linear_search(seq, target) == 0

        index, metrics = linear_search_instrumented(seq, target)
        assert index == 0
        assert metrics.key_comparisons == 1
        assert metrics.equality_comparisons == 1

    def test_single_element_missing(self):
        """Single-element sequence where target is missing."""
        seq = [10]
        target = 99
        assert linear_search(seq, target) == -1

        index, metrics = linear_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == 1
        assert metrics.equality_comparisons == 1

    def test_target_at_first_position_best_case(self):
        """Best case: target is at index 0, requiring exactly 1 key comparison."""
        seq = [5, 12, 19, 23, 37, 42, 59]
        target = 5
        assert linear_search(seq, target) == 0

        index, metrics = linear_search_instrumented(seq, target)
        assert index == 0
        assert metrics.key_comparisons == 1
        assert metrics.equality_comparisons == 1

    def test_target_at_last_position(self):
        """Worst-case successful search: target at index n - 1 requires n key comparisons."""
        seq = [5, 12, 19, 23, 37, 42, 59]
        n = len(seq)
        target = 59
        assert linear_search(seq, target) == n - 1

        index, metrics = linear_search_instrumented(seq, target)
        assert index == n - 1
        assert metrics.key_comparisons == n
        assert metrics.equality_comparisons == n

    def test_target_missing_unsuccessful_worst_case(self):
        """Unsuccessful search: target absent requires exactly n key comparisons."""
        seq = [5, 12, 19, 23, 37, 42, 59]
        n = len(seq)
        target = 999
        assert linear_search(seq, target) == -1

        index, metrics = linear_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == n
        assert metrics.equality_comparisons == n

    def test_duplicate_elements_returns_first_occurrence(self):
        """Linear search must return the first occurrence among duplicates."""
        seq = [10, 20, 30, 20, 50, 20]
        target = 20
        assert linear_search(seq, target) == 1

        index, metrics = linear_search_instrumented(seq, target)
        assert index == 1
        # Checked index 0 (10 == 20: False), index 1 (20 == 20: True) -> 2 comparisons
        assert metrics.key_comparisons == 2

    def test_negative_integers(self):
        """Handles negative integers and zero correctly."""
        seq = [-50, -25, -10, 0, 15, 30]
        assert linear_search(seq, -10) == 2
        assert linear_search(seq, 0) == 3
        assert linear_search(seq, -100) == -1

    def test_sequence_not_mutated(self):
        """Linear search must not mutate input sequence."""
        seq = [4, 2, 7, 1, 9]
        original_copy = list(seq)
        linear_search(seq, 7)
        assert seq == original_copy

        linear_search_instrumented(seq, 7)
        assert seq == original_copy

    def test_intermediate_comparisons_exact_match(self):
        """Verifies exact comparison count matches target index + 1 for successful search."""
        seq = ["alpha", "beta", "gamma", "delta", "epsilon"]
        for expected_index, item in enumerate(seq):
            index, metrics = linear_search_instrumented(seq, item)
            assert index == expected_index
            assert metrics.key_comparisons == expected_index + 1


class TestBinarySearch:
    """Test suite for Binary Search."""

    def test_empty_sequence(self):
        """Empty sequence returns -1 with 0 key comparisons."""
        seq = []
        target = 10
        assert binary_search(seq, target) == -1

        index, metrics = binary_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == 0
        assert metrics.equality_comparisons == 0
        assert metrics.ordering_comparisons == 0
        assert metrics.loop_evaluations == 1  # 0 > -1 condition check

    def test_single_element_present(self):
        """Single element matching target: 1 equality comparison."""
        seq = [42]
        target = 42
        assert binary_search(seq, target) == 0

        index, metrics = binary_search_instrumented(seq, target)
        assert index == 0
        assert metrics.key_comparisons == 1
        assert metrics.equality_comparisons == 1
        assert metrics.ordering_comparisons == 0

    def test_single_element_missing(self):
        """Single element missing target: 1 equality + 1 ordering = 2 comparisons."""
        seq = [42]
        target = 99
        assert binary_search(seq, target) == -1

        index, metrics = binary_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == 2
        assert metrics.equality_comparisons == 1
        assert metrics.ordering_comparisons == 1

    def test_target_at_initial_midpoint_best_case(self):
        """Best case: target is at initial midpoint (low=0, high=6 -> mid=3)."""
        seq = [10, 20, 30, 40, 50, 60, 70]
        target = 40
        assert binary_search(seq, target) == 3

        index, metrics = binary_search_instrumented(seq, target)
        assert index == 3
        # Match found on first probe -> 1 equality, 0 ordering -> 1 total
        assert metrics.key_comparisons == 1
        assert metrics.equality_comparisons == 1
        assert metrics.ordering_comparisons == 0

    def test_target_at_first_position(self):
        """Target at index 0."""
        seq = [10, 20, 30, 40, 50, 60, 70]
        target = 10
        assert binary_search(seq, target) == 0

        index, metrics = binary_search_instrumented(seq, target)
        assert index == 0
        # Probe 1: mid=3 (40 != 10, 40 < 10 False -> high=2) -> 2 comps
        # Probe 2: mid=1 (20 != 10, 20 < 10 False -> high=0) -> 2 comps
        # Probe 3: mid=0 (10 == 10 True) -> 1 comp
        # Total: 2 + 2 + 1 = 5 comparisons
        assert metrics.key_comparisons == 5
        assert metrics.equality_comparisons == 3
        assert metrics.ordering_comparisons == 2

    def test_target_at_last_position(self):
        """Target at index n - 1."""
        seq = [10, 20, 30, 40, 50, 60, 70]
        target = 70
        assert binary_search(seq, target) == 6

        index, metrics = binary_search_instrumented(seq, target)
        assert index == 6
        # Probe 1: mid=3 (40 != 70, 40 < 70 True -> low=4) -> 2 comps
        # Probe 2: mid=5 (60 != 70, 60 < 70 True -> low=6) -> 2 comps
        # Probe 3: mid=6 (70 == 70 True) -> 1 comp
        # Total: 2 + 2 + 1 = 5 comparisons
        assert metrics.key_comparisons == 5
        assert metrics.equality_comparisons == 3
        assert metrics.ordering_comparisons == 2

    def test_target_missing_less_than_min(self):
        """Missing target smaller than all elements."""
        seq = [10, 20, 30, 40, 50, 60, 70]
        target = 5
        assert binary_search(seq, target) == -1

        index, metrics = binary_search_instrumented(seq, target)
        assert index == -1
        # Maximum tree depth for n=7 is 3 probes. Each unsuccessful probe costs 2 comparisons.
        # Total comparisons = 3 * 2 = 6.
        assert metrics.key_comparisons == 6
        assert metrics.equality_comparisons == 3
        assert metrics.ordering_comparisons == 3

    def test_target_missing_greater_than_max(self):
        """Missing target greater than all elements."""
        seq = [10, 20, 30, 40, 50, 60, 70]
        target = 100
        assert binary_search(seq, target) == -1

        index, metrics = binary_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == 6
        assert metrics.equality_comparisons == 3
        assert metrics.ordering_comparisons == 3

    def test_target_missing_intermediate(self):
        """Missing target between elements."""
        seq = [10, 20, 30, 40, 50, 60, 70]
        target = 35
        assert binary_search(seq, target) == -1

        index, metrics = binary_search_instrumented(seq, target)
        assert index == -1
        assert metrics.key_comparisons == 6

    def test_duplicate_elements_finds_valid_index(self):
        """With duplicates, returns one valid matching index."""
        seq = [1, 2, 3, 3, 3, 4, 5]
        target = 3
        idx = binary_search(seq, target)
        assert idx in {2, 3, 4}
        assert seq[idx] == target

        idx_inst, _ = binary_search_instrumented(seq, target)
        assert idx_inst in {2, 3, 4}
        assert seq[idx_inst] == target

    def test_negative_integers(self):
        """Handles negative integers sorted properly."""
        seq = [-100, -50, -20, -5, 0, 10, 25]
        assert binary_search(seq, -50) == 1
        assert binary_search(seq, 0) == 4
        assert binary_search(seq, -75) == -1

    def test_sequence_not_mutated(self):
        """Binary search must not mutate input sequence."""
        seq = [1, 3, 5, 7, 9, 11]
        copy = list(seq)
        binary_search(seq, 5)
        assert seq == copy

        binary_search_instrumented(seq, 5)
        assert seq == copy

    def test_precondition_check_sorted(self):
        """Asserts that check_sorted=True raises ValueError on unsorted inputs."""
        unsorted_seq = [5, 2, 8, 1, 9]
        with pytest.raises(ValueError, match="Precondition violated"):
            binary_search(unsorted_seq, 8, check_sorted=True)

        with pytest.raises(ValueError, match="Precondition violated"):
            binary_search_instrumented(unsorted_seq, 8, check_sorted=True)

        # When check_sorted is False (default), no exception is raised
        # (even if search behavior may be undefined on unsorted input)
        binary_search(unsorted_seq, 8, check_sorted=False)

    def test_logarithmic_bound_exhaustive(self):
        """Verifies logarithmic comparison bound for all elements across sizes 1 to 31."""
        import math

        for n in range(1, 32):
            seq = list(range(10, 10 + n * 10, 10))
            for i, target in enumerate(seq):
                idx, metrics = binary_search_instrumented(seq, target)
                assert idx == i
                # Maximum number of iterations is floor(log2(n)) + 1
                max_iterations = math.floor(math.log2(n)) + 1
                # In each iteration at most 2 comparisons (1 equality + 1 ordering)
                assert metrics.key_comparisons <= 2 * max_iterations
                assert metrics.loop_evaluations <= max_iterations + 1

