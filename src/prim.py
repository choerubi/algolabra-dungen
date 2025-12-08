import math
import heapq
import random
import pygame
from bowyer_watson import Edge
from config import TILE_SIZE

class Prim:
    """A class that implements Prim's algorithm to create a Minimum Spanning Tree."""

    def __init__(self):
        """A constructor that initializes an empty set and dictionary to store vertices
            created by the Delaunay triangulation."""

        self.vertices = set()
        self.neighbors = {}

    def get_vertices(self, triangles):
        """A method that builds a set of all vertices and a dictionary of neighboring vertices."""

        self.vertices.clear()
        self.neighbors.clear()

        for triangle in triangles:
            for edge in triangle.edges:
                self.vertices.add(edge.v1)
                self.vertices.add(edge.v2)

        for vertex in self.vertices:
            self.neighbors[vertex] = set()

        for triangle in triangles:
            for edge in triangle.edges:
                self.neighbors[edge.v1].add(edge.v2)
                self.neighbors[edge.v2].add(edge.v1)

    def calculate_weight(self, v1, v2):
        """A method that calculates the distance between two vertices to use as a weight
            in the Minimum Spanning Tree."""

        return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)

    def create_mst(self):
        """A method that creates the Minimum Spanning Tree."""

        # Choose a random starting vertex
        start_vertex = random.choice(list(self.vertices))

        explored_vertices = set()
        unexplored_vertices = set(self.vertices)

        explored_vertices.add(start_vertex)
        unexplored_vertices.remove(start_vertex)

        possible_edges = []
        heapq.heapify(possible_edges)

        # Start by adding the edges to the neighbors of the starting vertex
        # to the priority queue of possible edges
        for neighbor in self.neighbors[start_vertex]:
            weight = self.calculate_weight(start_vertex, neighbor)
            heapq.heappush(possible_edges, (weight, start_vertex, neighbor))

        mst_edges = set()

        while possible_edges and unexplored_vertices:
            # Pop the shortest edge from possible edges
            weight, prev_vertex, next_vertex = heapq.heappop(possible_edges)

            if next_vertex not in explored_vertices:
                # Add the edge to the final MST edges if it connects to an unexplored vertex
                mst_edges.add(Edge(prev_vertex, next_vertex))

                # Remove the vertex from the vertices to be explored
                explored_vertices.add(next_vertex)
                unexplored_vertices.discard(next_vertex)

                # Add the edges to the unexplored neighbors of the new vertex
                # to the priority queue of possible edges
                for neighbor in self.neighbors[next_vertex]:
                    if neighbor not in explored_vertices:
                        weight = self.calculate_weight(next_vertex, neighbor)
                        heapq.heappush(possible_edges, (weight, next_vertex, neighbor))

        return mst_edges

def edge_collides_with_room(edge, rooms):
    """A function that checks if the extra edge about to be added collides with any room
        other than the rooms that contain the endpoints of the edge."""

    room_rects = []

    ax, ay = edge.v1
    bx, by = edge.v2

    for room in rooms:
        room_rect = pygame.Rect(
            room.tile_x * TILE_SIZE,
            room.tile_y * TILE_SIZE,
            room.tile_width * TILE_SIZE,
            room.tile_height * TILE_SIZE
        )
        if not room_rect.collidepoint((ax, ay)):
            if not room_rect.collidepoint((bx, by)):
                room_rects.append(room_rect)

    for room_rect in room_rects:
        if room_rect.clipline((ax, ay), (bx, by)):
            return True

    return False

def add_random_edges(chance, mst_edges, triangles, rooms):
    """A function that adds random extra edges from the triangulation to the set of edges
        to introduce cycles to the dungeon."""

    bw_edges = set()
    extra_edges = set()

    for triangle in triangles:
        for edge in triangle.edges:
            if edge not in mst_edges:
                bw_edges.add(edge)

    for edge in bw_edges:
        if edge_collides_with_room(edge, rooms) is False:
            if random.randint(1, 100) <= chance:
                extra_edges.add(edge)

    return extra_edges
