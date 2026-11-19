# Algorithm Explorer — Interactive Web Dashboard

**Algorithm Explorer: Interactive Algorithm Analysis & Complexity Visualization** is a standalone, client-side academic web application designed to complement university-level study of **Kenneth H. Rosen's *Discrete Mathematics and Its Applications* (8th Edition), Chapter 3**.

---

## 1. Architectural Purpose & Theoretical Scope

The dashboard bridges discrete mathematical proofs with interactive visual exploration and real-world empirical performance telemetry. It delivers live simulations and visualizers for the four canonical algorithms studied throughout the project:

1. **Linear Search** (Rosen §3.1, Algorithm 2)
2. **Binary Search** (Rosen §3.1, Algorithm 3)
3. **Bubble Sort** (Rosen §3.1, Algorithm 4 — *Textbook Fixed-Pass Formulation*)
4. **Insertion Sort** (Rosen §3.1, Algorithm 5)

---

## 2. Distinction Between the Three Data Layers

To maintain rigorous scientific and academic integrity, the dashboard strictly distinguishes between three independent sources of data:

1. **Theoretical Mathematical Complexity ($\mathcal{O}, \Omega, \Theta$)**:
   - Closed-form mathematical formulas derived from Chapter 3 proofs (e.g., Bubble Sort comparisons $= \frac{n(n-1)}{2}$, Binary Search worst-case comparisons $= 2\lfloor \log_2 n \rfloor + 2$).
2. **Live Client-Side JavaScript Simulation**:
   - Interactive, step-by-step in-browser algorithm execution on user-defined arrays and sizes. Demonstrates instantaneous state changes, element comparisons, swaps, right shifts, and inversion counts. Timings in milliseconds are illustrative browser execution metrics and are explicitly labeled as such.
3. **Python 3.14.7 Empirical Microbenchmarks (M3 Data)**:
   - High-precision telemetry recorded from the isolated Python benchmarking harness across $n \in [100, 100\,000]$ and $k = 30$ replications with sub-microsecond batch calibration. Sourced directly from `dashboard/data/benchmark_data.json`.

---

## 3. Technology Stack & Zero-Dependency Design

- **HTML5 & CSS3**: Responsive, semantic structure with a modern dark theme inspired by scientific research tools. Mobile-friendly grid and flexbox layout with custom property theming.
- **Vanilla JavaScript (ES2022)**: Lightweight, modular architecture without external frameworks (no React, Angular, Vue, or Node.js required).
- **Pure SVG & DOM Rendering**: Custom-engineered charting for Growth of Functions curves and comparison bars. Zero external CDN dependencies, ensuring fast loading and complete offline availability.

---

## 4. Directory Structure

```text
dashboard/
├── index.html                  # Single-page web application
├── css/
│   └── style.css               # Professional academic dark theme and animations
├── js/
│   ├── algorithms.js           # Authoritative step-generator state machines
│   ├── visualizations.js       # Array grid and vertical bar DOM renderers
│   ├── charts.js               # Pure SVG Growth of Functions and Comparison charts
│   └── app.js                  # Application orchestrator and event handlers
├── data/
│   ├── benchmark_data.json     # Processed Python M3 benchmark dataset
│   └── benchmark_data.js       # Global variable script for CORS-free file:// protocol
├── assets/                     # Optional graphic assets and icons
└── README.md                   # Technical documentation and deployment guide
```

---

## 5. Local Execution

The dashboard can be executed locally using any modern web browser via either of two methods:

### Method A: Local HTTP Web Server (Recommended)
From the project root directory, launch Python's built-in HTTP server:
```powershell
python -m http.server 8000
```
Then navigate to:
```text
http://localhost:8000/dashboard/
```

### Method B: Direct File Opening
Double-click or open `dashboard/index.html` directly in your browser:
```text
file:///D:/DiscreteMathsProject_202612120/dashboard/index.html
```
*Note: The dual JSON/JS data export (`benchmark_data.js`) guarantees that all Python benchmark tables and metadata load instantly even when opened via the `file://` protocol.*

---

## 6. Key Interactive Features

1. **Algorithm Explorer Deep-Dive**:
   - Tabbed view displaying the formal definition, objective, working principle, loop invariants, textbook pseudocode, and $\Theta$ bounds for each algorithm.
2. **Interactive Searching Lab**:
   - Step, Play, Pause, Reset, and Speed controls.
   - Live visual highlights for active index, current probe, discarded search spaces (for Binary Search), and target match.
   - Precondition enforcement: Rejects Binary Search on unsorted sequences and provides a 1-click sort action.
3. **Interactive Sorting Lab**:
   - Vertical bar visualization with dynamic scaling and color coding for comparisons, swaps, right shifts, and sorted boundaries.
   - Strict adherence to Rosen's fixed-pass Bubble Sort ($n(n-1)/2$ comparisons without early exit).
   - Real-time comparison and swap/shift counters.
4. **Head-to-Head Comparison Lab**:
   - Live comparisons for searching (Linear vs Binary) and sorting (Bubble vs Insertion).
   - Inversion Equivalence Validator: Confirms that for any random array, Bubble Sort swaps $\equiv$ Insertion Sort right shifts $\equiv$ total inversions.
5. **Growth of Functions Lab**:
   - Interactive SVG curves for the 7 canonical growth rates ($1, \log_2 n, n, n \log_2 n, n^2, 2^n, n!$).
   - Adjustable $n$ range (4 to 32) and toggleable logarithmic Y-axis ($\log_{10}$).
   - Reference table showing values up to $n = 64$.
6. **Python 3.14.7 Microbenchmarks Viewer**:
   - Live tables displaying recorded median execution times and operation counts from the M3 experimental suite.

---

## 7. Production Deployment (Cloudflare Pages — Official Hosting Target)

The official public production release is hosted on **Cloudflare Pages** via native Git integration with the private GitHub repository `WebArpit07/algorithm-explorer`.

### Build & Deployment Configuration
- **Hosting Platform**: Cloudflare Pages
- **Repository**: `WebArpit07/algorithm-explorer` (Private)
- **Production Branch**: `main`
- **Framework Preset**: `None`
- **Root Directory**: *(empty / repository root)*
- **Build Command**: `exit 0`
- **Build Output Directory**: `dashboard`
- **Production URL**: `https://algorithm-explorer.pages.dev` (or assigned project slug)

Only the `dashboard/` directory is published as the document root; all Python source code, raw data, tests, and LaTeX monographs remain securely isolated inside the repository.

---

## 8. Alternative Deployment (GitHub Pages)

For institutions utilizing GitHub Pages directly:
1. Ensure the repository has GitHub Pages enabled under **Settings** $\rightarrow$ **Pages**.
2. Select **GitHub Actions** as the build source to use `.github/workflows/deploy.yml`.
3. The workflow automatically publishes `./dashboard` to `https://<username>.github.io/<repo-name>/`.
