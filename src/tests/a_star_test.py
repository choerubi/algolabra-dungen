import unittest
from a_star import Vertex, AStar

class TestAStar(unittest.TestCase):
    def setUp(self):
        self.a_star = AStar()
        self.tiles = [[0 for col in range(10)] for row in range(10)]

    def test_path_from_start_to_goal_found(self):
        start_pos = (1, 1)
        goal_pos = (5, 5)
        path = self.a_star.find_path(start_pos, goal_pos, self.tiles)

        self.assertEqual(path[0], start_pos)
        self.assertEqual(path[-1], goal_pos)

    def test_start_and_goal_with_same_position(self):
        start_pos = (1, 1)
        goal_pos = (1, 1)
        path = self.a_star.find_path(start_pos, goal_pos, self.tiles)

        self.assertEqual(path, [(1, 1)])

    def test_no_path_when_goal_out_of_reach(self):
        start_pos = (1, 1)
        goal_pos = (100, 100)
        path = self.a_star.find_path(start_pos, goal_pos, self.tiles)

        self.assertEqual(path, None)

    def test_correct_neighbors_for_edge_tile(self):
        v = Vertex((1, 0), None, 0, 0)
        neighbors = self.a_star.get_neighbors(v, self.tiles)

        self.assertEqual(len(neighbors), 3)
        self.assertEqual(sorted(neighbors), sorted([(0, 0), (2, 0), (1, 1)]))

    def test_correct_neighbors_for_corner_tile(self):
        v = Vertex((0, 0), None, 0, 0)
        neighbors = self.a_star.get_neighbors(v, self.tiles)

        self.assertEqual(len(neighbors), 2)
        self.assertEqual(sorted(neighbors), sorted([(0, 1), (1, 0)]))

    def test_correct_tile_costs_returned(self):
        self.assertEqual(self.a_star.get_tile_cost(0), 1)
        self.assertEqual(self.a_star.get_tile_cost(1), 10)
        self.assertEqual(self.a_star.get_tile_cost(2), 50)
        self.assertEqual(self.a_star.get_tile_cost(100), float("inf"))
