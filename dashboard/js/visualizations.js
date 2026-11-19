/**
 * Algorithm Explorer — Visual Rendering Engines
 * Manages animated DOM array layouts for searching and SVG bar charts for sorting.
 */

"use strict";

const Visualizations = (() => {

    /**
     * Searching Lab Array Visualizer
     */
    class SearchVisualizer {
        constructor(containerId, statusTextId) {
            this.container = document.getElementById(containerId);
            this.statusText = document.getElementById(statusTextId);
        }

        render(state, algorithm) {
            if (!this.container) return;
            this.container.innerHTML = "";

            const arr = state.array;
            const n = arr.length;

            const grid = document.createElement("div");
            grid.className = "search-grid";

            for (let i = 0; i < n; i++) {
                const cell = document.createElement("div");
                cell.className = "search-cell";
                cell.id = `search-cell-${i}`;

                // Determine cell state
                let stateClass = "default";
                const badges = [];

                if (algorithm === "linear_search") {
                    if (state.currentIndex === i) {
                        stateClass = state.found ? "match" : "comparing";
                        badges.push("i");
                    } else if (state.examinedIndices && state.examinedIndices.includes(i)) {
                        stateClass = "examined";
                    }
                } else if (algorithm === "binary_search") {
                    const isDiscarded = state.discardedRanges && state.discardedRanges.some(r => i >= r.start && i <= r.end);
                    if (isDiscarded && i !== state.mid) {
                        stateClass = "discarded";
                    } else if (i === state.mid) {
                        stateClass = state.found ? "match" : "midpoint";
                    } else if (i >= state.low && i <= state.high) {
                        stateClass = "active-range";
                    } else {
                        stateClass = "discarded";
                    }

                    if (i === state.low) badges.push("low");
                    if (i === state.mid) badges.push("mid");
                    if (i === state.high) badges.push("high");
                }

                cell.classList.add(stateClass);

                // HTML structure for cell
                cell.innerHTML = `
                    <div class="cell-index">${i}</div>
                    <div class="cell-value">${arr[i]}</div>
                    <div class="cell-pointers">${badges.map(b => `<span class="badge badge-${b}">${b}</span>`).join("")}</div>
                `;

                grid.appendChild(cell);
            }

            this.container.appendChild(grid);

            if (this.statusText && state.description) {
                this.statusText.textContent = state.description;
            }
        }
    }

    /**
     * Sorting Lab Vertical Bar Chart Visualizer
     */
    class SortVisualizer {
        constructor(containerId, statusTextId) {
            this.container = document.getElementById(containerId);
            this.statusText = document.getElementById(statusTextId);
        }

        render(state, algorithm) {
            if (!this.container) return;
            this.container.innerHTML = "";

            const arr = state.array;
            const n = arr.length;
            if (n === 0) return;

            const maxVal = Math.max(...arr.map(v => Math.abs(v)), 1);
            const chart = document.createElement("div");
            chart.className = "sort-chart";

            for (let i = 0; i < n; i++) {
                const barWrapper = document.createElement("div");
                barWrapper.className = "bar-wrapper";

                const val = arr[i];
                const heightPercent = Math.max(8, (Math.abs(val) / maxVal) * 92);

                let stateClass = "default";
                let pointerLabel = "";

                if (algorithm === "bubble_sort") {
                    if (state.swappingIndices && state.swappingIndices.includes(i)) {
                        stateClass = "swapping";
                    } else if (state.comparingIndices && state.comparingIndices.includes(i)) {
                        stateClass = "comparing";
                    } else if (i >= state.sortedStartIndex) {
                        stateClass = "sorted";
                    }
                } else if (algorithm === "insertion_sort") {
                    if (state.shiftingIndices && state.shiftingIndices.includes(i)) {
                        stateClass = "shifting";
                    } else if (i === state.keyIndex && state.keyValue !== null) {
                        stateClass = "key-element";
                        pointerLabel = "key";
                    } else if (i === state.comparingIndex) {
                        stateClass = "comparing";
                    } else if (i < state.sortedPrefixLength) {
                        stateClass = "sorted-prefix";
                    }
                }

                barWrapper.innerHTML = `
                    <div class="bar-value">${val}</div>
                    <div class="bar-pillar ${stateClass}" style="height: ${heightPercent}%;"></div>
                    <div class="bar-index">${i}</div>
                    ${pointerLabel ? `<div class="bar-tag">${pointerLabel}</div>` : ""}
                `;

                chart.appendChild(barWrapper);
            }

            this.container.appendChild(chart);

            if (this.statusText && state.description) {
                this.statusText.textContent = state.description;
            }
        }
    }

    return {
        SearchVisualizer,
        SortVisualizer
    };
})();

if (typeof module !== "undefined" && module.exports) {
    module.exports = Visualizations;
}
