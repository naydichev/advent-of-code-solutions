#!/usr/bin/python

from collections import defaultdict
from heapq import heappop, heappush

CLIMBING_GEAR = "climbing_gear"
TORCH = "torch"
NEITHER = "neither"
GEAR = [ NEITHER, TORCH, CLIMBING_GEAR ]
VALID_GEAR = [
    [ TORCH, CLIMBING_GEAR ],
    [ NEITHER, CLIMBING_GEAR ],
    [ NEITHER, TORCH ]
]

TYPES = [
    ".",
    "=",
    "|",
]

ROCKY = TYPES[0]
WET = TYPES[1]
NARROW = TYPES[2]

class RegionManager(object):
    def __init__(self, depth, target):
        self.grid = defaultdict(dict)
        self.depth = depth
        self.target = target

    def get(self, x, y):
        if x in self.grid[y]:
            return self.grid[y][x]

        self.grid[y][x] = dict(geo=self._geo(x, y))
        self.grid[y][x]["ero"] = self._ero(self.grid[y][x]["geo"])
        self.grid[y][x]["type"] = self._type(self.grid[y][x]["ero"])

        return self.grid[y][x]

    def _geo(self, x, y):
        if x == 0 and y == 0:
            return 0
        elif x == self.target[0] and y == self.target[1]:
            return 0
        elif y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271

        return self.get(x - 1, y)["ero"] * self.get(x, y - 1)["ero"]

    def _ero(self, geo):
        return (geo + self.depth) % 20183

    def _type(self, ero):
        return ero % 3

def main(depth, target):
    manager = RegionManager(depth, target)

    time_to_target = find_route_to_target(manager)

    print("Time to target is {}".format(time_to_target))

def find_route_to_target(manager):
    depth = manager.depth
    target = (manager.target[0], manager.target[1], TORCH)

    best = {}
    # (minutes, x, y, equipment)
    queue = [(0, 0, 0, TORCH)]

    while len(queue):
        minutes, x, y, equipment = heappop(queue)

        key = (x, y, equipment)
        if key in best and best[key] <= minutes:
            continue

        best[key] = minutes

        if key == target:
            print("we got to the end!")
            return minutes

        region = manager.get(x, y)
        for gear in VALID_GEAR[region["type"]]:
            if gear == equipment:
                continue
            heappush(queue, (minutes + 7, x, y, gear))


        for dx, dy in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            new_x = x + dx
            new_y = y + dy
            if new_x < 0 or new_y < 0:
                continue
            if equipment not in VALID_GEAR[manager.get(new_x, new_y)["type"]]:
                continue
            heappush(queue, (minutes + 1, new_x, new_y, equipment))

if __name__ == "__main__":
    with open("target.pi") as f:
        raw = f.read().split("\n")

    depth = int(raw[0].split(": ")[1])
    target = raw[1].split(": ")[1]
    targetx, targety = [int(i) for i in target.split(",")]

    # sample:
    # depth = 510
    # targetx, targety = (10, 10)

    main(depth, (targetx, targety))
