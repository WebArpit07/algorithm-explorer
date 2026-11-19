/**
 * Algorithm Explorer — Main Application Orchestrator
 * Integrates labs, visualizers, mathematical charts, and experimental datasets.
 */

"use strict";

document.addEventListener("DOMContentLoaded", () => {

    // =========================================================================
    // 1. ALGORITHM EXPLORER KNOWLEDGE BASE
    // =========================================================================
    const ALGO_DETAILS = {
        linear_search: {
            title: "Linear Search",
            textbookRef: "Kenneth H. Rosen, §3.1, Algorithm 2",
            objective: "Locate the index of the first occurrence of target x in sequence a₁..aₙ, or return -1 if absent.",
            principle: "Examines array elements sequentially from index 0 to n-1 until a match is encountered or the sequence boundary is reached. Preserves original element order and requires no initial preconditions.",
            pseudocode: `procedure linear_search(x: integer, a1, a2, ..., an: integers)
    i := 1
    while (i ≤ n and x ≠ ai)
        i := i + 1
    if i ≤ n then location := i
    else location := 0
    return location`,
            bestCase: "Θ(1) key comparisons (Target located at index 0)",
            avgCase: "Θ(n) key comparisons (Under uniform distribution: (n + 1)/2)",
            worstCase: "Θ(n) key comparisons (Target at index n-1 or missing: exactly n)",
            space: "Θ(1) auxiliary space (In-place iterative pointer)",
            precondition: "None. Works on arbitrary, unsorted, duplicate, and negative sequences."
        },
        binary_search: {
            title: "Binary Search",
            textbookRef: "Kenneth H. Rosen, §3.1, Algorithm 3",
            objective: "Locate target x in a pre-sorted sequence a₁ ≤ a₂ ≤ ... ≤ aₙ in logarithmic time.",
            principle: "Repeatedly computes the midpoint of the active subrange [low, high]. Compares the target against the midpoint element, halving the remaining search space on each iteration by discarding the impossible half.",
            pseudocode: `procedure binary_search(x: integer, a1, a2, ..., an: increasing integers)
    i := 1      {low boundary}
    j := n      {high boundary}
    while i < j
        m := ⌊(i + j) / 2⌋
        if x > am then i := m + 1
        else j := m
    if x = ai then location := i
    else location := 0
    return location`,
            bestCase: "Θ(1) key comparisons (Target located at initial midpoint)",
            avgCase: "Θ(log n) key comparisons (≈ 2 log₂ n comparisons)",
            worstCase: "Θ(log n) key comparisons (At most 2(⌊log₂ n⌋ + 1) comparisons)",
            space: "Θ(1) auxiliary space (Iterative boundary pointers)",
            precondition: "MANDATORY: Array must be sorted in non-decreasing order prior to execution."
        },
        bubble_sort: {
            title: "Bubble Sort (Textbook Fixed-Pass)",
            textbookRef: "Kenneth H. Rosen, §3.1, Algorithm 4",
            objective: "Sort sequence a₁..aₙ into ascending order through repeated adjacent exchanges.",
            principle: "Performs exactly n - 1 successive passes. Each pass sweeps through adjacent pairs, swapping them if out of order, which 'bubbles' the maximum remaining element to its final sorted position. Rosen's canonical formulation does NOT include an early-exit flag.",
            pseudocode: `procedure bubblesort(a1, ..., an: real numbers with n ≥ 2)
    for i := 1 to n - 1
        for j := 1 to n - i
            if aj > aj+1 then
                interchange aj and aj+1`,
            bestCase: "Comparisons: Θ(n²) (Exactly n(n-1)/2); Swaps: 0 (Already sorted)",
            avgCase: "Comparisons: Θ(n²); Swaps: n(n-1)/4 = Θ(n²) (Random permutations)",
            worstCase: "Comparisons: Θ(n²); Swaps: n(n-1)/2 = Θ(n²) (Distinct reverse-sorted)",
            space: "Θ(1) auxiliary space (In-place sort, stable)",
            precondition: "None. Comparisons are strictly invariant across all input arrangements."
        },
        insertion_sort: {
            title: "Insertion Sort",
            textbookRef: "Kenneth H. Rosen, §3.1, Algorithm 5",
            objective: "Sort sequence a₁..aₙ into ascending order by iteratively inserting elements into an expanding sorted prefix.",
            principle: "Considers the initial prefix [0..0] trivially sorted. For each subsequent element (key), it scans backward through the sorted prefix, shifting greater elements one position to the right, and drops the key into its correct relative position.",
            pseudocode: `procedure insertionsort(a1, a2, ..., an: real numbers with n ≥ 2)
    for j := 2 to n
        i := 1
        while aj > ai
            i := i + 1
        m := aj
        for k := 0 to j - i - 1
            aj-k := aj-k-1
        ai := m`,
            bestCase: "Comparisons: n - 1 = Θ(n); Shifts: 0 (Pre-sorted input, adaptive)",
            avgCase: "Comparisons: ≈ n²/4 = Θ(n²); Shifts: ≈ n²/4 = Θ(n²)",
            worstCase: "Comparisons: n(n-1)/2 = Θ(n²); Shifts: n(n-1)/2 = Θ(n²) (Reverse-sorted)",
            space: "Θ(1) auxiliary space (In-place sort, stable)",
            precondition: "None. Inversions strictly equal right shifts and Bubble Sort swaps."
        }
    };

    // =========================================================================
    // 2. EXPLORER SECTION TAB SWITCHING
    // =========================================================================
    const algoTabs = document.querySelectorAll(".algo-tab-btn");
    const algoDetailsContainer = document.getElementById("algo-details-display");

    function renderAlgoDetails(key) {
        const d = ALGO_DETAILS[key];
        if (!d || !algoDetailsContainer) return;

        algoDetailsContainer.innerHTML = `
            <div class="algo-detail-card">
                <div class="detail-header">
                    <h3>${d.title}</h3>
                    <span class="textbook-cite">${d.textbookRef}</span>
                </div>
                <p class="algo-objective"><strong>Objective:</strong> ${d.objective}</p>
                <p class="algo-principle"><strong>Working Principle:</strong> ${d.principle}</p>
                
                <div class="detail-grid">
                    <div class="detail-col">
                        <h4>Complexity Bounds & Invariants</h4>
                        <ul class="complexity-list">
                            <li><span class="label">Best Case:</span> <code>${d.bestCase}</code></li>
                            <li><span class="label">Average Case:</span> <code>${d.avgCase}</code></li>
                            <li><span class="label">Worst Case:</span> <code>${d.worstCase}</code></li>
                            <li><span class="label">Auxiliary Space:</span> <code>${d.space}</code></li>
                        </ul>
                        <div class="precondition-box">
                            <strong>Input Preconditions:</strong> ${d.precondition}
                        </div>
                    </div>
                    <div class="detail-col">
                        <h4>Textbook Pseudocode</h4>
                        <pre class="pseudocode-block"><code>${d.pseudocode}</code></pre>
                    </div>
                </div>
            </div>
        `;
    }

    algoTabs.forEach(btn => {
        btn.addEventListener("click", () => {
            algoTabs.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderAlgoDetails(btn.dataset.algo);
        });
    });

    renderAlgoDetails("linear_search");

    // =========================================================================
    // 3. SEARCHING LAB CONTROLLER
    // =========================================================================
    const searchVisualizer = new Visualizations.SearchVisualizer("search-array-container", "search-status-text");
    let currentSearchAlgo = "linear_search";
    let searchArray = [12, 28, 35, 42, 55, 68, 74, 89, 93];
    let searchSteps = [];
    let searchStepIdx = 0;
    let searchTimer = null;
    let searchSpeedMs = 500;

    const searchAlgoSelect = document.getElementById("search-algo-select");
    const searchTargetInput = document.getElementById("search-target-input");
    const searchCustomInput = document.getElementById("search-custom-input");
    const searchPreconditionAlert = document.getElementById("search-precondition-alert");
    const searchSortBtn = document.getElementById("search-sort-btn");

    const searchPlayBtn = document.getElementById("search-play-btn");
    const searchPauseBtn = document.getElementById("search-pause-btn");
    const searchStepBtn = document.getElementById("search-step-btn");
    const searchResetBtn = document.getElementById("search-reset-btn");
    const searchSpeedSlider = document.getElementById("search-speed-slider");

    // Metric display elements
    const searchMetricComparisons = document.getElementById("search-metric-comparisons");
    const searchMetricIterations = document.getElementById("search-metric-iterations");
    const searchMetricStatus = document.getElementById("search-metric-status");
    const searchMetricResult = document.getElementById("search-metric-result");

    function parseCustomArray(str) {
        if (!str || !str.trim()) return null;
        const parts = str.split(/[,\s]+/).map(s => s.trim()).filter(Boolean);
        const nums = parts.map(Number);
        if (nums.some(isNaN)) return null;
        return nums;
    }

    function checkSearchPreconditions() {
        if (currentSearchAlgo === "binary_search") {
            const sorted = Algorithms.isSorted(searchArray);
            if (!sorted) {
                if (searchPreconditionAlert) searchPreconditionAlert.classList.remove("hidden");
                return false;
            }
        }
        if (searchPreconditionAlert) searchPreconditionAlert.classList.add("hidden");
        return true;
    }

    function initSearchLab() {
        pauseSearch();
        const custom = parseCustomArray(searchCustomInput ? searchCustomInput.value : "");
        if (custom && custom.length > 0) {
            searchArray = custom.slice(0, 30); // Cap at 30 for visualization
        }

        const target = Number(searchTargetInput ? searchTargetInput.value : 42);
        checkSearchPreconditions();

        try {
            if (currentSearchAlgo === "linear_search") {
                searchSteps = Algorithms.linearSearchSteps(searchArray, target);
            } else {
                if (!Algorithms.isSorted(searchArray)) {
                    searchSteps = [{
                        type: "error",
                        array: [...searchArray],
                        comparisons: 0,
                        iterations: 0,
                        description: "Precondition Error: Binary Search requires a sorted sequence. Click 'Sort Array' below."
                    }];
                } else {
                    searchSteps = Algorithms.binarySearchSteps(searchArray, target);
                }
            }
        } catch (e) {
            console.error(e);
            return;
        }

        searchStepIdx = 0;
        updateSearchUI();
    }

    function updateSearchUI() {
        if (!searchSteps || searchSteps.length === 0) return;
        const state = searchSteps[searchStepIdx];
        searchVisualizer.render(state, currentSearchAlgo);

        if (searchMetricComparisons) searchMetricComparisons.textContent = state.comparisons ?? state.totalComparisons ?? 0;
        if (searchMetricIterations) searchMetricIterations.textContent = state.iterations ?? 0;
        if (searchMetricStatus) {
            searchMetricStatus.textContent = state.found ? "Target Found" : (state.type === "not_found" ? "Not Found" : "Searching...");
            searchMetricStatus.className = `metric-value ${state.found ? "status-success" : (state.type === "not_found" ? "status-danger" : "")}`;
        }
        if (searchMetricResult) searchMetricResult.textContent = state.resultIndex !== undefined && state.resultIndex >= 0 ? `Index ${state.resultIndex}` : (state.found ? "Found" : "None");
    }

    function stepSearch() {
        if (searchStepIdx < searchSteps.length - 1) {
            searchStepIdx++;
            updateSearchUI();
        } else {
            pauseSearch();
        }
    }

    function playSearch() {
        if (searchTimer) return;
        if (searchStepIdx >= searchSteps.length - 1) searchStepIdx = 0;
        if (searchPlayBtn) searchPlayBtn.disabled = true;
        if (searchPauseBtn) searchPauseBtn.disabled = false;

        searchTimer = setInterval(() => {
            if (searchStepIdx < searchSteps.length - 1) {
                stepSearch();
            } else {
                pauseSearch();
            }
        }, searchSpeedMs);
    }

    function pauseSearch() {
        if (searchTimer) {
            clearInterval(searchTimer);
            searchTimer = null;
        }
        if (searchPlayBtn) searchPlayBtn.disabled = false;
        if (searchPauseBtn) searchPauseBtn.disabled = true;
    }

    if (searchAlgoSelect) {
        searchAlgoSelect.addEventListener("change", (e) => {
            currentSearchAlgo = e.target.value;
            initSearchLab();
        });
    }

    if (searchTargetInput) searchTargetInput.addEventListener("input", initSearchLab);
    if (searchCustomInput) searchCustomInput.addEventListener("input", initSearchLab);
    if (searchSortBtn) {
        searchSortBtn.addEventListener("click", () => {
            searchArray.sort((a, b) => a - b);
            if (searchCustomInput) searchCustomInput.value = searchArray.join(", ");
            initSearchLab();
        });
    }

    document.getElementById("search-gen-rand-btn")?.addEventListener("click", () => {
        searchArray = Array.from({ length: 12 }, () => Math.floor(Math.random() * 90) + 10);
        if (currentSearchAlgo === "binary_search") searchArray.sort((a, b) => a - b);
        if (searchCustomInput) searchCustomInput.value = searchArray.join(", ");
        if (searchTargetInput) searchTargetInput.value = searchArray[Math.floor(Math.random() * searchArray.length)];
        initSearchLab();
    });

    if (searchPlayBtn) searchPlayBtn.addEventListener("click", playSearch);
    if (searchPauseBtn) searchPauseBtn.addEventListener("click", pauseSearch);
    if (searchStepBtn) searchStepBtn.addEventListener("click", () => { pauseSearch(); stepSearch(); });
    if (searchResetBtn) searchResetBtn.addEventListener("click", () => { pauseSearch(); searchStepIdx = 0; updateSearchUI(); });
    if (searchSpeedSlider) {
        searchSpeedSlider.addEventListener("input", (e) => {
            searchSpeedMs = 1050 - Number(e.target.value);
            if (searchTimer) {
                pauseSearch();
                playSearch();
            }
        });
    }

    initSearchLab();

    // =========================================================================
    // 4. SORTING LAB CONTROLLER
    // =========================================================================
    const sortVisualizer = new Visualizations.SortVisualizer("sorting-canvas-container", "sort-status-text");
    let currentSortAlgo = "bubble_sort";
    let sortArray = [45, 18, 62, 29, 73, 11, 88, 34, 52, 23];
    let sortSteps = [];
    let sortStepIdx = 0;
    let sortTimer = null;
    let sortSpeedMs = 300;

    const sortAlgoSelect = document.getElementById("sort-algo-select");
    const sortCustomInput = document.getElementById("sort-custom-input");
    const sortPlayBtn = document.getElementById("sort-play-btn");
    const sortPauseBtn = document.getElementById("sort-pause-btn");
    const sortStepBtn = document.getElementById("sort-step-btn");
    const sortResetBtn = document.getElementById("sort-reset-btn");
    const sortSpeedSlider = document.getElementById("sort-speed-slider");

    // Metric display elements
    const sortMetricComparisons = document.getElementById("sort-metric-comparisons");
    const sortMetricSwapsShifts = document.getElementById("sort-metric-swaps-shifts");
    const sortMetricSwapsShiftsLabel = document.getElementById("sort-metric-swaps-label");
    const sortMetricPass = document.getElementById("sort-metric-pass");
    const sortMetricStatus = document.getElementById("sort-metric-status");

    function initSortLab() {
        pauseSort();
        const custom = parseCustomArray(sortCustomInput ? sortCustomInput.value : "");
        if (custom && custom.length > 0) {
            sortArray = custom.slice(0, 30); // Cap at 30 bars
        }

        if (currentSortAlgo === "bubble_sort") {
            sortSteps = Algorithms.bubbleSortSteps(sortArray);
            if (sortMetricSwapsShiftsLabel) sortMetricSwapsShiftsLabel.textContent = "Swaps";
        } else {
            sortSteps = Algorithms.insertionSortSteps(sortArray);
            if (sortMetricSwapsShiftsLabel) sortMetricSwapsShiftsLabel.textContent = "Right Shifts";
        }

        sortStepIdx = 0;
        updateSortUI();
    }

    function updateSortUI() {
        if (!sortSteps || sortSteps.length === 0) return;
        const state = sortSteps[sortStepIdx];
        sortVisualizer.render(state, currentSortAlgo);

        if (sortMetricComparisons) sortMetricComparisons.textContent = state.comparisons ?? 0;
        if (sortMetricSwapsShifts) {
            sortMetricSwapsShifts.textContent = currentSortAlgo === "bubble_sort" ? (state.swaps ?? 0) : (state.rightShifts ?? 0);
        }
        if (sortMetricPass) sortMetricPass.textContent = state.pass ?? 0;
        if (sortMetricStatus) {
            const isFin = state.type === "finished";
            sortMetricStatus.textContent = isFin ? "Sorted" : "Sorting...";
            sortMetricStatus.className = `metric-value ${isFin ? "status-success" : ""}`;
        }
    }

    function stepSort() {
        if (sortStepIdx < sortSteps.length - 1) {
            sortStepIdx++;
            updateSortUI();
        } else {
            pauseSort();
        }
    }

    function playSort() {
        if (sortTimer) return;
        if (sortStepIdx >= sortSteps.length - 1) sortStepIdx = 0;
        if (sortPlayBtn) sortPlayBtn.disabled = true;
        if (sortPauseBtn) sortPauseBtn.disabled = false;

        sortTimer = setInterval(() => {
            if (sortStepIdx < sortSteps.length - 1) {
                stepSort();
            } else {
                pauseSort();
            }
        }, sortSpeedMs);
    }

    function pauseSort() {
        if (sortTimer) {
            clearInterval(sortTimer);
            sortTimer = null;
        }
        if (sortPlayBtn) sortPlayBtn.disabled = false;
        if (sortPauseBtn) sortPauseBtn.disabled = true;
    }

    if (sortAlgoSelect) {
        sortAlgoSelect.addEventListener("change", (e) => {
            currentSortAlgo = e.target.value;
            initSortLab();
        });
    }

    if (sortCustomInput) sortCustomInput.addEventListener("input", initSortLab);

    document.getElementById("sort-gen-rand-btn")?.addEventListener("click", () => {
        sortArray = Array.from({ length: 12 }, () => Math.floor(Math.random() * 80) + 15);
        if (sortCustomInput) sortCustomInput.value = sortArray.join(", ");
        initSortLab();
    });

    document.getElementById("sort-gen-sorted-btn")?.addEventListener("click", () => {
        sortArray = Array.from({ length: 12 }, (_, i) => (i + 1) * 7);
        if (sortCustomInput) sortCustomInput.value = sortArray.join(", ");
        initSortLab();
    });

    document.getElementById("sort-gen-rev-btn")?.addEventListener("click", () => {
        sortArray = Array.from({ length: 12 }, (_, i) => (12 - i) * 7);
        if (sortCustomInput) sortCustomInput.value = sortArray.join(", ");
        initSortLab();
    });

    if (sortPlayBtn) sortPlayBtn.addEventListener("click", playSort);
    if (sortPauseBtn) sortPauseBtn.addEventListener("click", pauseSort);
    if (sortStepBtn) sortStepBtn.addEventListener("click", () => { pauseSort(); stepSort(); });
    if (sortResetBtn) sortResetBtn.addEventListener("click", () => { pauseSort(); sortStepIdx = 0; updateSortUI(); });
    if (sortSpeedSlider) {
        sortSpeedSlider.addEventListener("input", (e) => {
            sortSpeedMs = 650 - Number(e.target.value);
            if (sortTimer) {
                pauseSort();
                playSort();
            }
        });
    }

    initSortLab();

    // =========================================================================
    // 5. COMPARISON LAB RUNNER (SEARCHING & SORTING)
    // =========================================================================
    const compSearchRunBtn = document.getElementById("comp-search-run-btn");
    const compSearchSize = document.getElementById("comp-search-size");
    const compSearchScenario = document.getElementById("comp-search-scenario");

    function runSearchComparison() {
        const n = Number(compSearchSize ? compSearchSize.value : 1000);
        const scenario = compSearchScenario ? compSearchScenario.value : "missing";

        // Generate synthetic sequence
        const arr = Array.from({ length: n }, (_, i) => i * 2);
        let target;
        if (scenario === "first") target = arr[0];
        else if (scenario === "middle") target = arr[Math.floor(n / 2)];
        else if (scenario === "last") target = arr[n - 1];
        else target = -999; // Missing

        // Run Linear Search
        const t0Linear = performance.now();
        const linSteps = Algorithms.linearSearchSteps(arr, target);
        const t1Linear = performance.now();
        const linFinal = linSteps[linSteps.length - 1];

        // Run Binary Search
        const t0Binary = performance.now();
        const binSteps = Algorithms.binarySearchSteps(arr, target);
        const t1Binary = performance.now();
        const binFinal = binSteps[binSteps.length - 1];

        const chartData = [
            {
                name: "Linear Search",
                caseType: scenario.toUpperCase(),
                complexity: "Θ(n)",
                operations: linFinal.comparisons,
                color: "#38bdf8",
                note: `Browser runtime: ${(t1Linear - t0Linear).toFixed(3)} ms (Client illustrative only)`
            },
            {
                name: "Binary Search",
                caseType: scenario.toUpperCase(),
                complexity: "Θ(log n)",
                operations: binFinal.totalComparisons,
                color: "#34d399",
                note: `Browser runtime: ${(t1Binary - t0Binary).toFixed(3)} ms (Speedup: ${(linFinal.comparisons / Math.max(1, binFinal.totalComparisons)).toFixed(1)}x)`
            }
        ];

        Charts.renderComparisonChart("comp-search-chart", chartData);
    }

    if (compSearchRunBtn) compSearchRunBtn.addEventListener("click", runSearchComparison);
    runSearchComparison();

    const compSortRunBtn = document.getElementById("comp-sort-run-btn");
    const compSortSize = document.getElementById("comp-sort-size");
    const compSortArrangement = document.getElementById("comp-sort-arrangement");

    function runSortComparison() {
        const n = Number(compSortSize ? compSortSize.value : 200);
        const arrangement = compSortArrangement ? compSortArrangement.value : "random";

        let arr = [];
        if (arrangement === "sorted") {
            arr = Array.from({ length: n }, (_, i) => i + 1);
        } else if (arrangement === "reverse") {
            arr = Array.from({ length: n }, (_, i) => n - i);
        } else {
            arr = Array.from({ length: n }, (_, i) => i + 1);
            // Fisher-Yates shuffle
            for (let i = n - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
        }

        const inversions = Algorithms.countInversions(arr);

        // Run Bubble Sort
        const bSteps = Algorithms.bubbleSortSteps(arr);
        const bFinal = bSteps[bSteps.length - 1];

        // Run Insertion Sort
        const insSteps = Algorithms.insertionSortSteps(arr);
        const insFinal = insSteps[insSteps.length - 1];

        const chartData = [
            {
                name: "Bubble Sort (Rosen Fixed-Pass)",
                caseType: arrangement.toUpperCase(),
                complexity: "Θ(n²)",
                operations: bFinal.comparisons,
                color: "#f87171",
                note: `Comparisons: ${bFinal.comparisons.toLocaleString()} (Strictly invariant n(n-1)/2) | Swaps: ${bFinal.swaps.toLocaleString()}`
            },
            {
                name: "Insertion Sort",
                caseType: arrangement.toUpperCase(),
                complexity: arrangement === "sorted" ? "Θ(n)" : "Θ(n²)",
                operations: insFinal.comparisons,
                color: "#34d399",
                note: `Comparisons: ${insFinal.comparisons.toLocaleString()} | Right Shifts: ${insFinal.rightShifts.toLocaleString()}`
            }
        ];

        Charts.renderComparisonChart("comp-sort-chart", chartData);

        // Update Inversion Equivalence proof card
        const invCard = document.getElementById("comp-inversion-proof");
        if (invCard) {
            const isEqual = bFinal.swaps === insFinal.rightShifts && bFinal.swaps === inversions;
            invCard.innerHTML = `
                <div class="inversion-banner ${isEqual ? 'verified' : ''}">
                    <h4>Inversion Equivalence Verification</h4>
                    <p>Total permutation inversions: <strong>${inversions.toLocaleString()}</strong></p>
                    <p>Bubble Sort adjacent swaps: <strong>${bFinal.swaps.toLocaleString()}</strong></p>
                    <p>Insertion Sort right shifts: <strong>${insFinal.rightShifts.toLocaleString()}</strong></p>
                    <div class="inv-result">
                        ${isEqual ? '✓ Mathematical Identity Verified: Swaps ≡ Shifts ≡ Inversions' : 'Discrepancy detected'}
                    </div>
                </div>
            `;
        }
    }

    if (compSortRunBtn) compSortRunBtn.addEventListener("click", runSortComparison);
    runSortComparison();

    // =========================================================================
    // 6. GROWTH OF FUNCTIONS LAB
    // =========================================================================
    const growthChart = new Charts.GrowthChart("growth-chart-svg", "growth-tooltip");
    const growthRangeN = document.getElementById("growth-range-n");
    const growthValN = document.getElementById("growth-val-n");
    const growthScaleToggle = document.getElementById("growth-scale-toggle");

    if (growthRangeN) {
        growthRangeN.addEventListener("input", (e) => {
            const val = Number(e.target.value);
            if (growthValN) growthValN.textContent = val;
            growthChart.setMaxN(val);
        });
    }

    if (growthScaleToggle) {
        growthScaleToggle.addEventListener("change", (e) => {
            growthChart.setLogScale(e.target.checked);
        });
    }

    document.querySelectorAll(".fn-toggle-checkbox").forEach(cb => {
        cb.addEventListener("change", (e) => {
            growthChart.toggleFunction(e.target.dataset.fn, e.target.checked);
        });
    });

    growthChart.render();

    // =========================================================================
    // 7. EXPERIMENTAL PYTHON BENCHMARK DATA VIEWER (M3 DATA INTEGRATION)
    // =========================================================================
    const benchmarkData = window.BENCHMARK_DATA || null;

    function renderBenchmarkSection(data) {
        if (!data) return;

        // Metadata display
        const metaContainer = document.getElementById("benchmark-metadata-container");
        if (metaContainer && data.metadata) {
            const m = data.metadata;
            metaContainer.innerHTML = `
                <div class="meta-grid">
                    <div class="meta-item"><span class="lbl">Python Runtime:</span> <strong>${m.python_version} (${m.python_implementation})</strong></div>
                    <div class="meta-item"><span class="lbl">Platform:</span> <strong>${m.operating_system} ${m.os_release} (${m.machine_architecture})</strong></div>
                    <div class="meta-item"><span class="lbl">Processor:</span> <strong>${m.processor} (${m.cpu_count_logical} vCPUs)</strong></div>
                    <div class="meta-item"><span class="lbl">Timer Resolution:</span> <strong>${m.timing_resolution_ns} ns (${m.timing_timer})</strong></div>
                    <div class="meta-item"><span class="lbl">Replications:</span> <strong>${m.repetitions_per_case} iterations / condition</strong></div>
                    <div class="meta-item"><span class="lbl">Benchmark Date:</span> <strong>${m.benchmark_date_utc}</strong></div>
                </div>
            `;
        }

        // Highlight summary cards
        if (data.highlighted_comparisons) {
            const s100k = data.highlighted_comparisons.search_at_100k;
            const linTime = document.getElementById("bm-search-linear-time");
            const binTime = document.getElementById("bm-search-binary-time");
            const speedup = document.getElementById("bm-search-speedup");
            if (linTime) linTime.textContent = `${s100k.linear.median_time_ms} ms (${s100k.linear.comparisons.toLocaleString()} ops)`;
            if (binTime) binTime.textContent = `${(s100k.binary.median_time_ms * 1000).toFixed(2)} µs (${s100k.binary.comparisons} ops)`;
            if (speedup) speedup.textContent = `${s100k.speedup_factor.toLocaleString()}×`;

            const sort3k = data.highlighted_comparisons.sorting_at_3k;
            const invEq = document.getElementById("bm-sorting-inversion-eq");
            const adaptSpeed = document.getElementById("bm-sorting-adapt-speedup");
            if (invEq) invEq.textContent = `${sort3k.inversion_equivalence.bubble_swaps_random.toLocaleString()} operations (Identical)`;
            if (adaptSpeed) adaptSpeed.textContent = `${sort3k.sorted_adaptation.speedup_factor}× faster on sorted array`;
        }

        // Render Search Summary Table
        const searchTableBody = document.querySelector("#bm-search-table tbody");
        if (searchTableBody && data.search_summary) {
            searchTableBody.innerHTML = "";
            // Show sample representative rows (100, 1000, 10000, 100000 on worst/missing)
            const filtered = data.search_summary.filter(r => r.scenario === "missing");
            filtered.forEach(r => {
                const tr = document.createElement("tr");
                const medianMs = (r.median_duration_ns / 1e6).toFixed(4);
                tr.innerHTML = `
                    <td><code>${r.algorithm}</code></td>
                    <td>${r.input_size.toLocaleString()}</td>
                    <td><span class="badge badge-scenario">${r.scenario}</span></td>
                    <td><strong>${r.key_comparisons.toLocaleString()}</strong></td>
                    <td>${r.loop_evaluations ? r.loop_evaluations.toLocaleString() : "-"}</td>
                    <td><code>${medianMs} ms</code></td>
                `;
                searchTableBody.appendChild(tr);
            });
        }

        // Render Sorting Summary Table
        const sortTableBody = document.querySelector("#bm-sort-table tbody");
        if (sortTableBody && data.sorting_summary) {
            sortTableBody.innerHTML = "";
            const filtered = data.sorting_summary.filter(r => r.input_size === 1000 || r.input_size === 3000);
            filtered.forEach(r => {
                const tr = document.createElement("tr");
                const medianMs = (r.median_duration_ns / 1e6).toFixed(2);
                tr.innerHTML = `
                    <td><code>${r.algorithm}</code></td>
                    <td>${r.input_size.toLocaleString()}</td>
                    <td><span class="badge badge-topology">${r.arrangement}</span></td>
                    <td><strong>${r.element_comparisons.toLocaleString()}</strong></td>
                    <td>${r.swaps ? r.swaps.toLocaleString() : "-"}</td>
                    <td>${r.right_shifts ? r.right_shifts.toLocaleString() : "-"}</td>
                    <td><code>${medianMs} ms</code></td>
                `;
                sortTableBody.appendChild(tr);
            });
        }
    }

    if (benchmarkData) {
        renderBenchmarkSection(benchmarkData);
    } else {
        // Fallback fetch
        fetch("data/benchmark_data.json")
            .then(res => res.json())
            .then(data => renderBenchmarkSection(data))
            .catch(err => console.warn("Could not load benchmark_data.json via fetch:", err));
    }

    // =========================================================================
    // 8. MOBILE NAVIGATION MENU TOGGLE
    // =========================================================================
    const navToggle = document.getElementById("nav-toggle");
    const navLinks = document.getElementById("nav-links");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
        navLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => navLinks.classList.remove("open"));
        });
    }
});
