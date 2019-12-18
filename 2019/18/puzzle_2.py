#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from random import shuffle

Point = namedtuple("Point", ["x", "y"])
Space = namedtuple("Space", ["location", "kind", "value"], defaults=[None] * 3)
PointWithKeys = namedtuple("PointWithKeys", ["point", "keys"])

KEY = "key"
DOOR = "door"
WALL = "#"
EMPTY = "."
START = "@"


def main(raw):
    maze = parse(raw)
    starts = [p for p in maze.keys() if maze[p].kind == START]

    steps = find_shortest_path(maze, starts)
    print(f"fewest steps {steps}")


D = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find_reachable_keys(maze, current, keys):
    queue = [current]
    distance = {current: 0}
    found_keys = dict()

    while len(queue):
        inspect = queue.pop(0)
        for point in [Point(inspect.x + x, inspect.y + y) for x, y in D]:
            space = maze[point]
            if space.kind == WALL or space.location in distance:
                continue
            distance[space.location] = distance[inspect] + 1
            if space.kind == DOOR and space.value not in keys:
                continue
            elif space.kind == KEY and space.value not in keys:
                found_keys[space] = distance[space.location]
            else:
                queue.append(space.location)

    return found_keys


def find_all_reachable_keys(maze, currents, keys):
    found_keys = {}
    for i, point in enumerate(currents):
        new_keys = find_reachable_keys(maze, point, keys)
        for s, d in new_keys.items():
            found_keys[s] = (d, i)

    return found_keys


PATHS = {}

def find_shortest_path(maze, currents, keys=set()):
    pk = PointWithKeys(tuple(currents), frozenset(keys))
    if pk in PATHS:
        return PATHS[pk]

    reachable_keys = find_all_reachable_keys(maze, currents, keys)
    options = []
    if not len(reachable_keys):
        # couldn't reach anything, we must have them all
        options.append(0)
    else:
        for space, (distance, quadrant) in reachable_keys.items():
            k_copy = keys.copy()
            k_copy.add(space.value)
            c_copy = currents.copy()
            c_copy[quadrant] = space.location

            options.append(
                distance + find_shortest_path(maze, c_copy, k_copy)
            )

    PATHS[pk] = min(options)
    return PATHS[pk]


def parse(raw):
    maze = defaultdict(lambda: Space(None, WALL))
    for y, row in enumerate(raw):
        for x, val in enumerate(row):
            p = Point(x, y)
            kind = None
            value = None
            if val == EMPTY:
                kind = EMPTY
            elif val == WALL:
                kind = WALL
            elif val == START:
                kind = START
            elif val == val.upper():
                kind = DOOR
                value = val.lower()
            elif val == val.lower():
                kind = KEY
                value = val

            maze[p] = Space(p, kind, value)

    return maze


BG_WHITE = "\33[47m"
BG_BLACK = "\33[40m"
FG_PINK = "\33[95m"
FG_BLUE = "\33[34m"
FG_RED = "\33[31m"
RESET = "\33[0m"


def print_maze(maze, highlight=None, keys=None):
    max_y = max(p.y for p in maze.keys())
    max_x = max(p.x for p in maze.keys())

    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            p = maze[Point(x, y)]
            spot = p.kind
            colored = p.kind
            if p.kind == DOOR:
                spot = p.value.upper()
                colored = f"{FG_RED}{spot}{RESET}"
            elif p.kind == KEY:
                spot = p.value
                colored = f"{FG_BLUE}{spot}{RESET}"

            if p.location == highlight:
                colored = f"{FG_PINK}{BG_BLACK}{spot}{RESET}"

            line.append(colored)

        print("".join(line))
    if keys:
        print(f"Keys obtained: {keys}")
    print()


if __name__ == "__main__":
    with open("maze-part-2.pi") as f:
        main(f.read().strip().split("\n"))
