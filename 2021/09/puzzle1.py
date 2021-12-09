#!/usr/bin/env python3

from collections import defaultdict


def main():
    data = parse_input()

    lowest = []
    ymax = len(data)
    xmax = len(data[0])
    for y in range(ymax):
        for x in range(xmax):
            value = data[y][x]
            adjacent = [data[y - 1][x], data[y + 1][x], data[y][x - 1], data[y][x + 1]]
            if all([value < v for v in adjacent]):
                lowest.append(value)

    print(f"The thing is {sum(lowest) + len(lowest)}")


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    heights = defaultdict(lambda: defaultdict(lambda: 10))
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            heights[y][x] = int(value)

    return heights


if __name__ == "__main__":
    main()
