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


def program_output(lines, value):
    if value == 10:
        print("".join(lines))
        for _ in range(len(lines)):
            lines.pop()

        lines.append("")
    else:
        if value < 128:
            lines.append(chr(value))
        else:
            lines.append(value)


def program_input(commands, pointer):
    val = commands[pointer["idx"]]
    pointer["idx"] += 1
    return val


def main(instructions):
    instructions[0] = 2
    lines = []

    command = to_input(["A", "A", "B", "C", "C", "A", "C", "B", "C", "B"])
    func_A = to_input(["L4", "L4", "L6", "R10", "L6"])
    func_B = to_input(["L12", "L6", "R10", "L6"])
    func_C = to_input(["R8", "R10", "L6"])

    full_input = command + func_A + func_B + func_C + to_input("y")
    pointer = dict(idx=0)

    program = Thread(target=run_program,
        args=(instructions, partial(program_input, full_input, pointer), partial(program_output, lines)),
        kwargs=dict(debug=False),
        name="program-thread",
        daemon=True
    )
    program.start()

    program.join()

    print(f"final answer: {lines[-1]}")

def to_input(commands):
    out = []
    for c in commands:
        out.append(ord(c[0]))
        out.append(ord(","))
        if len(c) > 1:
            out.extend([ord(x) for x in c[1:]])
            out.append(ord(","))

    out[-1] = ord("\n")
    return out


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
