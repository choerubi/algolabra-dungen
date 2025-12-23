import unittest
from bowyer_watson import BowyerWatson
from prim import Prim, add_random_edges

class TestPrim(unittest.TestCase):
    def setUp(self):
        self.vertices = [(1, 1), (5, 2), (7, 3), (2, 4), (8, 6), (5, 7), (2, 8), (8, 9)]
        self.bowyer_watson = BowyerWatson()
        self.triangles = self.bowyer_watson.triangulate(self.vertices)

        self.bw_edges = set()
        for t in self.triangles:
            for e in t.edges:
                self.bw_edges.add(e)

        self.prim = Prim()
        self.prim.get_vertices(self.triangles)
        self.mst_edges = self.prim.create_mst()

    def test_prim_stores_correct_neighbors(self):
        for e in self.mst_edges:
            self.assertIn(e.v1, self.prim.neighbors[e.v2])
            self.assertIn(e.v2, self.prim.neighbors[e.v1])

    def test_mst_edges_are_triangulation_edges(self):
        for e in self.mst_edges:
            self.assertIn(e, self.bw_edges)

    def test_correct_number_of_mst_edges(self):
        self.assertEqual(len(self.mst_edges), len(self.vertices) - 1)

    def test_vertices_not_explored_more_than_once(self):
        self.vertices.append((3, 5))
        self.vertices.append((6, 2))

        self.prim.get_vertices(self.bowyer_watson.triangulate(self.vertices))
        self.mst_edges = self.prim.create_mst()

        self.assertEqual(len(self.mst_edges), len(self.vertices) - 1)

    def test_mst_with_one_vertex(self):
        self.prim.vertices = {(0, 0)}
        self.prim.neighbors = {(0, 0): set()}

        mst_edges = self.prim.create_mst()

        self.assertEqual(len(mst_edges), 0)

    def test_all_vertices_connected(self):
        neighbors = {}

        for v in self.vertices:
            neighbors[v] = set()

        for e in self.mst_edges:
            neighbors[e.v1].add(e.v2)
            neighbors[e.v2].add(e.v1)

        # Traverse with BFS
        connected_vertices = set()
        queue = []

        connected_vertices.add(self.vertices[0])
        queue.append(self.vertices[0])

        for v in queue:
            for next_v in neighbors[v]:
                if next_v not in connected_vertices:
                    connected_vertices.add(next_v)
                    queue.append(next_v)

        self.assertEqual(connected_vertices, set(self.vertices))

class TestAddRandomEdges(unittest.TestCase):
    def setUp(self):
        self.vertices = [(1, 1), (5, 2), (7, 3), (2, 4), (8, 6), (5, 7), (2, 8), (8, 9)]
        self.bowyer_watson = BowyerWatson()
        self.triangles = self.bowyer_watson.triangulate(self.vertices)

        self.bw_edges = set()
        for t in self.triangles:
            for e in t.edges:
                self.bw_edges.add(e)

        self.prim = Prim()
        self.prim.get_vertices(self.triangles)

    def test_correct_number_of_extra_edges(self):
        # Test extra edges when chance is 0
        mst_edges = self.prim.create_mst()
        extra_edges = add_random_edges(0, mst_edges, self.triangles)
        new_mst_edges = mst_edges.union(extra_edges)
        self.assertEqual(new_mst_edges, mst_edges)

        # Test extra edges when chance is 100
        mst_edges = self.prim.create_mst()
        extra_edges = add_random_edges(100, mst_edges, self.triangles)
        new_mst_edges = mst_edges.union(extra_edges)
        self.assertEqual(new_mst_edges, self.bw_edges)
