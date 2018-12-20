#!/usr/bin/python

from collections import defaultdict
from collections import deque
from collections import namedtuple

PathComponent = namedtuple("PathComponent", ["position", "doors", "distance"])

N = "N"
E = "E"
W = "W"
S = "S"

DIRECTION = dict(
    N=lambda p: (p[0], p[1] - 1),
    S=lambda p: (p[0], p[1] + 1),
    E=lambda p: (p[0] + 1, p[1]),
    W=lambda p: (p[0] - 1, p[1]),
)

WALL = "#"
DOOR_NS = "-"
DOOR_EW = "|"

class Room(object):
    def __init__(self):
        self.north = "?"
        self.south = "?"
        self.east = "?"
        self.west = "?"

XMIN = None
XMAX = None
YMIN = None
YMAX = None

def main(raw):
    grid = make_grid(raw[1:-1])

    print_grid(grid)

    doors = find_path(grid)

    print("max doors, shortest distance: {}".format(len(doors)))
    print_grid(grid, doors)

def find_path(grid):
    queue = deque()
    queue.append(PathComponent((0,0), [], 0))

    visited = set()
    distance = {}

    while len(queue):
        pc = queue.popleft()

        if pc.position in visited:
            continue

        visited.add(pc.position)

        distance[pc.position] = pc

        x = pc.position[0]
        y = pc.position[1]
        new_directions = []
        if grid[y][x].north != WALL:
            new_directions.append(DIRECTION[N](pc.position))
        if grid[y][x].south != WALL:
            new_directions.append(DIRECTION[S](pc.position))
        if grid[y][x].east != WALL:
            new_directions.append(DIRECTION[E](pc.position))
        if grid[y][x].west != WALL:
            new_directions.append(DIRECTION[W](pc.position))

        for d in new_directions:
            queue.append(PathComponent(d, pc.doors + [d], pc.distance + 1))
    max_key = max(distance, key=lambda k: len(distance[k].doors))

    return distance[max_key].doors

def make_grid(raw):
    global YMIN, YMAX, XMIN, XMAX
    grid = defaultdict(lambda: defaultdict(Room))

    current_position = (0, 0)
    branches = []

    for c in raw:
        if c == "(":
            branches.append(current_position)
        elif c == ")":
            branches.pop()
        elif c == "|":
            current_position = branches[-1]
        else:
            next_position = DIRECTION[c](current_position)
            if c == N:
                grid[current_position[1]][current_position[0]].north = DOOR_NS
                grid[next_position[1]][next_position[0]].south = DOOR_NS
            elif c == S:
                grid[current_position[1]][current_position[0]].south = DOOR_NS
                grid[next_position[1]][next_position[0]].north = DOOR_NS
            elif c == E:
                grid[current_position[1]][current_position[0]].east = DOOR_EW
                grid[next_position[1]][next_position[0]].west = DOOR_EW
            else:
                grid[current_position[1]][current_position[0]].west = DOOR_EW
                grid[next_position[1]][next_position[0]].east = DOOR_EW

            current_position = next_position

            if YMIN is None or current_position[1] < YMIN:
                YMIN = current_position[1]
            if YMAX is None or current_position[1] > YMAX:
                YMAX = current_position[1]
            if XMIN is None or current_position[0] < XMIN:
                XMIN = current_position[0]
            if XMAX is None or current_position[0] > XMAX:
                XMAX = current_position[0]

    for y in range(YMIN, YMAX + 1):
        for x in range(XMIN, XMAX + 1):
            if grid[y][x].north == "?":
                grid[y][x].north = WALL
            if grid[y][x].south == "?":
                grid[y][x].south = WALL
            if grid[y][x].east == "?":
                grid[y][x].east = WALL
            if grid[y][x].west == "?":
                grid[y][x].west = WALL

    return grid

def print_grid(grid, path=[]):
    SPACE = "    "
    # print(SPACE + "".join("{:3d}".format(x) for x in range(XMIN, XMAX + 1)))
    for y in sorted(grid.keys()):
        print(SPACE + WALL + WALL.join(grid[y][x].north for x in range(XMIN, XMAX + 1)) + WALL)
        row = [WALL]
        for x in sorted(grid[y].keys()):
            if x == 0 and y == 0:
                row.append("X")
            elif (x, y) in path:
                row.append("+")
            else:
                row.append(".")
            row.append(grid[y][x].east)
        print("{:3d} ".format(y) + "".join(row))

    print(SPACE + WALL * ((XMAX - XMIN + 1) * 2 + 1))

def parse(raw, start=0, end=None):
    path = []
    branch = []
    i = start
    if end is None:
        end = len(raw)

    while i < end:
        c = raw[i]
        if c == '(':
            n = find_matching(raw, i)
            subpath = parse(raw, i + 1, n)
            print(subpath)
            i += n
        else:
            path.append(Path(direction=c))

        i += 1

    return path

def find_matching(raw, start):
    pstack = []
    for i, c in enumerate(raw[start:]):
        if c == "(":
            pstack.append(i)
        elif c == ")":
            pstack.pop()
            if not len(pstack):
                return i + start

if __name__ == "__main__":
    with open("map_regex.pi") as f:
        raw = f.read().strip()
    main(raw)
#    main("^ENWWW(NEEE|SSE(EE|N))$")
#    main("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")
#    main("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
#    main("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")
