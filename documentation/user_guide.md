# User Guide

## How to Run the Program

To run the program locally, follow these steps:

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

4. Run the program:

```
python3 src/index.py
```

## How to Use the Program

When the program is run, the user is presented with a *Generate* button, which, when pressed, opens a popup window for configuring the dungeon. The user can set values for *min room size*, *max room size*, and *room amount*. The values of *min room size* and *max room size* must be in the range 3-10, and the value of *min room size* must be smaller than the value of *max room size*. The value of *room amount* must be in the range 3-15. If the user sets an invalid value, the input box turns red to let the user know that the input is invalid. Once all three inputs are valid, the *Done* button can be pressed to generate the dungeon.

When the *Done* button is pressed, the user is presented with the first step of the dungeon generation process. There are five different views, each visualizing one step of the generation process. The user can switch between these views with the arrow buttons. After this, the user can either press the *Generate* button to generate another dungeon, or press the *Exit* button to exit the program.

Below is an example run of the program:

![example_01](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_01.png)
![example_02](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_02.png)
![example_03](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_03.png)
![example_04](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_04.png)
![example_05](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_05.png)
![example_06](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_06.png)
![example_07](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_07.png)
![example_08](https://github.com/choerubi/algolabra-dungen/blob/main/documentation/images/example_08.png)
