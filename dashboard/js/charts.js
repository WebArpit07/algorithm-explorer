/**
 * Algorithm Explorer — Mathematical Charting Engine
 * Pure SVG charting for Growth of Functions hierarchy and Head-to-Head Comparisons.
 * Zero external CDN dependencies.
 */

"use strict";

const Charts = (() => {

    const FUNCTION_SPECS = {
        constant: {
            name: "Constant: 1",
            latex: "\\mathcal{O}(1)",
            color: "#64748b", // Slate
            fn: (n) => 1
        },
        logarithmic: {
            name: "Logarithmic: log₂(n)",
            latex: "\\mathcal{O}(\\log n)",
            color: "#0284c7", // Sky blue
            fn: (n) => (n <= 0 ? 0 : Math.log2(n))
        },
        linear: {
            name: "Linear: n",
            latex: "\\mathcal{O}(n)",
            color: "#16a34a", // Green
            fn: (n) => n
        },
        linearithmic: {
            name: "Linearithmic: n log₂(n)",
            latex: "\\mathcal{O}(n \\log n)",
            color: "#d97706", // Amber
            fn: (n) => (n <= 0 ? 0 : n * Math.log2(n))
        },
        quadratic: {
            name: "Quadratic: n²",
            latex: "\\mathcal{O}(n^2)",
            color: "#be185d", // Dark Pink
            fn: (n) => n * n
        },
        exponential: {
            name: "Exponential: 2ⁿ",
            latex: "\\mathcal{O}(2^n)",
            color: "#7c3aed", // Violet
            fn: (n) => (n > 60 ? Infinity : Math.pow(2, n))
        },
        factorial: {
            name: "Factorial: n!",
            latex: "\\mathcal{O}(n!)",
            color: "#dc2626", // Red
            fn: (n) => {
                if (n > 25) return Infinity;
                let res = 1;
                for (let i = 2; i <= Math.floor(n); i++) res *= i;
                return res;
            }
        }
    };

    /**
     * Interactive SVG Growth Functions Chart
     */
    class GrowthChart {
        constructor(svgContainerId, tooltipId) {
            this.container = document.getElementById(svgContainerId);
            this.tooltip = document.getElementById(tooltipId);
            this.maxN = 16;
            this.isLogScale = false;
            this.activeFunctions = {
                constant: true,
                logarithmic: true,
                linear: true,
                linearithmic: true,
                quadratic: true,
                exponential: true,
                factorial: true
            };
        }

        setMaxN(n) {
            this.maxN = Math.max(2, Math.min(64, n));
            this.render();
        }

        setLogScale(isLog) {
            this.isLogScale = isLog;
            this.render();
        }

        toggleFunction(key, active) {
            this.activeFunctions[key] = active;
            this.render();
        }

        render() {
            if (!this.container) return;

            const width = this.container.clientWidth || 800;
            const height = 420;
            const padding = { top: 30, right: 40, bottom: 50, left: 75 };
            const plotW = width - padding.left - padding.right;
            const plotH = height - padding.top - padding.bottom;

            // Generate sample points
            const steps = Math.min(100, Math.max(20, this.maxN * 4));
            const nValues = [];
            for (let i = 0; i <= steps; i++) {
                nValues.push(1 + (i / steps) * (this.maxN - 1));
            }

            // Determine Y bounds
            let maxY = 1;
            const dataSeries = {};

            Object.entries(FUNCTION_SPECS).forEach(([key, spec]) => {
                if (!this.activeFunctions[key]) return;
                const pts = nValues.map(n => {
                    let y = spec.fn(n);
                    if (!Number.isFinite(y) || isNaN(y)) y = 1e12;
                    return { n, y };
                });
                dataSeries[key] = pts;

                pts.forEach(p => {
                    const val = this.isLogScale ? Math.log10(Math.max(1, p.y)) : p.y;
                    if (val > maxY && val < (this.isLogScale ? 15 : 1e8)) {
                        maxY = val;
                    }
                });
            });

            // Prevent zero height
            if (maxY <= 1) maxY = 10;
            // Add top margin headroom
            maxY = this.isLogScale ? Math.ceil(maxY) : maxY * 1.08;

            const xScale = (n) => padding.left + ((n - 1) / (this.maxN - 1)) * plotW;
            const yScale = (y) => {
                const val = this.isLogScale ? Math.log10(Math.max(1, y)) : y;
                const clamped = Math.min(maxY, Math.max(0, val));
                return padding.top + plotH - (clamped / maxY) * plotH;
            };

            // Build SVG markup
            let svg = `<svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="growth-svg">`;

            // Background & Gridlines
            svg += `<rect width="${width}" height="${height}" fill="#ffffff" stroke="#e2e8f0" stroke-width="1" rx="8" />`;

            // X gridlines and ticks
            const xTicks = 8;
            for (let i = 0; i <= xTicks; i++) {
                const nVal = 1 + (i / xTicks) * (this.maxN - 1);
                const x = xScale(nVal);
                svg += `<line x1="${x}" y1="${padding.top}" x2="${x}" y2="${padding.top + plotH}" stroke="#f1f5f9" stroke-width="1" />`;
                svg += `<text x="${x}" y="${height - 18}" fill="#64748b" font-size="12" text-anchor="middle" font-family="'Inter', sans-serif">${nVal.toFixed(nVal >= 10 ? 0 : 1)}</text>`;
            }

            // Y gridlines and ticks
            const yTicks = 6;
            for (let i = 0; i <= yTicks; i++) {
                const frac = i / yTicks;
                const yPos = padding.top + plotH - frac * plotH;
                const yVal = frac * maxY;
                const label = this.isLogScale ? `10^${yVal.toFixed(1)}` : (yVal >= 1000 ? yVal.toExponential(1) : yVal.toFixed(0));

                svg += `<line x1="${padding.left}" y1="${yPos}" x2="${width - padding.right}" y2="${yPos}" stroke="#f1f5f9" stroke-width="1" />`;
                svg += `<text x="${padding.left - 10}" y="${yPos + 4}" fill="#64748b" font-size="11" text-anchor="end" font-family="'Inter', sans-serif">${label}</text>`;
            }

            // Axes
            svg += `<line x1="${padding.left}" y1="${padding.top}" x2="${padding.left}" y2="${padding.top + plotH}" stroke="#cbd5e1" stroke-width="2" />`;
            svg += `<line x1="${padding.left}" y1="${padding.top + plotH}" x2="${width - padding.right}" y2="${padding.top + plotH}" stroke="#cbd5e1" stroke-width="2" />`;

            // Axis titles
            svg += `<text x="${padding.left + plotW / 2}" y="${height - 2}" fill="#0f172a" font-size="12" font-weight="600" text-anchor="middle" font-family="'Inter', sans-serif">Input Size (n)</text>`;
            svg += `<text x="18" y="${padding.top + plotH / 2}" fill="#0f172a" font-size="12" font-weight="600" text-anchor="middle" font-family="'Inter', sans-serif" transform="rotate(-90, 18, ${padding.top + plotH / 2})">${this.isLogScale ? "Growth Scale log₁₀(f(n))" : "Operations f(n)"}</text>`;

            // Curves
            Object.entries(dataSeries).forEach(([key, pts]) => {
                const spec = FUNCTION_SPECS[key];
                let d = "";
                let started = false;

                pts.forEach(p => {
                    const x = xScale(p.n);
                    const y = yScale(p.y);
                    if (!started) {
                        d += `M ${x.toFixed(1)} ${y.toFixed(1)}`;
                        started = true;
                    } else {
                        d += ` L ${x.toFixed(1)} ${y.toFixed(1)}`;
                    }
                });

                svg += `<path d="${d}" fill="none" stroke="${spec.color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="growth-curve" data-fn="${key}" />`;
            });

            svg += `</svg>`;
            this.container.innerHTML = svg;
        }
    }

    /**
     * Render Comparative Performance Chart
     */
    function renderComparisonChart(containerId, data) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const maxOps = Math.max(...data.map(d => d.operations), 1);

        let html = `<div class="comparison-bars">`;
        data.forEach(item => {
            const widthPct = Math.max(4, (item.operations / maxOps) * 100);
            html += `
                <div class="comp-row">
                    <div class="comp-label">
                        <strong>${item.name}</strong>
                        <span class="comp-meta">${item.caseType || ""} · Complexity: <code>${item.complexity}</code></span>
                    </div>
                    <div class="comp-track">
                        <div class="comp-fill" style="width: ${widthPct}%; background-color: ${item.color || '#38bdf8'};"></div>
                        <span class="comp-value">${item.operations.toLocaleString()} ops</span>
                    </div>
                    ${item.note ? `<div class="comp-note">${item.note}</div>` : ""}
                </div>
            `;
        });
        html += `</div>`;
        container.innerHTML = html;
    }

    return {
        FUNCTION_SPECS,
        GrowthChart,
        renderComparisonChart
    };
})();

if (typeof module !== "undefined" && module.exports) {
    module.exports = Charts;
}
