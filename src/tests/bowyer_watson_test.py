import math
import unittest
from bowyer_watson import Edge, Triangle, BowyerWatson

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
    def test_correct_circumcircle_calculated(self):
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

        # Test with a degenerate triangle
        triangle = Triangle((0, 0), (1, 1), (2, 2))

        self.assertFalse(triangle.vertex_in_circumcircle((0, 0)))

class TestBowyerWatson(unittest.TestCase):
    def setUp(self):
        self.vertices = [(1, 1), (5, 2), (7, 3), (2,4), (8, 6), (5, 7), (2, 8), (8, 9)]
        self.bowyer_watson = BowyerWatson()
        self.bowyer_watson.triangulate(self.vertices)

        self.new_vertex = (5, 5)
        self.invalid_triangles = self.bowyer_watson.find_invalid_triangles(self.new_vertex)
        self.polygon_edges = self.bowyer_watson.find_polygonal_hole_edges(self.invalid_triangles)

    def test_all_vertices_in_super_triangle(self):
        super_triangle = self.bowyer_watson.create_super_triangle(self.vertices)

        a = super_triangle.v1
        b = super_triangle.v2
        c = super_triangle.v3

        def vertex_in_triangle(v, a, b, c):
            # Check if a vertex is inside a triangle by checking
            # if the vertex lies on the same side of each edge of the triangle
            ax, ay = a
            bx, by = b
            cx, cy = c
            vx, vy = v

            # Calculate cross products for each pair of triangle edge vectors
            # and vectors from the vertex to each triangle vertice
            c1 = (bx - ax) * (vy - ay) - (by - ay) * (vx - ax) # AB x AV
            c2 = (cx - bx) * (vy - by) - (cy - by) * (vx - bx) # BC x BV
            c3 = (ax - cx) * (vy - cy) - (ay - cy) * (vx - cx) # CA x CV

            # If cross product > 0, the vertex lies on the left side of the edge
            # If cross product < 0, the vertex lies on the right side of the edge
            # If cross product = 0, the vertex lies on the edge

            # To check if the vertex lies inside or on the edge of the triangle,
            # check if all products have the same sign (>= 0 or <= 0)
            left_side = c1 >= 0 and c2 >= 0 and c3 >= 0
            right_side = c1 <= 0 and c2 <= 0 and c3 <= 0

            return left_side or right_side

        for v in self.vertices:
            self.assertTrue(vertex_in_triangle(v, a, b, c))

    def test_invalid_triangles_detected(self):
        # Check all invalid triangles contain the new vertex in their circumcircle
        for t in self.invalid_triangles:
            self.assertTrue(t.vertex_in_circumcircle(self.new_vertex))

        valid_triangles = []

        for t in self.bowyer_watson.triangles:
            if t not in self.invalid_triangles:
                valid_triangles.append(t)

        # Check no valid triangle contains the new vertex in their circumcircle
        for t in valid_triangles:
            self.assertFalse(t.vertex_in_circumcircle(self.new_vertex))

    def test_polygonal_hole_edges_detected(self):
        edge_counts = {}

        for t in self.invalid_triangles:
            for e in t.edges:
                if e not in edge_counts:
                    edge_counts[e] = 1
                else:
                    edge_counts[e] += 1

        # Check only unshared edges are counted as polygonal hole edges
        for e, count in edge_counts.items():
            if count == 1:
                self.assertIn(e, self.polygon_edges)
            else:
                self.assertNotIn(e, self.polygon_edges)

    def correct_triangles_removed(self):
        self.bowyer_watson.remove_invalid_triangles(self.invalid_triangles)

        for t in self.invalid_triangles:
            self.assertNotIn(t, self.bowyer_watson.triangles)

    def polygonal_hole_filled(self):
        old_triangles = len(self.bowyer_watson.triangles)
        self.bowyer_watson.create_new_triangle(self.new_vertex, self.polygon_edges)
        new_triangles = len(self.bowyer_watson.triangles) - old_triangles

        # Check that the amount of new triangles is the same as the amount of polygon edges
        self.assertEqual(new_triangles, len(self.polygon_edges))

    def super_triangle_removed(self):
        super_triangle = self.bowyer_watson.create_super_triangle(self.vertices)
        self.bowyer_watson.triangles.append(super_triangle)
        self.bowyer_watson.remove_super_triangle(super_triangle)

        self.assertNotIn(super_triangle, self.bowyer_watson.triangles)

    def correct_triangulation(self):
        pass
