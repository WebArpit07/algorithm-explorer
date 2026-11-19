# Algorithm Explorer: An Analytical and Experimental Study of Algorithms, Growth of Functions and Computational Complexity

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Discrete Mathematics](https://img.shields.io/badge/Curriculum-Rosen%20Ch.%203-darkgreen.svg)](https://www.mheducation.com/)
[![Tests](https://img.shields.io/badge/pytest-64%20passed-brightgreen.svg)](#running-the-automated-test-suite)
[![Web Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20HTML5-brightgreen.svg)](#interactive-web-dashboard)
[![LaTeX Report](https://img.shields.io/badge/LaTeX-Overleaf%20Ready-success.svg)](#academic-monograph-and-latex-report)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook%20Pre--Executed-orange.svg)](#interactive-jupyter-research-notebook)
[![Reproducibility](https://img.shields.io/badge/Benchmarks-Reproducible%201--Command-blue.svg)](#reproducing-the-entire-experiment)
[![License: Academic](https://img.shields.io/badge/License-Academic%20Evaluation-orange.svg)](#)

## Overview

**Algorithm Explorer** is a rigorous academic software and analytical suite developed for university-level Discrete Mathematics and Computer Science study. Grounded in **Kenneth H. Rosen's *Discrete Mathematics and Its Applications* (8th Edition), Chapter 3**, it investigates:

* **Section 3.1: Algorithms** — Specification, pseudocode, loop invariants, and deterministic state transitions.
* **Section 3.2: The Growth of Functions** — Asymptotic notations ($\mathcal{O}, \Omega, \Theta$), witness pairs $(C, k)$, and complexity hierarchies ($1 \prec \log n \prec n \prec n \log n \prec n^2 \prec 2^n \prec n!$).
* **Section 3.3: Complexity of Algorithms** — Exact operation counts (comparisons, data movements), best-, worst-, and average-case analysis, and space/time tradeoffs.

---

## Academic Monograph and LaTeX Report

The comprehensive formal academic report is structured as a modular LaTeX monograph ready for both local compilation and Overleaf deployment.

* **Root Master Document**: [`Algorithm_Explorer_Report.tex`](file:///d:/DiscreteMathsProject_202612120/Algorithm_Explorer_Report.tex)
* **Modular LaTeX Directory**: [`latex/`](file:///d:/DiscreteMathsProject_202612120/latex/)
  - `config.tex`: Author metadata, course title, roll number, and dashboard URL parameters.
  - `styles/academic_report.sty`: Typography, geometry, booktabs, listings, hyperref, and fancyhdr definitions.
  - `references.bib`: Complete BibTeX database (Rosen 8th ed., CLRS 4th ed., Knuth Vol 3, Hoare, Peters).
  - `chapters/`: 10 comprehensive academic chapters and 4 detailed appendices.
  - `tables/`: Dynamically generated LaTeX booktabs tables synced from empirical benchmark CSVs.
  - `figures/`: Dual-format synchronized publication figures (`.pdf` and `.png`).
* **Overleaf Distribution Package**: [`Algorithm_Explorer_Report_Overleaf.zip`](file:///d:/DiscreteMathsProject_202612120/Algorithm_Explorer_Report_Overleaf.zip) (Self-contained, 1-click upload).

### Compiling and Packaging the Report

```powershell
# Automated preparation, Overleaf packaging, and local PDF compilation:
python scripts/build_report.py

# To only refresh LaTeX tables and copy figure assets:
python scripts/prepare_report_assets.py

# To clean auxiliary build artifacts (.aux, .log, .toc, .bbl, etc.):
python scripts/build_report.py --clean
```

#### Option A: 1-Click Upload to Overleaf (Recommended)
1. Navigate to [Overleaf](https://www.overleaf.com/project) and log in.
2. Click **New Project** $\rightarrow$ **Upload Project**.
3. Select `Algorithm_Explorer_Report_Overleaf.zip` from this directory.
4. Click **Recompile**. Overleaf automatically compiles with standard TeX Live.

#### Option B: Local Windows PDF Compilation
Install MiKTeX or TeX Live via the Windows Package Manager:
```powershell
winget install MiKTeX.MiKTeX
# Once installed, reopen terminal and compile:
python scripts/build_report.py
```

---

## Interactive Web Dashboard

A polished, standalone, interactive web application is provided in [`dashboard/`](file:///d:/DiscreteMathsProject_202612120/dashboard/) for live algorithmic visualization and performance exploration:

* **Entry Point**: [`dashboard/index.html`](file:///d:/DiscreteMathsProject_202612120/dashboard/index.html)
* **Design Philosophy**: Zero-framework, zero-CDN-dependency vanilla ES2022 JavaScript, semantic HTML5, modern CSS3 dark theme, and custom pure-SVG charting.
* **Key Visualizers & Labs**:
  1. *Algorithm Deep-Dive Explorer*: In-depth mathematical specs, invariants, and Rosen pseudocode.
  2. *Interactive Searching Lab*: Step-by-step probing, boundary checks, and sorted precondition enforcement.
  3. *Interactive Sorting Lab*: Real-time vertical bar chart animation of fixed-pass Bubble Sort vs adaptive Insertion Sort.
  4. *Head-to-Head Comparison Lab*: Live browser simulations verifying asymptotic scaling and the Inversion Equivalence Theorem ($\text{Swaps} \equiv \text{Shifts} \equiv \text{Inversions}$).
  5. *Growth of Functions Lab*: Interactive SVG curves for the 7 canonical growth rates ($1, \log_2 n, n, n \log_2 n, n^2, 2^n, n!$) with logarithmic $\log_{10}$ Y-axis toggle.
  6. *Python 3.14.7 Experimental Microbenchmarks Viewer*: Interactive tables loaded from `dashboard/data/benchmark_data.json` presenting recorded M3 telemetry.

### Running the Dashboard Locally

```powershell
# Method A: Python HTTP Server (Recommended)
python -m http.server 8000
# Then open: http://localhost:8000/dashboard/

# Method B: Direct File Opening
# Open dashboard/index.html directly in any web browser.
```

### Production Cloudflare Pages Deployment

The official production release is deployed on **Cloudflare Pages** via Git integration with the private repository:
* **Production URL**: [`https://algorithm-explorer.glitchhunter69.workers.dev/`](https://algorithm-explorer.glitchhunter69.workers.dev/)
* **GitHub Repository**: [`WebArpit07/algorithm-explorer`](https://github.com/WebArpit07/algorithm-explorer) (Private)
* **Build Target**: Root directory blank, build command `exit 0`, build output directory `dashboard`
* **Complete Deployment Specification**: Refer to [`CLOUDFLARE_DEPLOYMENT.md`](file:///d:/DiscreteMathsProject_202612120/CLOUDFLARE_DEPLOYMENT.md) for full configuration, build parameters, and deployment audit logs.

---

## Interactive Jupyter Research Notebook

The primary interactive deliverable is located at:
[`notebooks/algorithm_explorer.ipynb`](file:///d:/DiscreteMathsProject_202612120/notebooks/algorithm_explorer.ipynb)

It is pre-executed with all cell outputs, styled DataFrames, and inline Matplotlib visualizations preserved.

### Notebook Structure
- **Section 1**: Title, Context, Objectives, Scope, and Research Questions
- **Section 2**: Fundamentals of Algorithms (Rosen §3.1)
- **Section 3**: The Growth of Functions (Rosen §3.2)
- **Section 4**: Asymptotic Notations: $\mathcal{O}$, $\Omega$, $\Theta$ (Rosen §3.2)
- **Section 5**: Complexity of Algorithms (Rosen §3.3)
- **Section 6**: In-Depth Study of the 4 Algorithms (Live Source Code, Traces, Proofs, Demos)
- **Section 7**: Experimental Benchmarking Methodology
- **Section 8**: Mathematical Growth Function Visualizations
- **Section 9**: Empirical Searching Analysis (Linear vs. Binary Search)
- **Section 10**: Empirical Sorting Analysis (Bubble Sort vs. Insertion Sort, Inversion Dynamics)
- **Section 11**: Theoretical vs. Experimental Telemetry & Pre-Notebook Data Audit
- **Section 12**: Comparative Findings & Educational Insights
- **Section 13**: Academic Conclusions
- **Section 14**: References (Rosen, CLRS, Knuth)

### Opening & Executing the Notebook
```powershell
# Option A: Open with standard Jupyter Lab / Notebook interface
jupyter notebook notebooks/algorithm_explorer.ipynb

# Option B: Headless re-execution and compilation via build script
python scripts/build_notebook.py
```

---

## Algorithms Analyzed

### 1. Linear Search (Rosen §3.1, Algorithm 2)
* **Description**: Sequentially traverses an input sequence from index $0$ to $n-1$, returning the index of the first matching element, or $-1$ if absent.
* **Complexity**:
  - *Best Case*: $\Theta(1)$ key comparisons ($1$ comparison when target is at index $0$).
  - *Worst Case*: $\Theta(n)$ key comparisons (target at index $n-1$ or absent; exactly $n$ comparisons).
  - *Average Case (Successful Search)*: Under uniform distribution: $C_{\text{avg}} = \frac{n + 1}{2} = \Theta(n)$.
  - *Unsuccessful Search*: Exactly $n$ key comparisons.
* **Metrics**: `key_comparisons` and `loop_evaluations`.

---

### 2. Binary Search (Rosen §3.1, Algorithm 3)
* **Description**: Iterative divide-and-conquer search on a pre-sorted sequence.
* **Precondition**: Sequence must be sorted in non-decreasing order ($O(n)$ check via `check_sorted=True`).
* **Exact Comparison Counting Convention**:
  1. Equality comparison: $\text{seq}[\text{mid}] == \text{target}$ ($1$ comparison).
  2. Ordering comparison: $\text{seq}[\text{mid}] < \text{target}$ ($1$ comparison).
  Terminating probe costs $1$ comparison; non-terminating probe costs $2$ key comparisons. Loop condition checks ($\text{low} \le \text{high}$) are tracked distinctly as `loop_evaluations`.
* **Complexity**:
  - *Best Case*: $\Theta(1)$ key comparisons ($1$ comparison when target is at initial midpoint).
  - *Worst Case*: $\Theta(\log n)$ key comparisons (at most $2(\lfloor \log_2 n \rfloor + 1)$ comparisons).
  - *Average Case*: $\Theta(\log n)$ key comparisons under uniform target distribution.

---

### 3. Bubble Sort (Rosen §3.1, Algorithm 4)
* **Description**: In-place adjacent exchange sort into ascending order. Preserves duplicate element ordering (stable sort).
* **Textbook Standard Requirement**: Exactly implements the classical $n - 1$ fixed passes without early-termination flags.
* **Complexity**:
  - *Comparisons (All Cases)*: Exactly:
    $$\sum_{i=0}^{n-2} (n - 1 - i) = (n - 1) + (n - 2) + \dots + 1 = \frac{n(n - 1)}{2} = \Theta(n^2)$$
  - *Best-Case Swaps*: $0$ (when input is already sorted).
  - *Worst-Case Swaps*: Exactly $\frac{n(n - 1)}{2}$ swaps for distinct reverse-sorted input.
  - *Average-Case Swaps*: $\frac{n(n - 1)}{4} = \Theta(n^2)$ for random permutations.

---

### 4. Insertion Sort (Rosen §3.1, Algorithm 5)
* **Description**: Incremental insertion into a growing sorted prefix. Preserves stability.
* **Shift vs Insertion Definition**:
  - *Right Shift*: Copying an existing element to the right ($\text{arr}[i+1] = \text{arr}[i]$).
  - *Insertion*: Assigning the stored key into its target slot ($\text{arr}[i+1] = \text{key}$). This is NOT counted as a right shift.
* **Complexity**:
  - *Best Case (Already Sorted)*: Comparisons: $n - 1 = \Theta(n)$. Right Shifts: $0$.
  - *Worst Case (Distinct Reverse Sorted)*: Comparisons: $\frac{n(n-1)}{2} = \Theta(n^2)$. Right Shifts: $\frac{n(n-1)}{2} = \Theta(n^2)$.
  - *Average Case*: $\Theta(n^2)$ comparisons and right shifts ($\approx n^2 / 4$).

---

## Directory Architecture

```text
DiscreteMathsProject_202612120/
├── Algorithm_Explorer_Report.tex             # Master academic LaTeX root document
├── Algorithm_Explorer_Report_Overleaf.zip    # Self-contained Overleaf 1-click deployment bundle
├── dashboard/                                # Standalone interactive HTML5/SVG web dashboard
│   ├── index.html                            # Dashboard single-page application
│   ├── README.md                             # Dashboard technical & deployment documentation
│   ├── css/
│   │   └── style.css                         # Dark academic theme & responsive animations
│   ├── js/
│   │   ├── algorithms.js                     # Step-generator state machines for 4 algorithms
│   │   ├── visualizations.js                 # DOM array & SVG bar chart rendering engines
│   │   ├── charts.js                         # Pure SVG growth functions & comparison charts
│   │   └── app.js                            # Lab controllers & benchmark table renderers
│   └── data/
│       ├── benchmark_data.json               # Processed M3 Python benchmark dataset
│       └── benchmark_data.js                 # Script export for CORS-free local execution
├── data/
│   ├── raw/
│   │   ├── search_benchmark_trials.csv       # 1,680 individual search trials
│   │   └── sorting_benchmark_trials.csv      # 1,080 individual sorting trials
│   └── processed/
│       ├── search_benchmark_summary.csv      # Aggregated search statistics (56 configs)
│       ├── sorting_benchmark_summary.csv     # Aggregated sorting statistics (36 configs)
│       ├── growth_functions.csv              # Canonical mathematical growth values
│       └── benchmark_metadata.json           # Machine, CPU, OS, and timestamp telemetry
├── figures/                                  # Dual-format publication figures (.pdf & .png)
│   ├── figure1_common_growth_functions.*     # Common polynomial & sub-polynomial curves
│   ├── figure2_growth_hierarchy_log_scale.*  # Full hierarchy (1 to n!) on semi-log scale
│   ├── figure3_search_operation_counts.*     # Linear vs Binary key comparisons
│   ├── figure4_search_execution_times.*      # Search execution times with error bars
│   ├── figure5_sorting_operation_counts.*    # Bubble vs Insertion comparisons & shifts
│   ├── figure6_sorting_execution_times.*     # Sorting execution times (linear & log-log)
│   ├── figure7_insertion_sort_arrangements.* # Insertion sort across 3 topologies
│   ├── figure8_bubble_sort_arrangements.*    # Bubble sort comparison invariance
│   └── figure9_theoretical_vs_experimental.* # Exact theoretical formulas vs measurements
├── latex/
│   ├── config.tex                            # Author metadata, course title, roll number
│   ├── main.tex                              # Secondary master document for modular compilation
│   ├── references.bib                        # Standard BibTeX bibliography database
│   ├── styles/
│   │   └── academic_report.sty               # Custom typography and package styling
│   ├── chapters/                             # 14 modular academic chapters and appendices
│   ├── tables/                               # Auto-generated booktabs LaTeX tables
│   └── figures/                              # Synchronized report figures (.pdf & .png)
├── notebooks/
│   └── algorithm_explorer.ipynb              # Fully executed interactive research notebook
├── scripts/
│   ├── run_benchmarks.py                     # Single-command automated benchmark runner
│   ├── generate_figures.py                   # Publication-grade figure generation script
│   ├── build_notebook.py                     # Headless notebook build & execution runner
│   ├── prepare_report_assets.py              # LaTeX tables and figures generator
│   ├── build_report.py                       # LaTeX compiler and Overleaf packager
│   ├── export_dashboard_data.py              # Export M3 processed data to JSON/JS for dashboard
│   └── test_dashboard_algorithms.js          # Node.js automated test runner for algorithms.js
├── src/
│   ├── algorithms/                           # Search and Sorting implementations
│   ├── benchmarking/                         # Harness, input generators, and telemetry
│   └── visualization/                        # Matplotlib publication plotting routines
├── tests/
│   ├── test_search.py                        # 24 unit tests for search algorithms
│   ├── test_sorting.py                       # 18 unit tests for sorting algorithms
│   ├── test_benchmarking.py                  # 13 unit tests for harness, outputs & notebook
│   ├── test_report.py                        # 5 unit tests for LaTeX report and Overleaf zip
│   └── test_dashboard.py                     # 4 integration tests for HTML5 web dashboard
├── .github/
│   └── workflows/
│       └── deploy.yml                        # GitHub Actions automated Pages deployment
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Reproducing the Entire Experiment

From the project root directory:

```powershell
# 1. Execute all empirical benchmarks (generates data/raw and data/processed)
python scripts/run_benchmarks.py

# 2. Synthesize all 9 publication figures (.pdf and .png into figures/)
python scripts/generate_figures.py

# 3. Build, execute, and verify the Jupyter Research Notebook
python scripts/build_notebook.py

# 4. Export Python benchmark telemetry for the web dashboard
python scripts/export_dashboard_data.py

# 5. Prepare LaTeX tables, copy figures, and package Overleaf archive
python scripts/build_report.py

# 6. Execute all unit, regression, document, and dashboard validation tests
python -m pytest -v
```

---

## Running the Automated Test Suite

```powershell
python -m pytest -v
```

All 64 tests validate:
- Algorithmic correctness across edge cases, negative integers, duplicates, and empty lists.
- Sorting stability and in-place reference preservation.
- Precondition enforcement (`check_sorted=True` for binary search).
- Isolated copy semantics in the benchmarking harness.
- Correctness of descriptive statistics (mean, median, std dev, quartiles, IQR).
- Existence and non-emptiness of all generated data files and dual-format figures.
- Structure, integrity, and execution status of `notebooks/algorithm_explorer.ipynb`.
- Integrity of LaTeX source files, booktabs table generation, and Overleaf distribution zip.
- Web dashboard HTML structure, CSS rules, Node.js algorithm step tests, and benchmark JSON integrity.
