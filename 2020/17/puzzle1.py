#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from copy import deepcopy

ACTIVE= "#"
INACTIVE = "."

Diff = namedtuple("Diff", "x, y, z")


def main():
    with open("cubes.pi") as f:
        world = parse(f.readlines())

    diffs = generate_diffs()

    for i in range(6):
        active = 0
        iterworld = deepcopy(world)

        zkey = world.keys()
        minz = min(zkey)
        maxz = max(zkey)

        ykey = world[minz].keys()
        miny = min(ykey)
        maxy = max(ykey)

        xkey = world[minz][miny].keys()
        minx = min(xkey)
        maxx = max(xkey)

        for z in range(minz - 1, maxz + 2):
            for y in range(miny - 1, maxy + 2):
                for x in range(minx - 1, maxx + 2):
                    # for each coordinate, figure out all of it's neighbors
                    state = world[z][y][x]
                    num_active = sum([1 if world[z + d.z][y + d.y][x + d.x] == ACTIVE else 0 for d in diffs])

                    if state == ACTIVE and (num_active < 2 or num_active > 3):
                        state = INACTIVE
                    elif state == INACTIVE and (num_active == 3):
                        state = ACTIVE

                    iterworld[z][y][x] = state
                    if state == ACTIVE:
                        active += 1

        world = iterworld

    print(f"after six cycles {active} cubes are active")


def generate_diffs():
    diffs = []

    for z in range(-1, 2):
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0 and z == 0:
                    continue

                diffs.append(Diff(x, y, z))

    return diffs


def parse(raw):
    world = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: INACTIVE)))

    z = 0
    for y, line in enumerate(raw):
        for x, char in enumerate(line.strip()):
            world[z][y][x] = char

    return world


if __name__ == "__main__":
    main()
