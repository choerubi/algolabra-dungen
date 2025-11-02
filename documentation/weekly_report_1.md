# Weekly Report #1

This week, I spent a total of **10** hours on the project. The workload revolved mostly around reading posts about procedurally generated dungeons, studying the algorithms, and exploring different websites and forums regarding the plethora of all kinds of questions that arose as the planning progressed. I had to spend a lot of time studying the algorithms used in the project, as the Bowyer-Watson algorithm is completely new to me, and as I had largely forgotten the algorithms covered in *Data Structures and Algorithms*. I went back to the course page to refresh my memory of Kruskal's and Dijkstra's algorithms, as they are similar to Prim's algorithm and the A* algorithm, and can thus help me get started with them. Picking the topic was not difficult at all, as dungeon generation was easily the most fascinating topic for me!

I was debating whether I should use Binary Space Partitioning for generating the rooms, but I decided against it, as I was worried it might complicate the project too much. Instead, my current plan is to use a random generation method that generates rooms with random sizes and positions, with a hallway-wide buffer on each side, and rejects overlapping rooms. I was also struggling to decide between Kruskal's and Prim's algorithm, but based on my research, Prim's algorithm is more efficient on sparse graphs, and the Delaunay triangulation graphs used in the project seem to be fairly sparse, as they always have more edges than vertices, so I landed on Prim's.

Aside from adding poetry and pylint to the project, I did not get to do any actual hands-on work yet, as the planning and researching took a decent amount of time over multiple days. I had to go do some studying on the *Ohjelmistotuotanto* and *Ohjelmistotekniikka* course pages, as it has been a while since my last git project, and some basics had slipped my mind. Next, I will start working on the room generation, and I hopefully will get to the Bowyer-Watson algorithm next week as well. Currently, I do not have anything that is unclear to me.

## Hours Spent

- Mon 27.10. **2h**
  - Exploring potential topics and reading the course instructions
  - Researching dungeon generation and the algorithms
- Tue 28.10. **3h**
  - Researching the algorithms
  - Planning and illustrating the different steps of the project
  - Planning a rough outline of the project
- Thu 30.10. **1h**
  - Planning the different stages of the project
  - Exploring some example projects
- Fri 31.10. **1h**
  - Creating the repository and registering in Labtool
- Sat 1.11. **3h**
  - Doing some initializing and project management
  - Writing the project specification
  - Writing the weekly report
