# Testing Report

## Coverage Report

Test coverage can be tracked here:

[![codecov](https://codecov.io/gh/choerubi/algolabra-dungen/graph/badge.svg?token=BCVIGKRP59)](https://codecov.io/gh/choerubi/algolabra-dungen)

## How to Run the Tests

1 Clone the repository:

```
git clone git@github.com:choerubi/algolabra-dungen.git
```

2 Navigate to the root directory of the project:

```
cd algolabra-dungen
```

3 Install the required dependencies:

```
poetry install
```

4 Activate the virtual environment:

```
poetry shell
```

5 Run the tests:

```
pytest src
```

6 View the coverage report:

```
coverage run --branch -m pytest src; coverage report -m
```

## Unit Tests

The project contains the following unit tests:

### rooms.py

- `test_room_stores_correct_values`

- `test_rooms_within_bounds`

- `test_no_room_overlaps`

- `test_no_infinite_room_generation`
