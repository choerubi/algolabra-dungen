# Testing Report

## Unit Tests

The project contains the following automated unit tests:

### For `rooms.py`

- `test_room_stores_correct_values`: The test makes sure that the `Room` class stores the correct tile and pixel coordinates.

- `test_rooms_within_bounds`: The test makes sure that all generated rooms respect the dungeon margins and the grid boundaries.

- `test_no_room_overlaps`: The test checks for all pairs of generated rooms that no rooms overlap with each other.

- `test_no_infinite_room_generation`: The test checks that the number of rooms generated is at most the number stored in `max_rooms`, which prevents infinite or excessive room generation.

### For `bowyer-watson.py`

- Todo

## Coverage Report

The test coverage can be viewed here:

[![codecov](https://codecov.io/gh/choerubi/algolabra-dungen/graph/badge.svg?token=BCVIGKRP59)](https://codecov.io/gh/choerubi/algolabra-dungen)

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
