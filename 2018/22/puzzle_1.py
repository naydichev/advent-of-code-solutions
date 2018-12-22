#!/usr/bin/python

from collections import defaultdict

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

class Region(object):
    TYPES = [
        (0, "."),
        (1, "="),
        (2, "|"),
    ]

    ROCKY = TYPES[0]
    WET = TYPES[1]
    NARROW = TYPES[2]

    def __init__(self, point, depth, target, grid):
        self.point = point
        self.depth = depth
        self.target = target
        self.geologic_index = self.determine_geologic_index(grid)
        self.erosion_level= self.determine_erosion_level()
        self.type = self.determine_type()

    def determine_type(self, point, depth):
        geologic_index = self.determine_geologic_index(point)

    def determine_geologic_index(self, grid):
        if self.point.x == 0 and self.point.y == 0:
            return 0
        elif self.point.x == self.target.x and self.point.y == self.target.y:
            return 0
        elif self.point.y == 0:
            return self.point.x * 16807
        elif self.point.x == 0:
            return self.point.y * 48271
        else:
            return grid[self.point.y][self.point.x - 1].erosion_level * grid[self.point.y - 1][self.point.x].erosion_level

    def determine_erosion_level(self):
        return (self.geologic_index + self.depth) % 20183


    def determine_type(self):
        return Region.TYPES[self.erosion_level % 3]

    def __repr__(self):
        return "{}".format(self.type[1])

    def __str__(self):
        return "{}(point={}, depth={}, target={}, geologic_index={}, erosion_level={}, type={})".format(
                self.__class__.__name__, self.point, self.depth, self.target, self.geologic_index, self.erosion_level, self.types
        )

def main(depth, target):
    grid = make_grid(depth, target)

    print_grid(grid, target)

    risk_level = calculate_risk(grid, target)

    print("Risk level for this cave is {}".format(risk_level))

def calculate_risk(grid, target):
    risk = 0
    for y in range(target.y + 1):
        for x in range(target.x + 1):
            risk += grid[y][x].type[0]

    return risk

def print_grid(grid, target):
    maxY = max(grid.keys())
    maxX = max(grid[maxY].keys())

    for y in range(maxY + 1):
        row = []
        for x in range(maxX + 1):
            if x == 0 and y == 0:
                row.append("M")
            elif y == target.y and x == target.x:
                row.append("T")
            else:
                row.append(repr(grid[y][x]))

        print("".join(row))

def make_grid(depth, target):
    grid = defaultdict(dict)

    for y in range(target.y + 1):
        for x in range(target.x + 1):
            grid[y][x] = Region(Point(x, y), depth, target, grid)

    return grid

if __name__ == "__main__":
    with open("target.pi") as f:
        raw = f.read().split("\n")

    depth = int(raw[0].split(": ")[1])
    target = raw[1].split(": ")[1]
    targetx, targety = [int(i) for i in target.split(",")]

    # sample:
#    depth = 510
#    targetx, targety = (10, 10)

    main(depth, Point(targetx, targety))
