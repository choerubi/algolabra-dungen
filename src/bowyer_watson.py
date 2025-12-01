from typing import Tuple

class Edge:
    """A class to represent an undirected edge between two vertices."""

    def __init__(self, v1: Tuple, v2: Tuple):
        """A constructor that initializes an edge."""

        self.v1 = (v1[0], v1[1])
        self.v2 = (v2[0], v2[1])

    # Use set for undirected edges
    def __eq__(self, other):
        return {self.v1, self.v2} == {other.v1, other.v2}

    def __hash__(self):
        return hash(frozenset([self.v1, self.v2]))

class Triangle:
    """A class to represent a triangle consisting of three vertices."""

    def __init__(self, v1: Tuple, v2: Tuple, v3: Tuple):
        """A constructor that initializes the vertices and the circumcircle."""

        self.v1 = (v1[0], v1[1])
        self.v2 = (v2[0], v2[1])
        self.v3 = (v3[0], v3[1])

        self.edges = [
            Edge(self.v1, self.v2),
            Edge(self.v2, self.v3),
            Edge(self.v3, self.v1)
        ]

        self.circumcenter = None
        self.sq_circumradius = None
        self.calculate_circumcircle()

    def calculate_circumcircle(self):
        """A method that calculates the circumcenter and circumradius of the triangle."""

        ax = self.v1[0]
        ay = self.v1[1]
        bx = self.v2[0]
        by = self.v2[1]
        cx = self.v3[0]
        cy = self.v3[1]

        # Calculate determinant
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

        # If determinant is zero, the triangle has zero area,
        # meaning it has collinear vertices and no valid circumcircle exists
        if d == 0:
            self.circumcenter = None
            self.sq_circumradius = float("inf")
            return

        # Calculate circumcenter coordinates
        ux = (
            (ax * ax + ay * ay) * (by - cy) +
            (bx * bx + by * by) * (cy - ay) +
            (cx * cx + cy * cy) * (ay - by)
            ) / d
        uy = (
            (ax * ax + ay * ay) * (cx - bx) +
            (bx * bx + by * by) * (ax - cx) +
            (cx * cx + cy * cy) * (bx - ax)
            ) / d
        self.circumcenter = (ux, uy)

        # Calculate squared distance from circumcenter to any of the vertices
        self.sq_circumradius = (ux - ax)**2 + (uy - ay)**2

    def vertex_in_circumcircle(self, vertex: Tuple):
        """A method that checks whether a vertex is inside the circumcircle."""

        if self.circumcenter is None:
            return False

        dx = self.circumcenter[0] - vertex[0]
        dy = self.circumcenter[1] - vertex[1]
        return dx**2 + dy**2 < self.sq_circumradius

class BowyerWatson:
    """A class that implements the Bowyer-Watson algorithm for the Delaunay triangulation."""

    def __init__(self):
        """A constructor that initializes an empty list to store the triangulation triangles."""

        self.triangles = []

    def triangulate(self, vertices):
        """A method that performs the Delaunay triangulation for the given vertices."""

        # Create the super triangle
        super_triangle = self.create_super_triangle(vertices)
        self.triangles = [super_triangle]

        # Iterate over given vertices one at a time
        for vertex in vertices:
            self.add_vertex(vertex)

        # Final step of the triangulation procedure
        # Remove triangles that share a vertex with the initial super triangle,
        # as the super triangle vertices are not part of the initial set of vertices
        self.remove_super_triangle(super_triangle)

        return self.triangles

    def add_vertex(self, vertex):
        """A method that adds a new vertex into the triangulation."""

        invalid_triangles = self.find_invalid_triangles(vertex)
        polygon_edges = self.find_polygonal_hole_edges(invalid_triangles)

        self.remove_invalid_triangles(invalid_triangles)
        self.create_new_triangle(vertex, polygon_edges)

    def create_super_triangle(self, vertices):
        """A method that creates a triangle containing all given vertices."""

        # Find minimum and maximum vertex coordinates
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        for v in vertices:
            min_x = min(min_x, v[0])
            min_y = min(min_y, v[1])
            max_x = max(max_x, v[0])
            max_y = max(max_y, v[1])

        # Find the maximum difference between x or y coordinates
        # to determine how large the super triangle has to be to contain all vertices
        d_max = max(max_x - min_x, max_y - min_y)

        # Center the super triangle around the min and max coordinates
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        # Create super triangle vertices
        # Multiply by scale factor 20 to make sure all vertices are inside the triangle
        v1 = (mid_x, mid_y - 20 * d_max)
        v2 = (mid_x - 20 * d_max, mid_y + 20 * d_max)
        v3 = (mid_x + 20 * d_max, mid_y + 20 * d_max)
        return Triangle(v1, v2, v3)

    def find_invalid_triangles(self, vertex):
        """A method that finds triangles with circumcircles that contain the given vertex."""

        invalid_triangles = set()

        for t in self.triangles:
            if t.vertex_in_circumcircle(vertex):
                invalid_triangles.add(t)

        return invalid_triangles

    def find_polygonal_hole_edges(self, invalid_triangles):
        """A method that finds all edges in the set of invalid triangles that
            are not shared between two invalid triangles.

        This basically means the edges at the boundaries of the polygonal hole,
            which is formed by removing invalid triangles."""

        edge_counts = {}

        for t in invalid_triangles:
            for edge in t.edges:
                if edge not in edge_counts:
                    edge_counts[edge] = 1
                else:
                    edge_counts[edge] += 1

        # Find the edges that are not shared between multiple triangles
        polygonal_hole_edges = set()

        for edge, count in edge_counts.items():
            if count == 1:
                polygonal_hole_edges.add(edge)

        return polygonal_hole_edges

    def remove_invalid_triangles(self, invalid_triangles):
        """A method that removes invalid triangles from the triangulation."""

        valid_triangles = []

        for t in self.triangles:
            if t not in invalid_triangles:
                valid_triangles.append(t)

        self.triangles = valid_triangles

    def create_new_triangle(self, vertex, polygonal_hole_edges):
        """A method that forms new triangles by connecting the given vertex with the
            unshared edges of the polygonal hole and adds these triangles to the triangulation.

        This basically means filling the polygonal hole with new triangles."""

        # Connect vertex to the two endpoints of one polygonal edge
        for edge in polygonal_hole_edges:
            self.triangles.append(Triangle(vertex, edge.v1, edge.v2))

    def remove_super_triangle(self, super_triangle):
        """A method that removes triangles that share a vertex with the initial super triangle."""

        valid_triangles = []

        st1 = super_triangle.v1
        st2 = super_triangle.v2
        st3 = super_triangle.v3

        for t in self.triangles:
            if (st1 not in (t.v1, t.v2, t.v3) and
                st2 not in (t.v1, t.v2, t.v3) and
                st3 not in (t.v1, t.v2, t.v3)):
                valid_triangles.append(t)

        self.triangles = valid_triangles
