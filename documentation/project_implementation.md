# Project Implementation

## Program Functionality and Structure

The five steps of generating a dungeon are as follows:

1. **Room generation**: Generate rooms with random sizes and positions, with *min room size*, *max room size*, and *room amount* read from user input. The rooms must not overlap with any other rooms, and a margin must be left around each room.
2. **Delaunay triangulation**: Create a Delaunay triangulation using the centers of the rooms as the triangulation vertices. This is done using the **Bowyer-Watson algorithm**.
3. **Minimum Spanning Tree**: Create a Minimum Spanning Tree (MST) from the triangulation edges. This is done using **Prim's algorithm**.
4. **Extra edges**: Add random edges from the triangulation edges to the MST edges to introduce cycles to the dungeon.
5. **Final paths**: Find paths between the rooms according to the MST edges and added extra edges. This is done using the **A\* algorithm**.

The code for room generation can be found in `rooms.py`. The code for computing the Delaunay triangulation can be found in `bowyer_watson.py`. The code for computing the MST and adding the extra edges can be found in `prim.py`, and the code for computing the final paths between the rooms can be found in `a_star.py`.

When the program is run, the user is presented with a *Generate* button, which, when pressed, opens a popup window for configuring the dungeon. The user can set values for *min room size*, *max room size*, and *room amount*. The values of *min room size* and *max room size* must be in the range 3-10, and the value of *min room size* must be smaller than the value of *max room size*. The value of *room amount* must be in the range 3-15. If the user sets an invalid value, the input box turns red to let the user know that the input is invalid. Once all three inputs are valid, the *Done* button can be pressed to generate the dungeon.

When the *Done* button is pressed, the user is presented with the first step of the dungeon generation process. There are five different views, each visualizing one step of the generation process. The user can switch between these views with the arrow buttons. After this, the user can either press the *Generate* button to generate another dungeon, or press the *Exit* button to exit the program.

## Algorithm Time Complexities

### Estimated Time Complexities:

- **Bowyer-Watson algorithm**: `O(n log n)` or `O(n^2)` ([source](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm))
- **Prim's algorithm**: `O(E log V)` ([source](https://en.wikipedia.org/wiki/Prim%27s_algorithm))
- **A\* algorithm**: `O(E log V)` ([source](https://en.wikipedia.org/wiki/A*_search_algorithm))

### Achieved Time Complexities:

- **Bowyer-Watson algorithm**:
  - First, the algorithm finds the invalid triangles from the list of triangles. This step iterates over all existing triangles, which means that the time complexity of this step is `O(|Triangles|) = O(n)`, where `n` is the number of vertices.
  - Next, the algorithm finds the polygonal hole edges. This step iterates over the invalid triangles, which means that the time complexity of this step is `O(|Invalid triangles|)`. However, the number of invalid triangles is always less than or equal to the number of all triangles, so this step does not contribute to the overall time complexity.
  - Next, the algorithm removes the invalid triangles from the list of triangles. This step, once again, iterates over all existing triangles, which means that the time complexity of this step is `O(|Triangles|) = O(n)`, where `n` is the number of vertices.
  - So, because the `O(n)` steps are repeated for all `n` inserted vertices, the total achieved time complexity is `O(n^2)`.

- **Prim's algorithm**:
  - First, the algorithm adds all vertices to the set of vertices and builds a dictionary of neighboring vertices. Both these steps iterate over all edges, which means that the time complexity of these steps is `O(E)`, where `E` is the number of edges.
  - Next, the algorithm computes the MST. The algorithm computes a total of `O(E)` `heappush` operations, with each operation having a cost of `O(log k)`, where `k` is the size of the heap. The size of the heap is the number of vertices, so the cost of each operation is `O(log V)`. So, the total cost of all `heappush` operations is `O(E log V)`. Similarly, the algorithm computes a total of `O(E)` `heappop` operations, with each operation having a cost of `O(log V)`. So, the total cost of all `heappop` operations is `O(E log V)`.
  - So, the total achieved time complexity is `O(E log V)`.

- **A\* algorithm**:
  - The algorithm computes the paths by computing at most `V` `heappop` operations on each iteration, with each operation having a cost of `O(log k)`, where `k` is the size of the heap. The size of the heap is the number of vertices, so the cost is `O(log V)`. So, the total cost of all `heappop` operations is `O(V log V)`. Similarly, the algorithm computes at most `E` `heappush` operations for each neighbor on each iteration, with each operation having a cost of `O(log V)`. So, the total cost of all `heappush` operations is `O(E log V)`.
  - So, because `E log V` is a larger term than `V log V`, the total achieved time complexity is `O(E log V)`.

So, all algorithms have the expected time complexities.

## Possible Improvements

I am pretty happy with the end result, so I do not have that many ideas for improvement. One idea I had, that I did not have time to implement, was animating the different steps of the dungeon generation process. For example, for the Delaunay triangulation, the user could have seen how the super triangle got drawn, how the circumcircles got computed, and which triangles got marked as invalid and removed, etc. However, this would have taken far too much time, especially since animating with Pygame is not something I have done before, so it is a fun idea for possible further development! Also, to improve readability, I could have added more type hints.

## Use of Large Language Models

I used ChatGPT (GPT-4.1) mostly to help with debugging. I also used it to help with Git problems, as I made a complete mess out of my local and remote repositories a few times. Also, I used it to ask if I was on the right track when I was unsure of my progress, and I used it to get examples of Pygame-related concepts, such as coding the popup window and drawing the wall tiles.

## Sources

I used the following sources in the project:

- [Vazgriz.com: Procedurally Generated Dungeons](https://vazgriz.com/119/procedurally-generated-dungeons/) (Dungeon generation steps)
- [Gorillasun.de: Bowyer-Watson Algorithm for Delaunay Triangulation](https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/) (Illustration of Bowyer-Watson steps)
- [Wikipedia: Circumcircle](https://en.wikipedia.org/wiki/Circumcircle) (Circumcenter and circumradius calculation)
- [GeeksForGeeks: Circumcenter of Triangle: Formula, Properties, Examples](https://www.geeksforgeeks.org/maths/circumcenter-of-triangle/) (Circumcircle definition and properties)
- [Baeldung.com: How To Determine if a Point Is in a 2D Triangle](https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle) (Checking if a vertex is inside a triangle)
- [Wikipedia: Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) (Euclidean distance calculation)
- [Wikipedia: Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm) (Prim's algorithm implementation)
- [Datacamp.com: The A* Algorithm: A Complete Guide](https://www.datacamp.com/tutorial/a-star-algorithm?dc_referrer=https%3A%2F%2Fwww.google.com%2F) (A* algorithm implementation)
- [Medium.com: Easy A* (star) Pathfinding](https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2) (A* algorithm implementation)
- [GeeksForGeeks: Manhattan Distance](https://www.geeksforgeeks.org/data-science/manhattan-distance/) (Manhattan distance calculation)
- [Stackoverflow.com: How can I create a text input box with Pygame?](https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame) (Creating an input box with Pygame)
- [Stackexchange.com: Minimum number of triangles in triangulation of points in general position](https://math.stackexchange.com/questions/2081451/minimum-number-of-triangles-in-triangulation-of-points-in-general-position) (Calculating the amount of triangles in a triangulation)
