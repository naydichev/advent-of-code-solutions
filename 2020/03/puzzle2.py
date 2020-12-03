#!/usr/bin/env python3

TREE = '#'
OPEN = '.'


def main():
    with open("trees.pi") as f:
        world = build_world(f.readlines())

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    trees_encountered = multiply([calculate_trees_at_slope(world, *slope) for slope in slopes])

    print(f"{trees_encountered} trees encountered")


def multiply(digits):
    start = digits.pop()

    for digit in digits:
        start *= digit

    return start


def calculate_trees_at_slope(world, xdiff, ydiff):
    bottom = len(world)
    x, y = 0, 0
    trees_encountered = 0

    while True:
        x += xdiff
        y += ydiff

        if y >= bottom:
            break

        if object_at_coordinate(x, y, world) == TREE:
            trees_encountered += 1

    return trees_encountered


def object_at_coordinate(x, y, world):
    row = world[y]
    actual_x = x % len(row)

    return row[actual_x]


def build_world(raw):
    return [y.strip() for y in raw]


if __name__ == "__main__":
    main()
