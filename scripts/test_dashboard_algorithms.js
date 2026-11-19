/**
 * Node.js automated test runner for dashboard/js/algorithms.js
 * Verifies algorithmic correctness, operation counts, edge cases,
 * precondition enforcement, and Inversion Equivalence in JavaScript.
 */

const assert = require("assert");
const Algorithms = require("../dashboard/js/algorithms.js");

console.log("==================================================");
console.log("RUNNING AUTOMATED DASHBOARD ALGORITHM TESTS (NODE)");
console.log("==================================================");

// 1. Linear Search Tests
console.log("Testing Linear Search...");
{
    // Best case: target at 0
    const steps1 = Algorithms.linearSearchSteps([42, 10, 20, 30], 42);
    const final1 = steps1[steps1.length - 1];
    assert.strictEqual(final1.found, true);
    assert.strictEqual(final1.resultIndex, 0);
    assert.strictEqual(final1.comparisons, 1);

    // Worst case: missing target
    const steps2 = Algorithms.linearSearchSteps([10, 20, 30, 40, 50], 99);
    const final2 = steps2[steps2.length - 1];
    assert.strictEqual(final2.found, false);
    assert.strictEqual(final2.resultIndex, -1);
    assert.strictEqual(final2.comparisons, 5); // Exactly n comparisons

    // Negative numbers and duplicates
    const steps3 = Algorithms.linearSearchSteps([-5, -2, 0, 3, 3, 7], 3);
    const final3 = steps3[steps3.length - 1];
    assert.strictEqual(final3.found, true);
    assert.strictEqual(final3.resultIndex, 3); // First occurrence
    console.log("  [PASS] Linear search tests passed.");
}

// 2. Binary Search Tests
console.log("Testing Binary Search...");
{
    // Best case: target at mid
    const sorted = [10, 20, 30, 40, 50, 60, 70];
    const steps1 = Algorithms.binarySearchSteps(sorted, 40);
    const final1 = steps1[steps1.length - 1];
    assert.strictEqual(final1.found, true);
    assert.strictEqual(final1.resultIndex, 3);
    assert.strictEqual(final1.equalityComparisons, 1);

    // Missing target
    const steps2 = Algorithms.binarySearchSteps(sorted, 99);
    const final2 = steps2[steps2.length - 1];
    assert.strictEqual(final2.found, false);
    assert.strictEqual(final2.resultIndex, -1);
    assert.ok(final2.totalComparisons > 0);

    // Precondition violation check
    let threw = false;
    try {
        Algorithms.binarySearchSteps([50, 20, 10], 10);
    } catch (e) {
        threw = true;
    }
    assert.strictEqual(threw, true, "Binary search must throw on unsorted array");
    console.log("  [PASS] Binary search tests passed.");
}

// 3. Bubble Sort Tests
console.log("Testing Bubble Sort (Rosen Fixed-Pass Formulation)...");
{
    const arr = [5, 4, 3, 2, 1];
    const n = arr.length;
    const steps = Algorithms.bubbleSortSteps(arr);
    const final = steps[steps.length - 1];

    // Sorted correctly
    assert.deepStrictEqual(final.array, [1, 2, 3, 4, 5]);
    // Exactly n(n-1)/2 comparisons
    assert.strictEqual(final.comparisons, (n * (n - 1)) / 2); // 10
    // Reverse array swaps = 10
    assert.strictEqual(final.swaps, 10);

    // Already sorted input: comparisons STILL n(n-1)/2, swaps = 0
    const sortedArr = [1, 2, 3, 4, 5];
    const stepsSorted = Algorithms.bubbleSortSteps(sortedArr);
    const finalSorted = stepsSorted[stepsSorted.length - 1];
    assert.strictEqual(finalSorted.comparisons, 10);
    assert.strictEqual(finalSorted.swaps, 0);
    console.log("  [PASS] Bubble sort fixed-pass tests passed.");
}

// 4. Insertion Sort Tests
console.log("Testing Insertion Sort...");
{
    // Pre-sorted input: comparisons = n - 1, shifts = 0 (Linear)
    const sortedArr = [10, 20, 30, 40, 50];
    const stepsSorted = Algorithms.insertionSortSteps(sortedArr);
    const finalSorted = stepsSorted[stepsSorted.length - 1];
    assert.deepStrictEqual(finalSorted.array, [10, 20, 30, 40, 50]);
    assert.strictEqual(finalSorted.comparisons, 4); // n - 1
    assert.strictEqual(finalSorted.rightShifts, 0);

    // Reverse input: comparisons = 10, shifts = 10
    const revArr = [5, 4, 3, 2, 1];
    const stepsRev = Algorithms.insertionSortSteps(revArr);
    const finalRev = stepsRev[stepsRev.length - 1];
    assert.deepStrictEqual(finalRev.array, [1, 2, 3, 4, 5]);
    assert.strictEqual(finalRev.comparisons, 10);
    assert.strictEqual(finalRev.rightShifts, 10);
    console.log("  [PASS] Insertion sort tests passed.");
}

// 5. Inversion Equivalence Theorem Test
console.log("Testing Inversion Equivalence Theorem...");
{
    const randArr = [34, 12, 89, 5, 23, 77, 61, 42, 19, 50];
    const inversions = Algorithms.countInversions(randArr);

    const bFinal = Algorithms.bubbleSortSteps(randArr).pop();
    const insFinal = Algorithms.insertionSortSteps(randArr).pop();

    assert.strictEqual(bFinal.swaps, insFinal.rightShifts);
    assert.strictEqual(bFinal.swaps, inversions);
    console.log(`  [PASS] Verified identity: Swaps (${bFinal.swaps}) === Shifts (${insFinal.rightShifts}) === Inversions (${inversions})`);
}

console.log("==================================================");
console.log("ALL 5 DASHBOARD ALGORITHM TEST SUITES PASSED!");
console.log("==================================================");
