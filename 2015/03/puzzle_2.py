#!/usr/bin/env python3

from collections import defaultdict


def main(data):
    houses = defaultdict(lambda: 0)

    sx, sy = 0, 0
    rx, ry = 0, 0
    key = lambda x, y: f"{x},{y}"

    houses[key(sx, sy)] = 2
    i = 0

    for house in data:
        if i % 2 == 0:
            x, y = sx, sy
        else:
            x, y = rx, ry

        if house == "^":
            y += 1
        elif house == "v":
            y -= 1
        elif house == "<":
            x -= 1
        elif house == ">":
            x += 1

        if i % 2 == 0:
            sx, sy = x, y
        else:
            rx, ry = x, y

        i += 1
        houses[key(x, y)] += 1

    print(len(houses))

if __name__ == "__main__":
    with open("input.pi") as f:
        line = f.read().rstrip()

        main(line)
