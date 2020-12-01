#!/usr/bin/env python3

from collections import defaultdict, namedtuple

Point = namedtuple("Point", "x, y")

BUG = "#"
EMPTY = "."
MAX_X = None
MAX_Y = None
D = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def main(raw):
    grid = parse(raw)
    history = set()

    while to_history(grid) not in history:
        history.add(to_history(grid))
        grid = time_passes(grid)

    biodiversity_rating = calculate_biodiversity(grid)
    print(f"the thingy {biodiversity_rating}")


def time_passes(grid):
    max_x, max_y = get_maxes(grid)

    new_grid = defaultdict(lambda: EMPTY)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            self = Point(x, y)
            bugs = sum([1 if grid[Point(nx + x, ny + y)] == BUG else 0 for nx, ny in D])
            identity = grid[Point(x, y)] == BUG

            if identity and bugs == 1:
                new_grid[self] = BUG
            elif not identity and (bugs == 1 or bugs == 2):
                new_grid[self] = BUG
            else:
                new_grid[self] = EMPTY

    return new_grid


def get_maxes(grid):
    global MAX_X, MAX_Y

    if MAX_X is None or MAX_Y is None:
        MAX_X = max([p.x for p in grid.keys()])
        MAX_Y = max([p.y for p in grid.keys()])

    return MAX_X, MAX_Y


def calculate_biodiversity(grid):
    max_x, max_y = get_maxes(grid)
    i = 1

    total = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if grid[Point(x, y)] == BUG:
                total += i

            i *= 2

    return total


def to_history(grid):
    max_x, max_y = get_maxes(grid)

    line = []
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            line.append(grid[Point(x, y)])

    return "".join(line)

def parse(raw):
    grid = defaultdict(lambda: EMPTY)

    for y, line in enumerate(raw):
        for x, c in enumerate(line):
            grid[Point(x, y)] = c

    return grid


if __name__ == "__main__":
    with open("bugs.pi") as f:
        main(f.read().strip().split("\n"))
