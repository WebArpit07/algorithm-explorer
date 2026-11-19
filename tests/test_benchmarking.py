"""Tests for benchmarking harness, input generators, telemetry, and figures.

Verifies statistical calculations, dataset generation, isolated copy semantics,
and reproducibility.
"""

import math
import os
import tempfile
import pytest

from src.benchmarking.harness import (
    benchmark_search_scenario,
    benchmark_sorting_scenario,
    run_pilot_benchmark,
)
from src.benchmarking.input_generators import (
    generate_random_list,
    generate_reverse_sorted_list,
    generate_sorted_list,
    generate_sorting_dataset,
    get_search_target,
)
from src.benchmarking.telemetry import (
    calculate_statistics,
    export_metadata_to_json,
    export_summaries_to_csv,
    export_trials_to_csv,
    get_environment_metadata,
)
from src.visualization.plots import compute_growth_table


class TestInputGenerators:
    """Validation of deterministic input generators."""

    def test_generate_sorted_list(self):
        arr = generate_sorted_list(10, step=5, start=100)
        assert len(arr) == 10
        assert arr == [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
        # Strictly increasing
        assert all(arr[i] < arr[i + 1] for i in range(len(arr) - 1))

    def test_generate_reverse_sorted_list(self):
        arr = generate_reverse_sorted_list(5, step=10, start=10)
        assert len(arr) == 5
        assert arr == [50, 40, 30, 20, 10]
        # Strictly decreasing
        assert all(arr[i] > arr[i + 1] for i in range(len(arr) - 1))

    def test_generate_random_list_deterministic(self):
        arr1 = generate_random_list(20, seed=123)
        arr2 = generate_random_list(20, seed=123)
        arr3 = generate_random_list(20, seed=999)

        assert arr1 == arr2  # Identical with same seed
        assert arr1 != arr3  # Different with different seed
        assert sorted(arr1) == generate_sorted_list(20)  # Contains exact same unique items

    def test_get_search_target_scenarios(self):
        seq = [10, 20, 30, 40, 50, 60, 70]
        assert get_search_target(seq, "first") == 10
        assert get_search_target(seq, "middle") == 40  # 7 // 2 = 3 -> seq[3] = 40
        assert get_search_target(seq, "last") == 70
        missing = get_search_target(seq, "missing")
        assert missing not in seq
        assert missing > max(seq)

    def test_generate_sorting_dataset_arrangements(self):
        s_arr = generate_sorting_dataset(5, "sorted")
        r_arr = generate_sorting_dataset(5, "reverse")
        rnd_arr = generate_sorting_dataset(5, "random", seed=42)

        assert s_arr == [10, 20, 30, 40, 50]
        assert r_arr == [50, 40, 30, 20, 10]
        assert sorted(rnd_arr) == s_arr


class TestTelemetryAndStatistics:
    """Validation of statistical telemetry calculations."""

    def test_calculate_statistics_known_values(self):
        data = [10.0, 20.0, 30.0, 40.0, 50.0]
        stats = calculate_statistics(data)
        assert stats["mean"] == 30.0
        assert stats["median"] == 30.0
        assert stats["min"] == 10.0
        assert stats["max"] == 50.0
        assert math.isclose(stats["std_dev"], 15.811388, rel_tol=1e-5)
        assert stats["q25"] == 20.0
        assert stats["q75"] == 40.0
        assert stats["iqr"] == 20.0

    def test_environment_metadata_structure(self):
        meta = get_environment_metadata(random_seed=42)
        assert "python_version" in meta
        assert "operating_system" in meta
        assert "timing_timer" in meta
        assert meta["random_seed"] == 42


class TestHarnessExecution:
    """Validation of execution harness and isolated copy semantics."""

    def test_benchmark_search_scenario(self):
        trials, summary = benchmark_search_scenario(
            algorithm_name="linear_search",
            input_size=50,
            scenario="last",
            repetitions=5,
            seed=42,
        )
        assert len(trials) == 5
        assert summary.input_size == 50
        assert summary.scenario == "last"
        assert summary.key_comparisons == 50
        assert summary.median_duration_ns > 0

    def test_benchmark_sorting_scenario_copies_input(self):
        # Bubble sort on reverse list of size 10
        trials, summary = benchmark_sorting_scenario(
            algorithm_name="bubble_sort",
            input_size=10,
            arrangement="reverse",
            repetitions=5,
            seed=42,
        )
        assert len(trials) == 5
        assert summary.input_size == 10
        assert summary.element_comparisons == 10 * 9 // 2  # 45
        assert summary.swaps == 10 * 9 // 2  # 45
        assert summary.median_duration_ns > 0

    def test_growth_table_computation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "growth.csv")
            df = compute_growth_table(csv_path)
            assert os.path.exists(csv_path)
            assert len(df) == 11
            assert "quadratic_n2" in df.columns
            # n=4: n^2=16, 2^n=16, n!=24
            row_4 = df[df["n"] == 4].iloc[0]
            assert row_4["quadratic_n2"] == 16.0
            assert row_4["exponential_2n"] == 16.0
            assert row_4["factorial_n_fact"] == 24.0


