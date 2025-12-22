import heapq

class Vertex:
    """A class to represent a vertex for the A* algorithm."""

    def __init__(self, position, parent, g, h):
        """A constructor that initializes the properties of the vertex.

        Args:
            position: Coordinates of the vertex.
            parent: Reference to the previous vertex.
            g: Cost from the start vertex to the current vertex.
            h: Estimated cost from the current vertex to the goal vertex.
        """

        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

class AStar:
    """A class that implements the A* algorithm to find the optimal path to the goal vertex."""

    def calculate_heuristic(self, v1, v2):
        """A method that calculates the estimated distance between the current vertex
            and the goal vertex to use as the heuristic value."""

        return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])

    def reconstruct_path(self, vertex):
        """A method that reconstructs the path from the goal vertex to the start vertex
            by following the parent references."""

        final_path = []

        while vertex:
            final_path.append(vertex.position)
            vertex = vertex.parent

        return reversed(final_path)

    def get_neighbors(self, vertex, tiles):
        """A method that gets all valid neighboring vertices of the given vertex."""

        neighbors = []

        for move_x, move_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x = move_x + vertex.position[0]
            new_y = move_y + vertex.position[1]

            if 0 <= new_x < len(tiles) and 0 <= new_y < len(tiles[0]):
                neighbors.append((new_x, new_y))

        return neighbors

    def get_tile_cost(self, tile_type):
        """A method that returns the cost of a tile."""

        if tile_type == 0:
            return 1
        if tile_type == 1:
            return 10
        if tile_type == 2:
            return 50

        return float("inf")

    def find_path(self, start_pos, goal_pos, tiles):
        """A method that finds the optimal path from the start vertex to the goal vertex."""

        start_vertex = Vertex(
            start_pos,
            None,
            0,
            self.calculate_heuristic(start_pos, goal_pos)
        )

        open_set = set()
        closed_set = set()

        open_queue = []
        best_g_score = {start_pos: 0}

        heapq.heappush(open_queue, start_vertex)
        open_set.add(start_pos)

        while open_queue:
            # Pop the vertex with the lowest total cost
            current_vertex = heapq.heappop(open_queue)

            if current_vertex.position == goal_pos:
                return self.reconstruct_path(current_vertex)

            closed_set.add(current_vertex.position)
            open_set.discard(current_vertex.position)

            # Loop through the neighbors of the vertex
            for neighbor_pos in self.get_neighbors(current_vertex, tiles):
                if neighbor_pos not in closed_set:

                    tile_type = tiles[neighbor_pos[0]][neighbor_pos[1]]
                    new_g_score = (
                        current_vertex.g
                        + self.calculate_heuristic(current_vertex.position, neighbor_pos)
                        + self.get_tile_cost(tile_type)
                    )
                    old_g_score = best_g_score.get(neighbor_pos, float("inf"))

                    # Update the path if a cheaper path to the neighbor is found
                    if new_g_score < old_g_score:
                        best_g_score[neighbor_pos] = new_g_score

                        new_vertex = Vertex(
                            neighbor_pos,
                            current_vertex,
                            new_g_score,
                            self.calculate_heuristic(neighbor_pos, goal_pos)
                        )

                        heapq.heappush(open_queue, new_vertex)
                        open_set.add(neighbor_pos)

        return None
