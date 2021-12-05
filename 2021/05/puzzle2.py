#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from itertools import zip_longest


Point = namedtuple("Point", "x, y")
Line = namedtuple("Line", "start, end")


def main():
    data = parse_input()

    coords = defaultdict(int)

    for line in data:
        points = calculate_points(line)

        for point in points:
            coords[point] += 1

    # print_map(coords)

    total = sum(map(lambda x: 1 if x > 1 else 0, coords.values()))

    print(f"The total is {total}")


def print_map(coords):
    points = sorted(coords.keys(), key=lambda p: [p.x, p.y])
    width = max(points, key=lambda p: p.x).x
    height = max(points, key=lambda p: p.y).y

    print(f"grid from (0, 0) -> ({width}, {height})")

    for y in range(height + 1):
        for x in range(width + 1):
            p = Point(x, y)
            num = coords[p]

            if num < 1:
                print(".", end="")
            else:
                print(num, end="")

        print()


def calculate_points(line):
    sx, sy = line.start.x, line.start.y
    ex, ey = line.end.x, line.end.y

    xstep = 1
    ystep = 1

    if ex - sx < 0:
        xstep = -1
    if ey - sy < 0:
        ystep = -1

    deltas = zip_longest(range(abs(sx - ex) + 1), range(abs(sy - ey) + 1), fillvalue=0)

    points = []
    for dx, dy in deltas:
        x = sx + (dx * xstep)
        y = sy + (dy * ystep)
        points.append(Point(x, y))

    # print(f"line {l(line)} has points {[p(x) for x in points]}")

    return points


def p(point):
    return (point.x, point.y)


def l(line):
    return f"{p(line.start)} -> {p(line.end)}"


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    lines = []
    for line in data:
        start, end = line.strip().split(" -> ")

        sx, sy = [int(i) for i in start.split(",")]
        ex, ey = [int(i) for i in end.split(",")]

        lines.append(Line(Point(sx, sy), Point(ex, ey)))


    return lines


if __name__ == "__main__":
    main()
