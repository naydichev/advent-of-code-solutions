#!/usr/bin/env python3

from collections import defaultdict, namedtuple

Point = namedtuple("Point", "x, y")

BUG = "#"
GRID = "?"
EMPTY = "."
MAX_X = 5
MAX_Y = 5
D = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def main(raw):
    grids = [parse(raw)]

    for _ in range(200):
        print(_)
        grid = time_passes(grids)

    num_bugs = sum([sum([1 if v == BUG else 0 for v in g.values()]) for g in grids])


def time_passes(grids):
    # each minute, a new grid forms
    grids.append(defaultdict(lambda: EMPTY))
    grids.insert(0, defaultdict(lambda: EMPTY))
    new_grids = []

    for g in range(len(grids)):
    for grid in reversed(grids):
        print(grid)

    return grids
    for y in range(MAX_Y + 1):
        for x in range(MAX_X + 1):
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


def parse(raw):
    grid = defaultdict(lambda: EMPTY)

    for y, line in enumerate(raw):
        for x, c in enumerate(line):
            grid[Point(x, y)] = c

    grid[Point(2,2)] = GRID
    return grid


if __name__ == "__main__":
    with open("bugs.pi") as f:
        main(f.read().strip().split("\n"))
