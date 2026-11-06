"""Command-line demonstration for the Mini-Courier Planner."""
import argparse
import csv
import random
import time
from pathlib import Path
from src.algorithms import dijkstra, knapsack, merge_sort_parcels, nearest_neighbor_route
from src.io_utils import load_graph, load_parcels


def benchmark(parcels, graph, capacity):
    timings = {}
    start = time.perf_counter(); merge_sort_parcels(parcels); timings["merge_sort"] = time.perf_counter() - start
    start = time.perf_counter(); knapsack(parcels, capacity); timings["knapsack_dp"] = time.perf_counter() - start
    start = time.perf_counter(); dijkstra(graph, "Depot"); timings["dijkstra"] = time.perf_counter() - start
    stops = sorted({parcel.destination for parcel in parcels})
    start = time.perf_counter(); nearest_neighbor_route(graph, "Depot", stops); timings["nearest_neighbor"] = time.perf_counter() - start
    return timings


def main():
    parser = argparse.ArgumentParser(description="Plan prioritized parcels, packing, and delivery routes.")
    parser.add_argument("--parcels", default="datasets/parcels.csv")
    parser.add_argument("--graph", default="datasets/routes.json")
    parser.add_argument("--capacity", type=int, default=15)
    parser.add_argument("--benchmark", action="store_true")
    args = parser.parse_args()
    parcels = load_parcels(args.parcels)
    graph = load_graph(args.graph)
    prioritized = merge_sort_parcels(parcels)
    selected, value, table = knapsack(prioritized, args.capacity)
    route = nearest_neighbor_route(graph, "Depot", [p.destination for p in selected])
    print("MINI-COURIER PLANNER")
    print("=" * 22)
    print("Prioritized parcels:", " -> ".join(p.parcel_id for p in prioritized))
    print(f"Packing capacity: {args.capacity} kg | selected weight: {sum(p.weight for p in selected)} kg | value: {value}")
    print("Selected parcels:", ", ".join(f"{p.parcel_id}({p.destination})" for p in selected))
    print(f"Delivery route: {' -> '.join(route.path)}")
    print(f"Approximate route distance: {route.distance:.1f} km")
    if args.benchmark:
        timings = benchmark(parcels, graph, args.capacity)
        Path("images").mkdir(exist_ok=True)
        with open("images/runtime_results.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file); writer.writerow(["component", "seconds"]); writer.writerows(timings.items())
        print("Runtime results written to images/runtime_results.csv")
        for name, seconds in timings.items(): print(f"  {name:18} {seconds:.8f} s")

if __name__ == "__main__":
    main()
