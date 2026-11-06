# Mini-Courier Planner

A complete DAA capstone prototype that prioritizes parcels, fills a courier box, computes shortest paths, and builds an approximate delivery tour.

## Algorithms
- **Merge sort:** parcels ordered by descending priority and ascending deadline, `O(n log n)`.
- **0/1 knapsack dynamic programming:** maximizes parcel value within the trip capacity, `O(nC)` time and `O(nC)` memory.
- **Dijkstra:** shortest paths on a non-negative weighted customer graph, `O((V+E) log V)` with a heap.
- **Nearest-neighbor TSP approximation:** repeatedly visits the closest unvisited destination and returns to the depot; heuristic, typically `O(k(E+V log V))` here because it calls Dijkstra for each stop.

## Setup and execution
Python 3.10+ is recommended. No third-party package is needed for the core CLI or tests.

```bash
python3 -m unittest discover -s tests -v
python3 main.py --capacity 15 --benchmark
```

The benchmark writes `images/runtime_results.csv`. To generate a chart after installing requirements:

```bash
python3 scripts/plot_runtime.py
python3 scripts/benchmark_scale.py
```

This creates `images/runtime_chart.svg`. The scaling benchmark creates `images/scaled_runtime_results.csv` for small and larger generated inputs. Open `mini_courier_planner.ipynb` for the guided demonstration and `REPORT.md` for the submission report.

## Repository structure
- `main.py`: command-line application and benchmark runner
- `src/`: data models, file loading, and algorithms
- `datasets/`: sample parcel CSV and weighted route graph JSON
- `tests/`: correctness tests
- `scripts/`: evidence/chart generation
- `images/`: generated runtime evidence
- `mini_courier_planner.ipynb`: complete notebook walkthrough
- `REPORT.md`: design, methodology, results, complexity, and future scope

## Expected sample result
With capacity 15, the planner selects a high-value feasible set, prints the prioritized order, and produces a depot-to-stops-to-depot route. Exact runtime values depend on the machine, so the benchmark records measured values rather than hard-coding them.
