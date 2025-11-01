# Project Specification

Degree programme: *Bachelor's Programme in Computer Science* (CS).

This project is a configurable dungeon generator for generating procedural 2D dungeon layouts. The project is built with python using pygame.

## Program Functionality and Interface

The interface of the program is relatively simple. The user is presented with a *generate* button, which when pressed will display either a series of images or an animation showing the different stages of the generation process. The steps of generating a dungeon are as follows:

- Generate the rooms. The sizes, placements, and overall arrangement of the rooms are random, but the rooms must not overlap, and a hallway-wide buffer must be left around each room.
- Create a Delaunay triangulation graph of the rooms using the **Bowyer-Watson algorithm**.
- Create a Minimum Spanning Tree from the triangulation graph using **Prim's algorithm**.
- Create a list of the hallways (MST) and add random edges from the triangulation graph to the list, creating cycles to the hallways.
- Find a path from the start of each hallway to the end using the **A\* algorithm**.

The program does not need any user input to run, but I plan on making it configurable by adding (at least) the option to choose the number of rooms generated. Without user input the number of rooms generated is random.

The core topic of the project is the Bowyer-Watson algorithm.

## Algorithm Time Complexities

- Bowyer-Watson algorithm: O(n log n) ([source](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm))
- Prim's algorithm: O(E log V) ([source](https://en.wikipedia.org/wiki/Prim%27s_algorithm))
- A* algorithm: O(E log V) = O($b^d$) ([source](https://en.wikipedia.org/wiki/A*_search_algorithm))

## Documentation

All code and documentation will be written in English. I would prefer to only peer review projects written in python, as my skills in other languages are not very developed, so I am not able to provide in-depth feedback.

## Sources

I plan on using at least the following sources:

- [Procedurally Generated Dungeons](https://vazgriz.com/119/procedurally-generated-dungeons/)
- [Bowyer-Watson algorithm](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm)
