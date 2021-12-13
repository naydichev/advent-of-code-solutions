#!/usr/bin/env python3

from collections import defaultdict


def main():
    points, folds = parse_input()


    grid = defaultdict(dict)

    for p in points:
        grid[p[1]][p[0]] = True

    grid = fold(grid, folds[0])

    total = 0
    for row in grid.values():
        total += sum(map(lambda x: 1, row.values()))


    print(f"There are {total} points")


def fold(grid, foldline):
    foldx = foldline[0] == "x"
    coord = foldline[1]

    g2 = defaultdict(dict)
    for y, row in grid.items():
        for x in row.keys():
            ny, nx = y, x
            if foldx:
                if x > coord:
                    nx = x - (2 * abs(x - coord))
            else:
                if y > coord:
                    ny = y - (2 * abs(y - coord))

            g2[ny][nx] = True

    return g2


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    points, folds = [], []
    for line in data:
        if line == "":
            continue
        elif "," in line:
            x, y = map(int, line.split(","))
            points.append((x, y))
        else:
            *_, part = line.split(" ")
            axis, coord = part.split("=")
            folds.append((axis, int(coord)))


    return points, folds


if __name__ == "__main__":
    main()
