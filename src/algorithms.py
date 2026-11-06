"""Algorithmic building blocks used by the courier planner."""
from __future__ import annotations

from heapq import heappop, heappush
from typing import Iterable
from .models import Parcel, RouteResult


def merge_sort_parcels(parcels: Iterable[Parcel]) -> list[Parcel]:
    """Stable merge sort: high priority first, then earliest deadline."""
    items = list(parcels)
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = merge_sort_parcels(items[:middle])
    right = merge_sort_parcels(items[middle:])
    result: list[Parcel] = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_key = (-left[i].priority, left[i].deadline)
        right_key = (-right[j].priority, right[j].deadline)
        if left_key <= right_key:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


def knapsack(parcels: list[Parcel], capacity: int) -> tuple[list[Parcel], int, list[list[int]]]:
    """0/1 knapsack maximizing parcel value under a weight capacity."""
    n = len(parcels)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, parcel in enumerate(parcels, 1):
        for weight in range(capacity + 1):
            table[i][weight] = table[i - 1][weight]
            if parcel.weight <= weight:
                table[i][weight] = max(table[i][weight], table[i - 1][weight - parcel.weight] + parcel.value)
    selected: list[Parcel] = []
    remaining = capacity
    for i in range(n, 0, -1):
        if table[i][remaining] != table[i - 1][remaining]:
            selected.append(parcels[i - 1])
            remaining -= parcels[i - 1].weight
    selected.reverse()
    return selected, table[n][capacity], table


def dijkstra(graph: dict[str, dict[str, float]], start: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """Single-source shortest paths for a non-negative weighted graph."""
    distances = {node: float("inf") for node in graph}
    previous: dict[str, str | None] = {node: None for node in graph}
    distances[start] = 0.0
    heap = [(0.0, start)]
    while heap:
        distance, node = heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, edge_weight in graph[node].items():
            candidate = distance + edge_weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heappush(heap, (candidate, neighbor))
    return distances, previous


def reconstruct_path(previous: dict[str, str | None], start: str, end: str) -> list[str]:
    path: list[str] = []
    current: str | None = end
    while current is not None:
        path.append(current)
        if current == start:
            return path[::-1]
        current = previous[current]
    return []


def nearest_neighbor_route(graph: dict[str, dict[str, float]], start: str, stops: list[str]) -> RouteResult:
    """TSP approximation: repeatedly visit the nearest unvisited stop."""
    route = [start]
    total = 0.0
    current = start
    unvisited = set(stops) - {start}
    while unvisited:
        distances, previous = dijkstra(graph, current)
        next_stop = min(unvisited, key=lambda stop: distances[stop])
        segment = reconstruct_path(previous, current, next_stop)
        total += distances[next_stop]
        route.extend(segment[1:])
        unvisited.remove(next_stop)
        current = next_stop
    distances, previous = dijkstra(graph, current)
    if start != current:
        segment = reconstruct_path(previous, current, start)
        total += distances[start]
        route.extend(segment[1:])
    return RouteResult(route, total)
