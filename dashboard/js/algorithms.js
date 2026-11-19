/**
 * Algorithm Explorer — Core Algorithmic Step Generators
 * Grounded in Kenneth H. Rosen, Discrete Mathematics and Its Applications (8th Edition), Chapter 3.
 *
 * Implements authoritative step generators for:
 * 1. Linear Search (Rosen §3.1, Alg. 2)
 * 2. Binary Search (Rosen §3.1, Alg. 3)
 * 3. Bubble Sort (Rosen §3.1, Alg. 4 - strictly fixed-pass, no early termination)
 * 4. Insertion Sort (Rosen §3.1, Alg. 5 - separate comparisons vs right shifts)
 */

"use strict";

const Algorithms = (() => {

    /**
     * Generate step-by-step trace for Linear Search.
     * @param {Array<number>} arr - Input array
     * @param {number} target - Target search value
     * @returns {Array<Object>} Sequence of visualization states
     */
    function linearSearchSteps(arr, target) {
        const steps = [];
        const n = arr.length;
        let comparisons = 0;
        let found = false;
        let resultIndex = -1;

        // Initial state
        steps.push({
            type: "init",
            array: [...arr],
            currentIndex: -1,
            examinedIndices: [],
            comparisons: 0,
            iterations: 0,
            found: false,
            resultIndex: -1,
            description: `Starting Linear Search for target = ${target} across n = ${n} elements.`
        });

        const examined = [];

        for (let i = 0; i < n; i++) {
            comparisons++;
            examined.push(i);

            // Step: Comparing
            steps.push({
                type: "compare",
                array: [...arr],
                currentIndex: i,
                examinedIndices: [...examined],
                comparisons: comparisons,
                iterations: i + 1,
                found: false,
                resultIndex: -1,
                description: `Iteration ${i + 1}: Comparing arr[${i}] = ${arr[i]} with target = ${target}. (Comparison #${comparisons})`
            });

            if (arr[i] === target) {
                found = true;
                resultIndex = i;

                // Step: Match found
                steps.push({
                    type: "match",
                    array: [...arr],
                    currentIndex: i,
                    examinedIndices: [...examined],
                    comparisons: comparisons,
                    iterations: i + 1,
                    found: true,
                    resultIndex: i,
                    description: `Target ${target} found at index ${i}! Terminating search in ${comparisons} comparison(s).`
                });
                break;
            }
        }

        if (!found) {
            steps.push({
                type: "not_found",
                array: [...arr],
                currentIndex: -1,
                examinedIndices: [...examined],
                comparisons: comparisons,
                iterations: n,
                found: false,
                resultIndex: -1,
                description: `Target ${target} not found after traversing all n = ${n} elements. Total comparisons = ${comparisons}.`
            });
        }

        return steps;
    }

    /**
     * Check if an array is sorted in non-decreasing order.
     * @param {Array<number>} arr
     * @returns {boolean}
     */
    function isSorted(arr) {
        for (let i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) return false;
        }
        return true;
    }

    /**
     * Generate step-by-step trace for Binary Search.
     * Requires pre-sorted sequence.
     * @param {Array<number>} arr - Sorted array
     * @param {number} target - Target search value
     * @returns {Array<Object>} Sequence of visualization states
     */
    function binarySearchSteps(arr, target) {
        const steps = [];
        const n = arr.length;

        if (!isSorted(arr)) {
            throw new Error("Binary Search requires the input array to be sorted in non-decreasing order (Precondition Violation).");
        }

        let low = 0;
        let high = n - 1;
        let equalityComparisons = 0;
        let orderingComparisons = 0;
        let totalComparisons = 0;
        let iterations = 0;
        let found = false;
        let resultIndex = -1;

        steps.push({
            type: "init",
            array: [...arr],
            low: low,
            high: high,
            mid: -1,
            discardedRanges: [],
            equalityComparisons: 0,
            orderingComparisons: 0,
            totalComparisons: 0,
            iterations: 0,
            found: false,
            resultIndex: -1,
            description: `Starting Binary Search on sorted sequence (n = ${n}) for target = ${target}. Range: [${low}, ${high}].`
        });

        const discarded = [];

        while (low <= high) {
            iterations++;
            const mid = Math.floor((low + high) / 2);

            // Equality probe
            equalityComparisons++;
            totalComparisons++;

            steps.push({
                type: "probe_equality",
                array: [...arr],
                low: low,
                high: high,
                mid: mid,
                discardedRanges: [...discarded],
                equalityComparisons: equalityComparisons,
                orderingComparisons: orderingComparisons,
                totalComparisons: totalComparisons,
                iterations: iterations,
                found: false,
                resultIndex: -1,
                description: `Iteration ${iterations}: Probing midpoint mid = ${mid} (arr[${mid}] = ${arr[mid]}). Equality test: arr[${mid}] === ${target}?`
            });

            if (arr[mid] === target) {
                found = true;
                resultIndex = mid;
                steps.push({
                    type: "match",
                    array: [...arr],
                    low: low,
                    high: high,
                    mid: mid,
                    discardedRanges: [...discarded],
                    equalityComparisons: equalityComparisons,
                    orderingComparisons: orderingComparisons,
                    totalComparisons: totalComparisons,
                    iterations: iterations,
                    found: true,
                    resultIndex: mid,
                    description: `Target ${target} matched at index ${mid}! Terminating search with ${totalComparisons} key comparisons.`
                });
                break;
            }

            // Ordering probe
            orderingComparisons++;
            totalComparisons++;

            if (arr[mid] < target) {
                discarded.push({ start: low, end: mid });
                steps.push({
                    type: "branch_right",
                    array: [...arr],
                    low: low,
                    high: high,
                    mid: mid,
                    discardedRanges: [...discarded],
                    equalityComparisons: equalityComparisons,
                    orderingComparisons: orderingComparisons,
                    totalComparisons: totalComparisons,
                    iterations: iterations,
                    found: false,
                    resultIndex: -1,
                    description: `arr[${mid}] (${arr[mid]}) < ${target}. Discarding left subrange [${low}, ${mid}]. New low = ${mid + 1}.`
                });
                low = mid + 1;
            } else {
                discarded.push({ start: mid, end: high });
                steps.push({
                    type: "branch_left",
                    array: [...arr],
                    low: low,
                    high: high,
                    mid: mid,
                    discardedRanges: [...discarded],
                    equalityComparisons: equalityComparisons,
                    orderingComparisons: orderingComparisons,
                    totalComparisons: totalComparisons,
                    iterations: iterations,
                    found: false,
                    resultIndex: -1,
                    description: `arr[${mid}] (${arr[mid]}) > ${target}. Discarding right subrange [${mid}, ${high}]. New high = ${mid - 1}.`
                });
                high = mid - 1;
            }
        }

        if (!found) {
            steps.push({
                type: "not_found",
                array: [...arr],
                low: low,
                high: high,
                mid: -1,
                discardedRanges: [...discarded, { start: 0, end: n - 1 }],
                equalityComparisons: equalityComparisons,
                orderingComparisons: orderingComparisons,
                totalComparisons: totalComparisons,
                iterations: iterations,
                found: false,
                resultIndex: -1,
                description: `Search space exhausted (low = ${low} > high = ${high}). Target ${target} not in sequence. Total comparisons = ${totalComparisons}.`
            });
        }

        return steps;
    }

    /**
     * Generate step-by-step trace for Bubble Sort (Rosen §3.1, Alg. 4).
     * Strictly fixed passes without early termination: exactly n(n - 1) / 2 comparisons.
     * @param {Array<number>} arr - Input array
     * @returns {Array<Object>} Sequence of visualization states
     */
    function bubbleSortSteps(arr) {
        const steps = [];
        const a = [...arr];
        const n = a.length;
        let comparisons = 0;
        let swaps = 0;

        steps.push({
            type: "init",
            array: [...a],
            comparingIndices: [-1, -1],
            swappingIndices: [-1, -1],
            sortedStartIndex: n,
            pass: 0,
            comparisons: 0,
            swaps: 0,
            description: `Starting Bubble Sort on n = ${n} elements. Classical textbook fixed-pass model (Rosen §3.1). Total planned comparisons = ${n * (n - 1) / 2}.`
        });

        for (let i = 0; i < n - 1; i++) {
            const currentPass = i + 1;
            const passComparisons = n - 1 - i;

            for (let j = 0; j < passComparisons; j++) {
                comparisons++;

                // Compare state
                steps.push({
                    type: "compare",
                    array: [...a],
                    comparingIndices: [j, j + 1],
                    swappingIndices: [-1, -1],
                    sortedStartIndex: n - i,
                    pass: currentPass,
                    comparisons: comparisons,
                    swaps: swaps,
                    description: `Pass ${currentPass}/${n - 1}: Comparing adjacent elements a[${j}] = ${a[j]} and a[${j + 1}] = ${a[j + 1]}.`
                });

                if (a[j] > a[j + 1]) {
                    // Swap elements
                    const temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                    swaps++;

                    steps.push({
                        type: "swap",
                        array: [...a],
                        comparingIndices: [-1, -1],
                        swappingIndices: [j, j + 1],
                        sortedStartIndex: n - i,
                        pass: currentPass,
                        comparisons: comparisons,
                        swaps: swaps,
                        description: `Swapped inverted pair: ${a[j + 1]} > ${a[j]}. Swaps count = ${swaps}.`
                    });
                }
            }

            // Element at n - 1 - i is now settled into final sorted position
            steps.push({
                type: "pass_complete",
                array: [...a],
                comparingIndices: [-1, -1],
                swappingIndices: [-1, -1],
                sortedStartIndex: n - 1 - i,
                pass: currentPass,
                comparisons: comparisons,
                swaps: swaps,
                description: `Pass ${currentPass} complete. Element at index ${n - 1 - i} (${a[n - 1 - i]}) is settled into final sorted position.`
            });
        }

        // Final sorted state
        steps.push({
            type: "finished",
            array: [...a],
            comparingIndices: [-1, -1],
            swappingIndices: [-1, -1],
            sortedStartIndex: 0,
            pass: n - 1,
            comparisons: comparisons,
            swaps: swaps,
            description: `Bubble Sort complete! Final comparisons = ${comparisons} (exactly n(n-1)/2 = ${n * (n - 1) / 2}). Total swaps = ${swaps}.`
        });

        return steps;
    }

    /**
     * Generate step-by-step trace for Insertion Sort (Rosen §3.1, Alg. 5).
     * Distinguishes key element comparisons from rightward shifts.
     * @param {Array<number>} arr - Input array
     * @returns {Array<Object>} Sequence of visualization states
     */
    function insertionSortSteps(arr) {
        const steps = [];
        const a = [...arr];
        const n = a.length;
        let comparisons = 0;
        let rightShifts = 0;

        steps.push({
            type: "init",
            array: [...a],
            keyIndex: -1,
            keyValue: null,
            comparingIndex: -1,
            shiftingIndices: [-1, -1],
            sortedPrefixLength: 1,
            pass: 0,
            comparisons: 0,
            rightShifts: 0,
            description: `Starting Insertion Sort on n = ${n} elements (Rosen §3.1). Sub-array [0..0] is trivially sorted.`
        });

        for (let i = 1; i < n; i++) {
            const key = a[i];
            let j = i - 1;

            steps.push({
                type: "pick_key",
                array: [...a],
                keyIndex: i,
                keyValue: key,
                comparingIndex: -1,
                shiftingIndices: [-1, -1],
                sortedPrefixLength: i,
                pass: i,
                comparisons: comparisons,
                rightShifts: rightShifts,
                description: `Pass ${i}/${n - 1}: Extracted key = ${key} at index ${i}. Preparing to insert into sorted prefix [0..${i - 1}].`
            });

            while (j >= 0 && a[j] > key) {
                comparisons++;

                steps.push({
                    type: "compare",
                    array: [...a],
                    keyIndex: i,
                    keyValue: key,
                    comparingIndex: j,
                    shiftingIndices: [-1, -1],
                    sortedPrefixLength: i,
                    pass: i,
                    comparisons: comparisons,
                    rightShifts: rightShifts,
                    description: `Comparing prefix element a[${j}] = ${a[j]} > key (${key}). Condition True.`
                });

                // Right shift
                a[j + 1] = a[j];
                rightShifts++;

                steps.push({
                    type: "shift",
                    array: [...a],
                    keyIndex: i,
                    keyValue: key,
                    comparingIndex: -1,
                    shiftingIndices: [j, j + 1],
                    sortedPrefixLength: i,
                    pass: i,
                    comparisons: comparisons,
                    rightShifts: rightShifts,
                    description: `Shifted a[${j}] (${a[j]}) rightward into slot ${j + 1}. Total right shifts = ${rightShifts}.`
                });

                j--;
            }

            // Non-boundary loop exit check
            if (j >= 0) {
                comparisons++;
                steps.push({
                    type: "compare_stop",
                    array: [...a],
                    keyIndex: i,
                    keyValue: key,
                    comparingIndex: j,
                    shiftingIndices: [-1, -1],
                    sortedPrefixLength: i,
                    pass: i,
                    comparisons: comparisons,
                    rightShifts: rightShifts,
                    description: `Comparing prefix element a[${j}] = ${a[j]} <= key (${key}). Search terminated.`
                });
            }

            // Insert key into slot j + 1
            a[j + 1] = key;

            steps.push({
                type: "insert_key",
                array: [...a],
                keyIndex: j + 1,
                keyValue: key,
                comparingIndex: -1,
                shiftingIndices: [-1, -1],
                sortedPrefixLength: i + 1,
                pass: i,
                comparisons: comparisons,
                rightShifts: rightShifts,
                description: `Inserted key (${key}) into slot ${j + 1}. Sorted prefix now spans [0..${i}].`
            });
        }

        steps.push({
            type: "finished",
            array: [...a],
            keyIndex: -1,
            keyValue: null,
            comparingIndex: -1,
            shiftingIndices: [-1, -1],
            sortedPrefixLength: n,
            pass: n - 1,
            comparisons: comparisons,
            rightShifts: rightShifts,
            description: `Insertion Sort complete! Total comparisons = ${comparisons}. Total right shifts = ${rightShifts}.`
        });

        return steps;
    }

    /**
     * Compute total inversions in an array.
     * @param {Array<number>} arr
     * @returns {number}
     */
    function countInversions(arr) {
        let count = 0;
        const n = arr.length;
        for (let i = 0; i < n - 1; i++) {
            for (let j = i + 1; j < n; j++) {
                if (arr[i] > arr[j]) count++;
            }
        }
        return count;
    }

    /**
     * Compute exact theoretical operation counts for given algorithm and input size.
     */
    function getTheoreticalMetrics(algorithm, n, caseType = "worst") {
        switch (algorithm) {
            case "linear_search":
                return {
                    best: { comparisons: 1, complexity: "\\Theta(1)" },
                    average: { comparisons: Math.round((n + 1) / 2), complexity: "\\Theta(n)" },
                    worst: { comparisons: n, complexity: "\\Theta(n)" }
                }[caseType] || { comparisons: n, complexity: "\\Theta(n)" };

            case "binary_search":
                return {
                    best: { comparisons: 1, complexity: "\\Theta(1)" },
                    average: { comparisons: Math.round(2 * Math.log2(n)), complexity: "\\Theta(\\log n)" },
                    worst: { comparisons: 2 * (Math.floor(Math.log2(n)) + 1), complexity: "\\Theta(\\log n)" }
                }[caseType] || { comparisons: 2 * (Math.floor(Math.log2(n)) + 1), complexity: "\\Theta(\\log n)" };

            case "bubble_sort":
                return {
                    comparisons: (n * (n - 1)) / 2,
                    swaps: caseType === "best" ? 0 : (caseType === "worst" ? (n * (n - 1)) / 2 : Math.round((n * (n - 1)) / 4)),
                    complexity: "\\Theta(n^2)"
                };

            case "insertion_sort":
                if (caseType === "best") {
                    return { comparisons: n - 1, shifts: 0, complexity: "\\Theta(n)" };
                } else if (caseType === "worst") {
                    return { comparisons: (n * (n - 1)) / 2, shifts: (n * (n - 1)) / 2, complexity: "\\Theta(n^2)" };
                } else {
                    return { comparisons: Math.round((n * (n - 1)) / 4), shifts: Math.round((n * (n - 1)) / 4), complexity: "\\Theta(n^2)" };
                }

            default:
                return null;
        }
    }

    return {
        linearSearchSteps,
        binarySearchSteps,
        bubbleSortSteps,
        insertionSortSteps,
        isSorted,
        countInversions,
        getTheoreticalMetrics
    };
})();

// Attach to module if available in test runner
if (typeof module !== "undefined" && module.exports) {
    module.exports = Algorithms;
}
