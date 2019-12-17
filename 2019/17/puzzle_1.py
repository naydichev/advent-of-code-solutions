#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from functools import partial
from threading import Thread

Point = namedtuple("Point", ["x", "y"])

SCAFFOLD = "#"
SPACE = "."
SHIPS = ["^", "<", "v", ">"]
NEWLINE = "\n"

FG_RED = "\33[31m"
FG_BLUE = "\33[34m"
RESET = "\33[0m"


def program_output(space, value):
    d = chr(value)
    if d == NEWLINE:
        space.append([])
    else:
        space[-1].append(d)


def program_input():
    pass


def main(instructions):
    space = [[]]

    program = Thread(target=run_program,
        args=(instructions, program_input, partial(program_output, space)),
        kwargs=dict(debug=True),
        name="program-thread",
        daemon=True
    )
    program.start()

    program.join()

    new_space = to_map(space)
    intersections = find_intersections(new_space)
    print_map(new_space, intersections)
    print(intersections)
    alignment = [p.x * p.y for p in intersections]

    print(f"sum of alignement is {sum(alignment)}")


def print_map(space, highlight=[]):
    min_y = min(p.y for p in space.keys())
    min_x = min(p.x for p in space.keys())
    max_y = max(p.y for p in space.keys())
    max_x = max(p.x for p in space.keys())

    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            if p in highlight:
                line.append(f"{FG_BLUE}{space[p]}{RESET}")
            else:
                line.append(space[p])

        print("".join(line))
    print()

D = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

def find_intersections(space):
    intersections = []
    for point in list(space.keys()):
        neighbors = [Point(point.x + x, point.y + y) for x, y in D]
        print([space[n] for n in neighbors])
        if all([space[n] == SCAFFOLD for n in neighbors]):
            print("yes")
            intersections.append(point)

    return intersections


def to_map(space):
    new_space = defaultdict(lambda: SPACE)

    for y, line in enumerate(space):
        for x, char in enumerate(line):
            new_space[Point(x, y)] = char

    return new_space

if __name__ == "__main__":
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "aoc.17"
    from intcode import run_program

    with open("ascii.pi") as f:
        main(list(map(int, f.read().rstrip().split(","))))
