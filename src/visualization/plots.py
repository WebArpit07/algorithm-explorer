"""Publication-grade visualization module for Algorithm Explorer.

Generates academic figures for theoretical growth of functions, empirical
operation counts, execution durations, and theoretical-vs-experimental
comparisons according to Kenneth H. Rosen, Discrete Mathematics and Its
Applications (8th Edition), Chapter 3.
"""

from __future__ import annotations

import math
import os
from typing import Sequence

import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Set consistent academic figure styling
plt.rcParams.update(
    {
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 13,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.grid": True,
        "grid.alpha": 0.5,
        "grid.linestyle": "--",
        "lines.linewidth": 1.75,
        "lines.markersize": 5,
    }
)


def save_dual_format(fig: plt.Figure, base_filename: str, output_dir: str = "figures") -> tuple[str, str]:
    """Saves a matplotlib figure in both vector PDF and 300 DPI PNG formats."""
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
    png_path = os.path.join(output_dir, f"{base_filename}.png")

    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    fig.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return pdf_path, png_path


# =====================================================================
# SECTION 6: MATHEMATICAL GROWTH OF FUNCTIONS
# =====================================================================

def compute_growth_table(output_csv: str = "data/processed/growth_functions.csv") -> pd.DataFrame:
    """Generates numerical growth comparison data for canonical Rosen §3.2 functions."""
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    n_values = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    rows = []

    for n in n_values:
        # Constant: 1
        c_val = 1
        # Logarithmic: log2(n)
        log_val = math.log2(n) if n > 0 else 0.0
        # Linear: n
        lin_val = float(n)
        # Linearithmic: n log2(n)
        linlog_val = n * math.log2(n) if n > 0 else 0.0
        # Quadratic: n^2
        quad_val = float(n**2)
        # Exponential: 2^n (cap or format to avoid unreadable representations)
        exp_val = float(2**n) if n <= 64 else float("inf")
        # Factorial: n! (cap to avoid float overflow)
        fact_val = float(math.factorial(n)) if n <= 20 else float("inf")

        rows.append(
            {
                "n": n,
                "constant_1": c_val,
                "logarithmic_log2_n": round(log_val, 4),
                "linear_n": lin_val,
                "linearithmic_n_log2_n": round(linlog_val, 4),
                "quadratic_n2": quad_val,
                "exponential_2n": exp_val,
                "factorial_n_fact": fact_val,
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    return df


def plot_figure1_common_growth_functions(output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 1: Common polynomial and sub-polynomial growth functions (Rosen §3.2).

    Examines 1, log2(n), n, n log2(n), and n^2 over n in [1, 100].
    """
    n = np.linspace(1, 100, 400)
    f_const = np.ones_like(n)
    f_log = np.log2(n)
    f_lin = n
    f_linlog = n * np.log2(n)
    f_quad = n**2

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n, f_const, label=r"Constant: $\mathcal{O}(1)$", color="#7f7f7f", linestyle=":")
    ax.plot(n, f_log, label=r"Logarithmic: $\mathcal{O}(\log_2 n)$", color="#2ca02c")
    ax.plot(n, f_lin, label=r"Linear: $\mathcal{O}(n)$", color="#1f77b4")
    ax.plot(n, f_linlog, label=r"Linearithmic: $\mathcal{O}(n \log_2 n)$", color="#ff7f0e")
    ax.plot(n, f_quad, label=r"Quadratic: $\mathcal{O}(n^2)$", color="#d62728")

    ax.set_title("Figure 1: Comparison of Common Growth Functions (Rosen §3.2)")
    ax.set_xlabel("Input Size ($n$)")
    ax.set_ylabel("Operation Count / Function Value $f(n)$")
    ax.set_xlim(1, 100)
    ax.set_ylim(0, 10000)
    ax.legend(loc="upper left", frameon=True)

    return save_dual_format(fig, "figure1_common_growth_functions", output_dir)


def plot_figure2_growth_hierarchy_log_scale(output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 2: Complete growth hierarchy on semi-log scale (Rosen §3.2).

    Displays 1, log2(n), n, n log2(n), n^2, 2^n, and n! on a logarithmic Y-scale
    over n in [1, 14] to illustrate asymptotic domination without overflow.
    """
    n_int = np.arange(1, 15)
    f_const = [1 for _ in n_int]
    f_log = [math.log2(x) if x > 0 else 0 for x in n_int]
    f_lin = [x for x in n_int]
    f_linlog = [x * math.log2(x) if x > 0 else 0 for x in n_int]
    f_quad = [x**2 for x in n_int]
    f_exp = [2**x for x in n_int]
    f_fact = [math.factorial(x) for x in n_int]

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(n_int, f_const, "o:", label=r"$\mathcal{O}(1)$", color="#7f7f7f")
    ax.plot(n_int, f_log, "s-", label=r"$\mathcal{O}(\log_2 n)$", color="#2ca02c")
    ax.plot(n_int, f_lin, "^-", label=r"$\mathcal{O}(n)$", color="#1f77b4")
    ax.plot(n_int, f_linlog, "v-", label=r"$\mathcal{O}(n \log_2 n)$", color="#ff7f0e")
    ax.plot(n_int, f_quad, "D-", label=r"$\mathcal{O}(n^2)$", color="#9467bd")
    ax.plot(n_int, f_exp, "p-", label=r"$\mathcal{O}(2^n)$", color="#e377c2")
    ax.plot(n_int, f_fact, "*-", label=r"$\mathcal{O}(n!)$", color="#d62728")

    ax.set_yscale("log")
    ax.set_title("Figure 2: Hierarchy of Functions on Semi-Log Scale (Rosen §3.2)")
    ax.set_xlabel("Input Size ($n$)")
    ax.set_ylabel(r"Growth Magnitude (Logarithmic Scale $\log_{10} f(n)$)")
    ax.set_xticks(n_int)
    ax.set_ylim(0.5, 1e11)
    ax.legend(loc="upper left", frameon=True)

    return save_dual_format(fig, "figure2_growth_hierarchy_log_scale", output_dir)


# =====================================================================
# SECTION 8: SEARCHING & SORTING EMPIRICAL FIGURES
# =====================================================================

def plot_figure3_search_operation_counts(search_df: pd.DataFrame, output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 3: Linear Search vs Binary Search — Key Comparisons."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Scenario: Worst Case (Missing Target)
    sub_worst = search_df[search_df["scenario"] == "missing"]
    lin_worst = sub_worst[sub_worst["algorithm"] == "linear_search"].sort_values("input_size")
    bin_worst = sub_worst[sub_worst["algorithm"] == "binary_search"].sort_values("input_size")

    ax1.plot(lin_worst["input_size"], lin_worst["key_comparisons"], "o-", color="#d62728", label="Linear Search (Unsuccessful: $n$)")
    ax1.plot(bin_worst["input_size"], bin_worst["key_comparisons"], "s-", color="#1f77b4", label=r"Binary Search (Unsuccessful: $2\lfloor\log_2 n\rfloor + 2$)")
    ax1.set_title("Linear Scale: Unsuccessful Search Comparisons")
    ax1.set_xlabel("Input Size ($n$)")
    ax1.set_ylabel("Key Comparisons")
    ax1.legend()

    # Scenario: Common positions on Log-Log Scale
    for scen, marker, ls in [("first", "o", "-"), ("middle", "s", "--"), ("last", "^", "-.")]:
        s_df = search_df[search_df["scenario"] == scen]
        lin_data = s_df[s_df["algorithm"] == "linear_search"].sort_values("input_size")
        bin_data = s_df[s_df["algorithm"] == "binary_search"].sort_values("input_size")
        ax2.plot(lin_data["input_size"], lin_data["key_comparisons"], marker=marker, linestyle=ls, label=f"Linear ({scen})")
        ax2.plot(bin_data["input_size"], bin_data["key_comparisons"], marker=marker, linestyle=ls, label=f"Binary ({scen})")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title("Log-Log Scale: Comparisons Across Scenarios")
    ax2.set_xlabel("Input Size ($n$) [log]")
    ax2.set_ylabel("Key Comparisons [log]")
    ax2.legend(fontsize=8)

    fig.suptitle("Figure 3: Linear Search vs. Binary Search — Operation Counts (Rosen §3.3)")
    fig.tight_layout()
    return save_dual_format(fig, "figure3_search_operation_counts", output_dir)


def plot_figure4_search_execution_times(search_df: pd.DataFrame, output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 4: Linear Search vs Binary Search — Execution Times."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    sub_df = search_df[search_df["scenario"].isin(["first", "middle", "last", "missing"])]

    # Plot Linear Search worst-case (missing) and average (middle)
    lin_miss = sub_df[(sub_df["algorithm"] == "linear_search") & (sub_df["scenario"] == "missing")].sort_values("input_size")
    lin_mid = sub_df[(sub_df["algorithm"] == "linear_search") & (sub_df["scenario"] == "middle")].sort_values("input_size")
    bin_miss = sub_df[(sub_df["algorithm"] == "binary_search") & (sub_df["scenario"] == "missing")].sort_values("input_size")
    bin_mid = sub_df[(sub_df["algorithm"] == "binary_search") & (sub_df["scenario"] == "middle")].sort_values("input_size")

    # Convert ns to microseconds for readable axis
    ax.errorbar(lin_miss["input_size"], lin_miss["median_duration_ns"] / 1e3, yerr=lin_miss["std_dev_duration_ns"] / 1e3,
                 fmt="o-", color="#d62728", capsize=3, label="Linear Search (Missing Target, Worst)")
    ax.errorbar(lin_mid["input_size"], lin_mid["median_duration_ns"] / 1e3, yerr=lin_mid["std_dev_duration_ns"] / 1e3,
                 fmt="v--", color="#ff7f0e", capsize=3, label="Linear Search (Middle Target)")
    ax.errorbar(bin_miss["input_size"], bin_miss["median_duration_ns"] / 1e3, yerr=bin_miss["std_dev_duration_ns"] / 1e3,
                 fmt="s-", color="#1f77b4", capsize=3, label="Binary Search (Missing Target)")
    ax.errorbar(bin_mid["input_size"], bin_mid["median_duration_ns"] / 1e3, yerr=bin_mid["std_dev_duration_ns"] / 1e3,
                 fmt="^-", color="#2ca02c", capsize=3, label="Binary Search (Middle Target)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Figure 4: Linear Search vs. Binary Search — Execution Times")
    ax.set_xlabel("Input Size ($n$) [log scale]")
    ax.set_ylabel(r"Median Execution Time ($\mu$s) [log scale]")
    ax.legend(loc="upper left")

    return save_dual_format(fig, "figure4_search_execution_times", output_dir)


def plot_figure5_sorting_operation_counts(sort_df: pd.DataFrame, output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 5: Bubble Sort vs Insertion Sort — Operation Counts (Random Input)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    rand_df = sort_df[sort_df["arrangement"] == "random"]
    b_data = rand_df[rand_df["algorithm"] == "bubble_sort"].sort_values("input_size")
    i_data = rand_df[rand_df["algorithm"] == "insertion_sort"].sort_values("input_size")

    # Comparisons
    ax1.plot(b_data["input_size"], b_data["element_comparisons"], "o-", color="#d62728", label=r"Bubble Sort Comp: $n(n-1)/2$")
    ax1.plot(i_data["input_size"], i_data["element_comparisons"], "s-", color="#1f77b4", label=r"Insertion Sort Comp: $\approx n^2/4$")
    ax1.set_title("Element Comparisons (Random Permutations)")
    ax1.set_xlabel("Input Size ($n$)")
    ax1.set_ylabel("Element Comparisons")
    ax1.legend()

    # Data movements: Bubble swaps vs Insertion right shifts
    ax2.plot(b_data["input_size"], b_data["swaps"], "o--", color="#d62728", label="Bubble Sort Swaps")
    ax2.plot(i_data["input_size"], i_data["right_shifts"], "s--", color="#1f77b4", label="Insertion Sort Right Shifts")
    ax2.set_title("Data Movements: Swaps vs. Right Shifts")
    ax2.set_xlabel("Input Size ($n$)")
    ax2.set_ylabel("Operation Count")
    ax2.legend()

    fig.suptitle("Figure 5: Bubble Sort vs. Insertion Sort — Operation Counts (Rosen §3.3)")
    fig.tight_layout()
    return save_dual_format(fig, "figure5_sorting_operation_counts", output_dir)


def plot_figure6_sorting_execution_times(sort_df: pd.DataFrame, output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 6: Bubble Sort vs Insertion Sort — Execution Times."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Linear scale for random permutations
    rand_df = sort_df[sort_df["arrangement"] == "random"]
    b_rand = rand_df[rand_df["algorithm"] == "bubble_sort"].sort_values("input_size")
    i_rand = rand_df[rand_df["algorithm"] == "insertion_sort"].sort_values("input_size")

    ax1.errorbar(b_rand["input_size"], b_rand["median_duration_ns"] / 1e6, yerr=b_rand["std_dev_duration_ns"] / 1e6,
                 fmt="o-", color="#d62728", capsize=3, label="Bubble Sort (Random)")
    ax1.errorbar(i_rand["input_size"], i_rand["median_duration_ns"] / 1e6, yerr=i_rand["std_dev_duration_ns"] / 1e6,
                 fmt="s-", color="#1f77b4", capsize=3, label="Insertion Sort (Random)")
    ax1.set_title("Linear Scale: Execution Duration (Random)")
    ax1.set_xlabel("Input Size ($n$)")
    ax1.set_ylabel("Median Time (ms)")
    ax1.legend()

    # Log-Log scale across all three arrangements
    styles = {"sorted": ("g", ":"), "random": ("b", "-"), "reverse": ("r", "--")}
    for arr, (c, ls) in styles.items():
        arr_df = sort_df[sort_df["arrangement"] == arr]
        b_sub = arr_df[arr_df["algorithm"] == "bubble_sort"].sort_values("input_size")
        i_sub = arr_df[arr_df["algorithm"] == "insertion_sort"].sort_values("input_size")
        ax2.plot(b_sub["input_size"], b_sub["median_duration_ns"] / 1e6, marker="o", color=c, linestyle=ls, label=f"Bubble ({arr})")
        ax2.plot(i_sub["input_size"], i_sub["median_duration_ns"] / 1e6, marker="s", color=c, linestyle=ls, alpha=0.6, label=f"Insertion ({arr})")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title("Log-Log Scale: All Input Arrangements")
    ax2.set_xlabel("Input Size ($n$) [log]")
    ax2.set_ylabel("Median Time (ms) [log]")
    ax2.legend(fontsize=8, ncol=2)

    fig.suptitle("Figure 6: Bubble Sort vs. Insertion Sort — Execution Times")
    fig.tight_layout()
    return save_dual_format(fig, "figure6_sorting_execution_times", output_dir)


def plot_figure7_insertion_sort_arrangements(sort_df: pd.DataFrame, output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 7: Insertion Sort — Comparisons & Shifts across Sorted, Random, and Reverse."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ins_df = sort_df[sort_df["algorithm"] == "insertion_sort"]
    sorted_d = ins_df[ins_df["arrangement"] == "sorted"].sort_values("input_size")
    random_d = ins_df[ins_df["arrangement"] == "random"].sort_values("input_size")
    reverse_d = ins_df[ins_df["arrangement"] == "reverse"].sort_values("input_size")

    # Comparisons
    ax1.plot(sorted_d["input_size"], sorted_d["element_comparisons"], "o-", color="#2ca02c", label=r"Sorted: Best $\Theta(n)$ ($n-1$)")
    ax1.plot(random_d["input_size"], random_d["element_comparisons"], "s--", color="#ff7f0e", label=r"Random: Avg $\Theta(n^2)$ ($\approx n^2/4$)")
    ax1.plot(reverse_d["input_size"], reverse_d["element_comparisons"], "^-", color="#d62728", label=r"Reverse: Worst $\Theta(n^2)$ ($n(n-1)/2$)")
    ax1.set_title("Insertion Sort: Element Comparisons")
    ax1.set_xlabel("Input Size ($n$)")
    ax1.set_ylabel("Comparisons")
    ax1.legend()

    # Execution Time
    ax2.plot(sorted_d["input_size"], sorted_d["median_duration_ns"] / 1e6, "o-", color="#2ca02c", label=r"Sorted: $\Theta(n)$ Runtime")
    ax2.plot(random_d["input_size"], random_d["median_duration_ns"] / 1e6, "s--", color="#ff7f0e", label=r"Random: $\Theta(n^2)$ Runtime")
    ax2.plot(reverse_d["input_size"], reverse_d["median_duration_ns"] / 1e6, "^-", color="#d62728", label=r"Reverse: $\Theta(n^2)$ Runtime")
    ax2.set_title("Insertion Sort: Execution Time (ms)")
    ax2.set_xlabel("Input Size ($n$)")
    ax2.set_ylabel("Median Time (ms)")
    ax2.legend()

    fig.suptitle("Figure 7: Insertion Sort Across Input Arrangements (Rosen §3.3)")
    fig.tight_layout()
    return save_dual_format(fig, "figure7_insertion_sort_arrangements", output_dir)


def plot_figure8_bubble_sort_arrangements(sort_df: pd.DataFrame, output_dir: str = "figures") -> tuple[str, str]:
    """FIGURE 8: Bubble Sort — Invariant Comparisons vs Dynamic Swaps."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    b_df = sort_df[sort_df["algorithm"] == "bubble_sort"]
    sorted_d = b_df[b_df["arrangement"] == "sorted"].sort_values("input_size")
    random_d = b_df[b_df["arrangement"] == "random"].sort_values("input_size")
    reverse_d = b_df[b_df["arrangement"] == "reverse"].sort_values("input_size")

    # Comparisons (All identical!)
    ax1.plot(sorted_d["input_size"], sorted_d["element_comparisons"], "o-", color="#2ca02c", label="Sorted Input")
    ax1.plot(random_d["input_size"], random_d["element_comparisons"], "x--", color="#ff7f0e", label="Random Input")
    ax1.plot(reverse_d["input_size"], reverse_d["element_comparisons"], "+:", color="#d62728", label="Reverse Input")
    ax1.set_title(r"Comparisons Invariance: Exactly $n(n-1)/2$")
    ax1.set_xlabel("Input Size ($n$)")
    ax1.set_ylabel("Element Comparisons")
    ax1.legend()

    # Swaps: 0 for sorted, n(n-1)/4 for random, n(n-1)/2 for reverse
    ax2.plot(sorted_d["input_size"], sorted_d["swaps"], "o-", color="#2ca02c", label="Sorted: 0 Swaps")
    ax2.plot(random_d["input_size"], random_d["swaps"], "s--", color="#ff7f0e", label=r"Random: $\approx n(n-1)/4$ Swaps")
    ax2.plot(reverse_d["input_size"], reverse_d["swaps"], "^-", color="#d62728", label=r"Reverse: $n(n-1)/2$ Swaps")
    ax2.set_title("Swaps Across Arrangements")
    ax2.set_xlabel("Input Size ($n$)")
    ax2.set_ylabel("Element Swaps")
    ax2.legend()

    fig.suptitle("Figure 8: Bubble Sort Invariance and Swaps (Rosen §3.1 Alg. 4 & §3.3)")
    fig.tight_layout()
    return save_dual_format(fig, "figure8_bubble_sort_arrangements", output_dir)


def plot_figure9_theoretical_vs_experimental(
    search_df: pd.DataFrame, sort_df: pd.DataFrame, output_dir: str = "figures"
) -> tuple[str, str]:
    """FIGURE 9: Direct Overlay of Mathematical Formulas vs. Empirical Measurements."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Linear Search Worst Case
    lin_worst = search_df[(search_df["algorithm"] == "linear_search") & (search_df["scenario"] == "missing")].sort_values("input_size")
    n_search = lin_worst["input_size"].values
    ax1.plot(n_search, n_search, "k--", label=r"Theory: $T(n) = n$")
    ax1.scatter(n_search, lin_worst["key_comparisons"], color="#d62728", zorder=3, label="Empirical Measured")
    ax1.set_title("Linear Search Worst-Case Key Comparisons")
    ax1.set_xlabel("Input Size ($n$)")
    ax1.set_ylabel("Comparisons")
    ax1.legend()

    # 2. Binary Search Worst Case (Unsuccessful)
    bin_worst = search_df[(search_df["algorithm"] == "binary_search") & (search_df["scenario"] == "missing")].sort_values("input_size")
    # In our implementation: 2 * (floor(log2(n)) + 1)
    theory_bin = [2 * (math.floor(math.log2(x)) + 1) for x in n_search]
    ax2.plot(n_search, theory_bin, "k--", label=r"Theory: $2(\lfloor\log_2 n\rfloor + 1)$")
    ax2.scatter(n_search, bin_worst["key_comparisons"], color="#1f77b4", zorder=3, label="Empirical Measured")
    ax2.set_title("Binary Search Worst-Case Key Comparisons")
    ax2.set_xlabel("Input Size ($n$)")
    ax2.set_ylabel("Comparisons")
    ax2.legend()

    # 3. Bubble Sort Fixed-Pass Comparisons
    b_rand = sort_df[(sort_df["algorithm"] == "bubble_sort") & (sort_df["arrangement"] == "random")].sort_values("input_size")
    n_sort = b_rand["input_size"].values
    theory_bubble = [x * (x - 1) // 2 for x in n_sort]
    ax3.plot(n_sort, theory_bubble, "k--", label=r"Theory: $n(n-1)/2$")
    ax3.scatter(n_sort, b_rand["element_comparisons"], color="#9467bd", zorder=3, label="Empirical Measured")
    ax3.set_title("Bubble Sort Element Comparisons (Any Input)")
    ax3.set_xlabel("Input Size ($n$)")
    ax3.set_ylabel("Comparisons")
    ax3.legend()

    # 4. Insertion Sort Reverse-Sorted Comparisons & Shifts
    i_rev = sort_df[(sort_df["algorithm"] == "insertion_sort") & (sort_df["arrangement"] == "reverse")].sort_values("input_size")
    theory_ins_rev = [x * (x - 1) // 2 for x in n_sort]
    ax4.plot(n_sort, theory_ins_rev, "k--", label=r"Theory: $n(n-1)/2$")
    ax4.scatter(n_sort, i_rev["element_comparisons"], color="#2ca02c", zorder=3, label="Empirical Comparisons")
    ax4.scatter(n_sort, i_rev["right_shifts"], marker="x", color="#ff7f0e", zorder=3, label="Empirical Right Shifts")
    ax4.set_title("Insertion Sort Reverse-Sorted Inversion Operations")
    ax4.set_xlabel("Input Size ($n$)")
    ax4.set_ylabel("Operations")
    ax4.legend()

    fig.suptitle("Figure 9: Mathematical Formulas vs. Empirical Telemetry (Rosen §3.3)", fontsize=13)
    fig.tight_layout()
    return save_dual_format(fig, "figure9_theoretical_vs_experimental", output_dir)
