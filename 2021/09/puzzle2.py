#!/usr/bin/env python3

from collections import defaultdict, deque


def main():
    data = parse_input()

    basins = sorted(find_basins(data))
    total = basins[-1] * basins[-2] * basins[-3]

    print(f"The thing is {total}")


def find_basins(data):
    basins = []
    ymax = len(data)
    xmax = len(data[0])

    for y in range(ymax):
        for x in range(xmax):
            if data[y][x] not in "-*":
                basins.append(find_basin_size(data, y, x))

    for y in range(ymax):
        row = []
        for x in range(xmax):
            row.append(data[y][x])

        print("".join(row))

    print(basins)
    return basins


def find_basin_size(data, y, x):
    queue = deque([(y, x)])

    size = 0

    while queue:
        ny, nx = queue.popleft()
        size += 1

        for dy, dx in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            nny = ny + dy
            nnx = nx + dx

            if data[nny][nnx] in "-*":
                continue

            data[nny][nnx] = "*"
            queue.append((nny, nnx))

    return size - 1


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    heights = defaultdict(lambda: defaultdict(lambda: "-"))
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value == "9":
                value = "-"
            heights[y][x] = value

    return heights


if __name__ == "__main__":
    main()
