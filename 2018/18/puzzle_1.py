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

    for i in range(10):
        print("{} ticks".format(i))
        print_forest(forest)
        forest = tick(forest)

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
    for y in forest.keys():
        for x in sorted(forest[y].keys()):
            if forest[y][x] == TREES:
                trees += 1
            elif forest[y][x] == LUMBERYARD:
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
