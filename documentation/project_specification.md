# Project Specification

Degree programme: *Bachelor's Programme in Computer Science (CS)*.

This project is a configurable dungeon generator for creating procedural 2D dungeon layouts. The project is built with python using pygame.

## Program Functionality and Interface

The interface of the program is relatively simple. The user is presented with a *generate* button, which, when pressed, displays either a series of images or an animation (not yet decided) showing the different stages of the generation process.

The steps of generating a dungeon are as follows:

- Generate the rooms. The sizes, placements, and overall arrangement of the rooms are random, but the rooms must not overlap, and a hallway-wide buffer must be left around each room.
- Create a Delaunay triangulation of the rooms using the **Bowyer-Watson algorithm**.
- Create a Minimum Spanning Tree (MST) from the triangulation graph using **Prim's algorithm**.
- Create a list of hallways from the MST, and add random edges from the triangulation graph to the list to introduce cycles into the layout.
- Find paths from the start to the end of each hallway using the **A\* algorithm**.

The program does not require any user input to run, but I plan on making it configurable by adding (at least) the option to select the number of rooms to generate. Without user input, the number of rooms generated will be random.

The core focus of the project is the Bowyer-Watson algorithm.

## Algorithm Time Complexities

The time complexities for the algorithms used in the project are as follows:

- Bowyer-Watson algorithm: *O(n log n)* ([source](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm))
- Prim's algorithm: *O(E log V)* ([source](https://en.wikipedia.org/wiki/Prim%27s_algorithm))
- A* algorithm: *O(E log V)*, also written as *O(b^d)* ([source](https://en.wikipedia.org/wiki/A*_search_algorithm))

## Language

All code and documentation will be written in English. I would prefer to only peer review projects written in python, as my skills in other languages are not very advanced, so I would not be able to provide in-depth feedback.

## Sources

I plan on using at least the following sources:

- [Vazgriz.com: Procedurally Generated Dungeons](https://vazgriz.com/119/procedurally-generated-dungeons/)
- [Wikipedia: Bowyer-Watson algorithm](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm)
- [Wikipedia: Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Wikipedia: A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
