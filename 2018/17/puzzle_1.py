#!/usr/bin/python

from collections import defaultdict
from collections import deque
import sys

if len(sys.argv) == 2:
    MAX_ROUNDS = int(sys.argv[-1])
else:
    MAX_ROUNDS = None
CLAY = "#"
SAND = "."
WATER = "~"
FLOW = "|"
SOURCE = "+"
YMIN = None
YMAX = None
XMIN = None
XMAX = None

def main():
    global XMIN, XMAX
    with open("spring.pi") as f:
        raw_springs = f.read().split("\n")

    water_springs = parse(raw_springs)

    queue = deque()
    queue.append((500, 0))

    flow_water(water_springs, queue)
    XMIN, XMAX = find_bounds(water_springs)
    print_springs(water_springs)
    reach = wheres_the_water(water_springs)
    print("water can reach {} tiles".format(reach))

rounds = 0
def flow_water(springs, queue):
    global rounds

    while len(queue):
        source = queue.popleft()
        y_current = source[1]
        x_current = source[0]

        rounds += 1

        while springs[y_current + 1][x_current] == SAND and y_current < YMAX:
            y_current += 1
            springs[y_current][x_current] = FLOW

        if MAX_ROUNDS and rounds > MAX_ROUNDS:
            return False
        else:
            print("round {}".format(rounds))

        flow = True
        while flow:
            flow = False
            y_next = y_current + 1
            if springs[y_next][x_current] in [CLAY, WATER]:
                flow = spill_out(springs, y_current, x_current, queue)
            y_current -= 1


def spill_out(springs, y, x, queue):
    # check left and right for walls
    left = check_left(springs, y, x)
    right = check_right(springs, y, x)
    if left is not None and right is not None:
        # fill it
        for i in range(left + 1, right):
            springs[y][i] = WATER
        return True
    elif left is not None and right is None:
        for i in range(left + 1, x + 1):
            springs[y][i] = FLOW
        drop = False
        while not drop:
            x += 1
            springs[y][x] = FLOW
            if springs[y + 1][x] == SAND:
                drop = True
        queue.append((x, y))
    elif left is None and right is not None:
        for i in range(x, right):
            springs[y][i] = FLOW
        drop = False
        while not drop:
            x -= 1
            springs[y][x] = FLOW
            if springs[y + 1][x] == SAND:
                drop = True
        queue.append((x, y))
    elif left is None and right is None:
        left = check_left(springs, y, x, True)
        right = check_right(springs, y, x, True)
        if left:
            for i in range(left, x):
                springs[y][i] = FLOW
            queue.append((left, y))
        if right:
            for i in range(x, right + 1):
                springs[y][i] = FLOW
            queue.append((right, y))
    return False

def check_right(springs, y, x, drop=False):
    right = lambda x, y: (x + 1, y)
    return check_dir(springs, y, x, drop, right)

def check_left(springs, y, x, drop=False):
    left = lambda x, y: (x - 1, y)
    return check_dir(springs, y, x, drop, left)

def check_dir(springs, y, x, drop, f):
    while y >= YMIN and y <= YMAX:
        if springs[y + 1][x] in [SAND, FLOW]:
            return None if not drop else x
        elif springs[y][x] == CLAY:
            return x

        x, y = f(x, y)

    return None

def wheres_the_water(springs):
    reach = 0
    for y in range(YMIN, YMAX + 1):
        for x in range(XMIN, XMAX + 1):
            if springs[y][x] in [WATER, FLOW]:
                reach += 1

    return reach

def print_springs(springs):
    ymin = min(springs.keys())
    ymax = max(springs.keys())
    for y in range(ymin, ymax + 1):
        row = ["{:4d}".format(y), " "]
        for x in range(XMIN, XMAX + 1):
            row.append(springs[y][x])
        print("".join(row))

def find_bounds(springs):
    xmin, xmax = None, None

    for y in range(YMIN, YMAX + 1):
        local_keys = springs[y].keys()

        if not local_keys:
            continue

        local_xmin = min(local_keys)
        local_xmax = max(local_keys)

        if xmin is None or local_xmin < xmin:
            xmin = local_xmin

        if xmax is None or local_xmax > xmax:
            xmax = local_xmax

    return xmin, xmax

def parse(raw):
    global YMIN, YMAX
    grid = defaultdict(lambda: defaultdict(lambda: SAND))

    for row in raw:
        parts = row.split(", ")
        xory, value = parts[0].split("=")
        if xory == "y":
            x = parse_range(parts[1])
            y = int(value)
            for i in x:
                grid[y][i] = CLAY
        else:
            y = parse_range(parts[1])
            x = int(value)
            for i in y:
                grid[i][x] = CLAY

    YMIN = min(grid.keys())
    YMAX = max(grid.keys())

    grid[0][500] = SOURCE

    return grid

def parse_range(data):
    _, value = data.split("=")
    datamin, datamax = value.split("..")

    return [i for i in range(int(datamin), int(datamax) + 1)]

if __name__ == "__main__":
    main()
