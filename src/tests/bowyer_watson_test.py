import math
import unittest
from bowyer_watson import Edge, Triangle # BowyerWatson

class TestEdge(unittest.TestCase):
    def test_edges_equal_with_reverse_order_vertices(self):
        e1 = Edge((0, 0), (1, 1))
        e2 = Edge((1, 1), (0, 0))

        self.assertEqual(e1, e2)
        self.assertEqual(hash(e1), hash(e2))

    def test_edges_not_equal(self):
        e1 = Edge((0, 0), (1, 1))
        e2 = Edge((1, 1), (2, 2))

        self.assertNotEqual(e1, e2)

class TestTriangle(unittest.TestCase):
    def test_circumcircle_calculation(self):
        v1, v2, v3 = ((0, 0), (3, 0), (0, 5))
        triangle = Triangle(v1, v2, v3)

        ux = triangle.circumcenter[0]
        uy = triangle.circumcenter[1]

        # Use the distance formula between two coordinates
        # to find the distances from the circumcenter to the vertices

        d1 = math.sqrt((ux - v1[0])**2 + (uy - v1[1])**2)
        d2 = math.sqrt((ux - v2[0])**2 + (uy - v2[1])**2)
        d3 = math.sqrt((ux - v3[0])**2 + (uy - v3[1])**2)

        # Check the circumcenter is the same distance from all vertices

        self.assertAlmostEqual(d1, d2)
        self.assertAlmostEqual(d2, d3)

        # Check the circumradius is the same as the calculated distances

        self.assertAlmostEqual(d1**2, triangle.sq_circumradius)

    def test_no_circumcircle_when_determinant_zero(self):
        # Test with a degenerate triangle
        triangle = Triangle((0, 0), (1, 1), (2, 2))

        self.assertEqual(triangle.circumcenter, None)
        self.assertEqual(triangle.sq_circumradius, float("inf"))

    def test_vertex_in_circumcircle(self):
        triangle = Triangle((0, 0), (3, 0), (0, 5))

        self.assertTrue(triangle.vertex_in_circumcircle((2, 2)))
        self.assertFalse(triangle.vertex_in_circumcircle((5, 5)))

class TestBowyerWatson(unittest.TestCase):
    def test_all_vertices_in_super_triangle(self):
        pass

    def test_invalid_triangle_detection(self):
        pass

    def test_polygonal_hole_edge_detection(self):
        pass
