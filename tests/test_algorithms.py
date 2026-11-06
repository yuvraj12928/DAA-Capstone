import unittest
from src.algorithms import dijkstra, knapsack, merge_sort_parcels, nearest_neighbor_route
from src.models import Parcel

class AlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.parcels = [Parcel("A", "X", 3, 40, 2, 2), Parcel("B", "Y", 2, 30, 5, 1), Parcel("C", "Z", 4, 70, 1, 3)]

    def test_merge_sort_priority_then_deadline(self):
        self.assertEqual([p.parcel_id for p in merge_sort_parcels(self.parcels)], ["B", "A", "C"])

    def test_knapsack(self):
        selected, value, _ = knapsack(self.parcels, 5)
        self.assertEqual(value, 70)
        self.assertEqual({p.parcel_id for p in selected}, {"A", "B"})

    def test_dijkstra(self):
        graph = {"A": {"B": 2, "C": 8}, "B": {"A": 2, "C": 3}, "C": {"A": 8, "B": 3}}
        distances, _ = dijkstra(graph, "A")
        self.assertEqual(distances["C"], 5)

    def test_route_returns_to_depot(self):
        graph = {"Depot": {"A": 2, "B": 5}, "A": {"Depot": 2, "B": 1}, "B": {"Depot": 5, "A": 1}}
        result = nearest_neighbor_route(graph, "Depot", ["A", "B"])
        self.assertEqual((result.path[0], result.path[-1]), ("Depot", "Depot"))
        self.assertEqual(result.distance, 6)

if __name__ == "__main__":
    unittest.main()
