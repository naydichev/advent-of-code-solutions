#!/usr/bin/python

from collections import defaultdict

OPEN = "."
TREES = "|"
LUMBERYARD = "#"

def main():
    # with open("sample.pi") as f:
    with open("wood.pi") as f:
        raw = f.read().split("\n")

    forest = parse(raw)

    hashes = defaultdict(int)
    period = None
    period_hash = None
    period_start = None
    n = 1000000000
    for i in xrange(1, n + 1):
        print("{} ticks".format(i))
        forest = tick(forest)

        forest_str = "".join(["".join(row.values()) for row in forest.values()])

        if forest_str == period_hash:
            cycle_start = i - len(period)
            cycle_end = i
            assert len(period) == cycle_end - cycle_start
            delta = n - cycle_start
            x = (cycle_start + delta) % len(period)
            print(resource_value(period[x]))
            print("the period is {}".format(len(period)))
            return

        if period_start is not None:
            period.append(forest_str)

        hashes[forest_str] += 1

        if hashes[forest_str] > 3:
            print("period found")
            if not period_hash:
                period_start = i
                period_hash = forest_str
                period = [forest_str]

    print_forest(forest)
    print(resource_value(forest))

def tick(forest):
    new_forest = defaultdict(dict)

    for y in sorted(forest.keys()):
        for x in sorted(forest[y].keys()):
            adjacent = get_adjacent(forest, y, x)

            new_forest[y][x] = forest[y][x]

            if forest[y][x] == OPEN:
                if len(filter(lambda x: x == TREES, adjacent)) >= 3:
                    new_forest[y][x] = TREES
            elif forest[y][x] == TREES:
                if len(filter(lambda x: x == LUMBERYARD, adjacent)) >= 3:
                    new_forest[y][x] = LUMBERYARD
            elif forest[y][x] == LUMBERYARD:
                if len(filter(lambda x: x == LUMBERYARD, adjacent)) < 1 or len(filter(lambda x: x == TREES, adjacent)) < 1:
                    new_forest[y][x] = OPEN
    return new_forest

def get_adjacent(forest, y, x):
    adjacent = []
    for y_diff in range(-1, +2):
        for x_diff in range(-1, +2):
            new_y = y + y_diff
            new_x = x + x_diff

            if new_y == y and new_x == x:
                continue

            if new_y in forest and new_x in forest[new_y]:
                adjacent.append(forest[new_y][new_x])

    return adjacent

def resource_value(forest):
    trees = 0
    lumberyard = 0
    for c in forest:
        if c == TREES:
            trees += 1
        elif c == LUMBERYARD:
            lumberyard += 1

    return trees * lumberyard

def parse(raw):
    grid = defaultdict(dict)
    for y, row in enumerate(raw):
        for x, c in enumerate(row):
            grid[y][x] = c

    return grid

def print_forest(forest):
    for y in sorted(forest.keys()):
        row = []
        for x in sorted(forest[y].keys()):
            row.append(forest[y][x])
        print("".join(row))

if __name__ == "__main__":
    main()
