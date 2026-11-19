"""Visualization subpackage for publication-grade figure generation."""

from src.visualization.plots import (
    compute_growth_table,
    plot_figure1_common_growth_functions,
    plot_figure2_growth_hierarchy_log_scale,
    plot_figure3_search_operation_counts,
    plot_figure4_search_execution_times,
    plot_figure5_sorting_operation_counts,
    plot_figure6_sorting_execution_times,
    plot_figure7_insertion_sort_arrangements,
    plot_figure8_bubble_sort_arrangements,
    plot_figure9_theoretical_vs_experimental,
    save_dual_format,
)

__all__ = [
    "compute_growth_table",
    "save_dual_format",
    "plot_figure1_common_growth_functions",
    "plot_figure2_growth_hierarchy_log_scale",
    "plot_figure3_search_operation_counts",
    "plot_figure4_search_execution_times",
    "plot_figure5_sorting_operation_counts",
    "plot_figure6_sorting_execution_times",
    "plot_figure7_insertion_sort_arrangements",
    "plot_figure8_bubble_sort_arrangements",
    "plot_figure9_theoretical_vs_experimental",
]
