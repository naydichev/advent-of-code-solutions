#!/usr/bin/env python3

TREE = '#'
OPEN = '.'


def main():
    with open("trees.pi") as f:
        world = build_world(f.readlines())

    bottom = len(world)
    x, y = 0, 0
    trees_encountered = 0

    while y < bottom - 1:
        x += 3
        y += 1

        if object_at_coordinate(x, y, world) == TREE:
            trees_encountered += 1

    print(f"{trees_encountered} trees encountered")


def object_at_coordinate(x, y, world):
    row = world[y]
    actual_x = x % len(row)

    return row[actual_x]


def build_world(raw):
    return [y.strip() for y in raw]


if __name__ == "__main__":
    main()
