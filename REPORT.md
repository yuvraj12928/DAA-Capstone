# Mini-Courier Planner: Technical Report

## 1. Problem and design
A courier must choose valuable parcels for one trip, visit their destinations, and return to the depot. Each parcel has an ID, destination, weight, value, priority, and deadline. The route dataset is an adjacency-list weighted graph.

Pipeline: load data -> merge-sort parcels -> solve 0/1 knapsack -> run Dijkstra while constructing a nearest-neighbor tour -> report route and measured performance.

The application flow is:

```text
CSV parcels + JSON graph
	  |
	  v
  Merge sort by priority/deadline
	  |
	  v
  0/1 knapsack under capacity
	  |
	  v
  Dijkstra + nearest-neighbor tour
	  |
	  v
  Route, value, and runtime evidence
```

## 2. Algorithm selection
Merge sort gives predictable `O(n log n)` prioritization and is stable. Knapsack DP is appropriate because parcel selection is binary and capacity is bounded; unlike a value/weight greedy rule, it guarantees the best value for the supplied capacity. Dijkstra is correct for non-negative road distances. Exact TSP is exponential, so nearest-neighbor is used as a practical approximation for a prototype.

## 3. Correctness evidence
The automated tests verify sorting tie rules, optimal knapsack value, a multi-edge shortest path, and route return to the depot. The CLI output demonstrates all four required algorithmic components. The DP table is returned by `knapsack()` and can be inspected in the notebook.

## 4. Complexity
Let `n` be parcels, `C` capacity, `V` graph vertices, `E` graph edges, and `k` selected destinations. Merge sort is `O(n log n)`. Knapsack is `O(nC)` time and memory. One heap-based Dijkstra run is `O((V+E)log V)`. The implemented nearest-neighbor route makes up to `k+1` Dijkstra runs, giving `O(k(V+E)log V)`.

## 5. Performance methodology
`main.py --benchmark` measures each component with `time.perf_counter()` and writes a CSV. `scripts/benchmark_scale.py` repeats the measurements for the sample size and larger generated inputs, making the growth trend visible. Single runs are still affected by interpreter overhead, so the results are comparative evidence rather than a formal performance estimate. The dependency-free chart script visualizes the measured sample as SVG.

## 6. Limitations and future scope
The nearest-neighbor tour is not guaranteed optimal. Future work could add 2-opt improvement, vehicle time windows, multiple vehicles, delivery-time feasibility, and repeated benchmark trials with confidence intervals. Graph validation could also reject negative weights and missing reciprocal edges before planning.

## 7. Conclusion
The prototype integrates sorting, dynamic programming, graph shortest paths, approximation, testing, and empirical evaluation in one reproducible Python project suitable for demonstration and viva discussion.
