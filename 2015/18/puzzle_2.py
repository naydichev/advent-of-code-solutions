#!/usr/bin/env python3

import itertools

def main(lights, steps):
    print_lights(lights)

    for i in range(steps):
        lights = animate(lights)
        print_lights(lights)

    lights_on = sum(itertools.chain.from_iterable(lights))
    print(f"there are {lights_on} lights on")


def print_lights(lights):
    for y in lights:
        line = []
        for x in y:
            if x == 1:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))
    print()


def animate(lights):
    new_lights = []

    for y in range(len(lights)):
        line = []
        for x in range(len(lights[y])):
            if is_corner(lights, x, y):
                line.append(1)
                continue

            on_neighbors = sum(get_neighbors(lights, x, y))

            if (lights[y][x] == 0 and on_neighbors == 3) or (lights[y][x] == 1 and on_neighbors in [2, 3]):
                line.append(1)
            else:
                line.append(0)

        new_lights.append(line)

    return new_lights


def is_corner(lights, x, y):
    if (x == 0 and y == 0) or \
       (x == 0 and y == len(lights) - 1) or \
       (y == 0 and x == len(lights[y]) - 1) or \
       (y == len(lights) - 1 and x == len(lights[y]) - 1):
           return True
    return False


SURROUNDING = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]


def get_neighbors(lights, x, y):
    surrounding = []

    for s in SURROUNDING:
        nx = x + s[0]
        ny = y + s[1]

        if nx < 0 or ny < 0 or ny >= len(lights) or nx >= len(lights[ny]):
            surrounding.append(0)
        else:
            surrounding.append(lights[ny][nx])

    return surrounding


if __name__ == "__main__":
    with open("lights.pi") as f:
        main([[1 if x == "#" else 0 for x in line] for line in f.read().strip().split("\n")], 100)
