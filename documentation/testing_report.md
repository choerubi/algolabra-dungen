# Testing Report

## Coverage Report

The test coverage report can be viewed here:

[![codecov](https://codecov.io/gh/choerubi/algolabra-dungen/graph/badge.svg?token=BCVIGKRP59)](https://codecov.io/gh/choerubi/algolabra-dungen)

## Overview

The project is tested with unit tests. No dedicated integration testing is done, as the structure of the program forces the different components to work together: `bowyer_watson.py` uses the output of `rooms.py` as input, `prim.py` uses the output of `bowyer_watson.py` as input, etc. When the separate components are tested with comprehensive unit tests, it serves a similar purpose to integration testing, so adding dedicated integration testing would be a bit redundant in this project. User interface is manually tested in development.

## Unit Tests

Unit tests are implemented using the `unittest` library. Only appropriate methods and functions are tested. Unit tests are automated and integrated into the CI pipeline, which means they are executed with every remote repository push.

The project contains the following automated unit tests:

### `TestRoom`: 

- `test_room_stores_correct_values`: The test makes sure that the `Room` class stores the correct tile and pixel coordinates.
 
### `TestGenerateRooms`:

- `test_correct_number_of_rooms`: The test checks that the number of rooms generated is at most the number stored in `max_rooms`, which prevents infinite or excessive room generation. Note that the number of rooms can be smaller than the value stored in `max_rooms`, as it is not always possible to generate the desired number of rooms if the sizes of the rooms are set to be very large.

- `test_no_room_overlaps`: The test checks for all pairs of generated rooms that no rooms overlap with each other.

- `test_rooms_within_bounds`: The test makes sure that all generated rooms respect the dungeon margins and the grid boundaries.

### `TestEdge`:

- `test_edges_equal_with_reverse_order_vertices`: The test makes sure that undirected edges are handled correctly, i.e. that edges `Edge((0, 0), (1, 1))` and `Edge((1, 1), (0, 0))` are treated as the same edge.
 
### `TestTriangle`:

- `test_correct_circumcircle_calculated`: The test verifies that the circumcenter and circumradius calculations are correct. The test uses the Euclidean distance formula to calculate the distances from the circumcenter to each of the triangle vertices, and checks that all three distances are the same. Then, the test checks that the circumradius is the same as the three calculated distances.

- `test_no_circumcircle_when_determinant_zero`: The test makes sure that no circumcenter or circumradius exists for a degenerate triangle.

- `test_vertex_in_circumcircle`: The test verifies that whether a vertex is inside the circumcircle of a triangle or not is correctly calculated. The test also handles the case of a degenerate triangle, which has no circumcircle, and will thus return `False` for all inputs.

### `TestBowyerWatson`:

- `test_all_vertices_in_super_triangle`: The test makes sure that all vertices are contained inside the super triangle. The test uses the helper function `vertex_in_triangle`, which checks if a vertex is inside a triangle by checking if the vertex lies on the same side of each edge of the triangle. It does this by calculating the cross products for each pair of triangle edge vectors and vectors from the vertex to each triangle vertice, and checks that all cross products share the same sign.

- `test_invalid_triangles_detected`: The test verifies that the correct invalid triangles are detected by checking that all invalid triangles contain the given vertex in their circumcircle, and that no valid triangle contains the given vertex in their circumcircle.

- `test_polygonal_hole_edges_detected`: The test checks that the correct polygonal hole edges are detected by checking that only edges that appear exactly once, so edges that are not shared between multiple triangles, are counted as polygonal hole edges.

- `test_correct_triangles_removed`: The test makes sure that invalid triangles are not in the list of triangles after they have been removed.

- `test_polygonal_hole_filled`: The test checks that the correct amount of triangles has been added to fill the polygonal hole by checking that the amount of added triangles is the same as the amount of polygon edges.

- `test_super_triangle_removed`: The test checks that any triangle that shares a vertex with the super triangle is not in the list of triangles after the super triangle has been removed.

- `test_correct_number_of_triangles`: The test makes sure that the triangulation computes the correct number of triangles.

- `test_all_vertices_connected`: The test verifies that the graph produced by the Delaunay triangulation is connected, i.e. that every vertex can be reached from every vertex by following the edges of the triangulation.

### `TestPrim`:

- `test_prim_stores_correct_neighbors`: The test makes sure that the correct neighbors for each vertex are stored when building the dictionary of neighboring vertices.

- `test_mst_edges_are_triangulation_edges`: The test checks that all edges in the Minimum Spanning Tree are edges produced by the Delaunay triangulation, and no edges that are not in the original triangulation exist in the MST.

- `test_correct_number_of_mst_edges`: The test verifies that the number of computed MST edges is one less than the number of vertices.

- `test_vertices_not_explored_more_than_once`: The test checks that only edges that connect to unexplored vertices are added to the MST.

- `test_mst_with_one_vertex`: The test checks that the case where the MST is built from only one vertex is handled correctly, i.e. that the number of MST edges produced with only one vertex is zero.

- `test_all_vertices_connected`: Similarly to the test in `TestBowyerWatson`, the test verifies that the Minimum Spanning Tree is connected, i.e. that every vertex can be reached from every vertex by following the edges of the tree.

### `TestAddRandomEdges`:

- `test_correct_number_of_extra_edges`: The test checks that changing the chance value correctly affects the number of extra edges added.

### `TestAStar`:

- `test_path_from_start_to_goal_found`: The test verifies that a path is found between simple start and goal positions by checking that the start and goal positions match the first and last elements of the path.

- `test_start_and_goal_with_same_position`: The test makes sure that if the start position is the same as the goal position, there is no path to be computed, and the path consists of only the start position.

- `test_no_path_when_goal_out_of_reach`: The test checks that no path is found when the goal position is outside the tile map bounds.

- `test_correct_neighbors_for_edge_tile`: The test makes sure that the neighbors of edge tiles are computed correctly, i.e. that edge tiles do not have neighbors that are outside the tile map bounds.

- `test_correct_neighbors_for_corner_tile`: Similarly, the test makes sure that the neighbors of corner tiles are computed correctly, i.e. that corner tiles do not have neighbors that are outside the tile map bounds.

- `test_correct_tile_costs_returned`: The test verifies that the three different tile types and unknown tiles have the correct tile costs.

## How to Run the Tests

To run the tests locally, follow these steps:

1. Clone the repository:

```
git clone git@github.com:choerubi/algolabra-dungen.git
```

2. Navigate to the root directory of the project:

```
cd algolabra-dungen
```

3. Install the required dependencies:

```
poetry install
```

4. Activate the virtual environment:

```
poetry shell
```

5. Run the tests:

```
pytest src
```

6. View the coverage report:

```
coverage run --branch -m pytest src; coverage report -m
```
