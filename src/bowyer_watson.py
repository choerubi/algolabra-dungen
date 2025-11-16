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
        self.circumradius = None
        self.calculate_circumcircle()

    def calculate_circumcircle(self):
        """A method that calculates the circumcenter and circumradius of the triangle."""

    def vertex_in_circumcircle(self, vertex: Tuple):
        """A method that checks whether a vertex is inside the circumcircle."""

class BowyerWatson:
    pass
