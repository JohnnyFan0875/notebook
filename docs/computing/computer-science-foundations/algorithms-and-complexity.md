# Algorithms and Complexity

## Core Idea

An algorithm is a step-by-step procedure for solving a problem. The same problem can often be solved by multiple algorithms, and the main tradeoff is usually correctness plus efficiency.

## Common Algorithm Families

| Family | Main task | Typical examples |
| --- | --- | --- |
| Sorting | Reorder data | Bubble sort, quick sort, merge sort |
| Searching | Find a target item | Linear search, binary search |
| Graph algorithms | Traverse or optimize over relationships | BFS, DFS, shortest path |

## Why Complexity Matters

Algorithm analysis asks how resource usage grows as input size grows.

The two most common measures are:

- Time complexity: how execution time scales with input size.
- Space complexity: how extra memory usage scales with input size.

This is more useful than raw timing because hardware changes, but growth behavior remains informative.

## Big-O Notation

Big-O describes an upper-bound growth pattern as input size increases.

| Complexity | Intuition | Typical interpretation |
| --- | --- | --- |
| `O(1)` | Constant | Cost stays roughly fixed |
| `O(log n)` | Logarithmic | Cost grows slowly as input grows |
| `O(n)` | Linear | Cost grows in direct proportion to input size |
| `O(n log n)` | Linearithmic | Common for efficient comparison-based sorting |
| `O(n^2)` | Quadratic | Pairwise comparison patterns become expensive quickly |

Big-O hides constants and low-order terms so we can focus on the dominant scaling behavior.

## Time vs Space

Two algorithms can solve the same problem with different tradeoffs:

- One may run faster but allocate more temporary memory.
- Another may save memory but do more repeated work.

Good engineering depends on workload constraints, not on one metric alone.

## Sorting Example: Bubble Sort vs Quick Sort

| Algorithm | Main idea | Typical complexity | When the intuition helps |
| --- | --- | --- | --- |
| Bubble sort | Repeatedly compare adjacent items and swap | `O(n^2)` | Simple teaching example, poor scalability |
| Quick sort | Partition around a pivot, then solve subproblems recursively | Average `O(n log n)` | Better for large datasets when implemented well |

The practical lesson is not just that one algorithm is "better", but that growth rate dominates when datasets become large.

## Searching Example: Linear Search vs Binary Search

| Algorithm | Main idea | Complexity | Constraint |
| --- | --- | --- | --- |
| Linear search | Check each element one by one | `O(n)` | Works on unsorted data |
| Binary search | Repeatedly halve the search interval | `O(log n)` | Requires sorted data |

Binary search is faster because it discards half the search space at each step, but that advantage depends on meeting its precondition.

## Real-World Reading

- Sorting is used when items must be ordered by price, time, score, or priority.
- Searching is used when a specific record, product, or event must be found.
- Efficiency becomes visible when data volume scales, not just when an example is small.

## Practical Takeaways

- Start with the problem definition, then choose an algorithm family.
- Analyze both runtime and memory growth.
- Faster asymptotic growth usually matters more than constant-factor polish at scale.
- Preconditions matter: an efficient algorithm may only work if the data is organized the right way.
