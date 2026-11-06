"""Measure planner components on the sample size and larger generated inputs."""
import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.algorithms import dijkstra, knapsack, merge_sort_parcels, nearest_neighbor_route
from src.models import Parcel


def build_case(parcel_count: int) -> tuple[list[Parcel], dict[str, dict[str, float]], int]:
    destinations = [f"Customer {index}" for index in range(parcel_count)]
    parcels = [
        Parcel(
            f"P{index:03d}",
            destination,
            weight=(index % 7) + 1,
            value=30 + (index % 13) * 5,
            priority=(index % 5) + 1,
            deadline=(index % 10) + 1,
        )
        for index, destination in enumerate(destinations)
    ]
    graph: dict[str, dict[str, float]] = {"Depot": {}}
    for index, destination in enumerate(destinations):
        next_destination = destinations[(index + 1) % parcel_count]
        graph.setdefault(destination, {})[next_destination] = 1.0
        graph.setdefault(next_destination, {})[destination] = 1.0
        graph["Depot"][destination] = float((index % 9) + 1)
        graph[destination]["Depot"] = float((index % 9) + 1)
    return parcels, graph, max(15, parcel_count * 2)


def measure(parcel_count: int) -> list[tuple[int, str, float]]:
    parcels, graph, capacity = build_case(parcel_count)
    timings: list[tuple[int, str, float]] = []

    start = time.perf_counter()
    merge_sort_parcels(parcels)
    timings.append((parcel_count, "merge_sort", time.perf_counter() - start))

    start = time.perf_counter()
    knapsack(parcels, capacity)
    timings.append((parcel_count, "knapsack_dp", time.perf_counter() - start))

    start = time.perf_counter()
    dijkstra(graph, "Depot")
    timings.append((parcel_count, "dijkstra", time.perf_counter() - start))

    start = time.perf_counter()
    nearest_neighbor_route(graph, "Depot", [parcel.destination for parcel in parcels])
    timings.append((parcel_count, "nearest_neighbor", time.perf_counter() - start))
    return timings


def main() -> None:
    rows = [row for parcel_count in (8, 40, 80) for row in measure(parcel_count)]
    output_path = Path("images/scaled_runtime_results.csv")
    output_path.parent.mkdir(exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["parcel_count", "component", "seconds"])
        writer.writerows(rows)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()