class TestFiguresAndDataOutputs:
    """Verifies that generated datasets and figures satisfy specification contracts."""

    def test_generated_csv_files_exist_and_non_empty(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        raw_search = os.path.join(root, "data", "raw", "search_benchmark_trials.csv")
        proc_search = os.path.join(root, "data", "processed", "search_benchmark_summary.csv")
        raw_sort = os.path.join(root, "data", "raw", "sorting_benchmark_trials.csv")
        proc_sort = os.path.join(root, "data", "processed", "sorting_benchmark_summary.csv")
        growth = os.path.join(root, "data", "processed", "growth_functions.csv")
        metadata = os.path.join(root, "data", "processed", "benchmark_metadata.json")

        for fpath in [raw_search, proc_search, raw_sort, proc_sort, growth, metadata]:
            assert os.path.exists(fpath), f"File {fpath} must exist"
            assert os.path.getsize(fpath) > 100, f"File {fpath} must be non-empty"

    def test_all_nine_figures_exist_in_dual_formats(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        figs_dir = os.path.join(root, "figures")
        figure_bases = [
            "figure1_common_growth_functions",
            "figure2_growth_hierarchy_log_scale",
            "figure3_search_operation_counts",
            "figure4_search_execution_times",
            "figure5_sorting_operation_counts",
            "figure6_sorting_execution_times",
            "figure7_insertion_sort_arrangements",
            "figure8_bubble_sort_arrangements",
            "figure9_theoretical_vs_experimental",
        ]

        for base in figure_bases:
            pdf_path = os.path.join(figs_dir, f"{base}.pdf")
            png_path = os.path.join(figs_dir, f"{base}.png")
            assert os.path.exists(pdf_path), f"Missing vector PDF: {pdf_path}"
            assert os.path.exists(png_path), f"Missing 300DPI PNG: {png_path}"
            assert os.path.getsize(pdf_path) > 1024
            assert os.path.getsize(png_path) > 1024


class TestJupyterNotebookIntegrity:
    """Verifies that the primary research notebook is valid and fully executed."""

    def test_notebook_exists_and_executed(self):
        import nbformat

        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        nb_path = os.path.join(root, "notebooks", "algorithm_explorer.ipynb")
        assert os.path.exists(nb_path), "Notebook file must exist"
        assert os.path.getsize(nb_path) > 50_000, "Notebook must contain executed content"

        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        code_cells = [c for c in nb.cells if c.cell_type == "code"]
        md_cells = [c for c in nb.cells if c.cell_type == "markdown"]

        assert len(code_cells) >= 15, "Notebook must have sufficient code cells"
        assert len(md_cells) >= 20, "Notebook must have comprehensive narrative markdown cells"

        # Every code cell must have an output and 0 errors
        for cell in code_cells:
            assert len(cell.outputs) > 0, "All code cells must be pre-executed with outputs"
            for out in cell.outputs:
                assert out.get("output_type") != "error", f"Found execution error: {out}"


