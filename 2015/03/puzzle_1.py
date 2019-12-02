#!/usr/bin/env python3

from collections import defaultdict


def main(data):
    houses = defaultdict(lambda: 0)

    x, y = 0, 0
    key = lambda x, y: f"{x},{y}"

    houses[key(x, y)] = 1

    for house in data:
        if house == "^":
            y += 1
        elif house == "v":
            y -= 1
        elif house == "<":
            x -= 1
        elif house == ">":
            x += 1

        houses[key(x, y)] += 1

    print(len(houses))

if __name__ == "__main__":
    with open("input.pi") as f:
        line = f.read().rstrip()

        main(line)
