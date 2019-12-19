#!/usr/bin/env python3

from functools import partial
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

X_NEXT = "x_next"
LAST = "last"

def producer(inputs, conf):
    x_next = conf[X_NEXT]
    conf[X_NEXT] = not x_next

    if x_next:
        return inputs[0]
    return inputs[1]


def consumer(plot, coords, value):
    plot[Point(*coords)] = value


def main(instructions):
    conf = dict(x_next=True)
    plot = dict()

    for y in range(50):
        for x in range(50):
            program_thread = execute_program(instructions.copy(), partial(producer, (x, y), conf), partial(consumer, plot, (x, y)), True)

            program_thread.join()

    affected = sum(plot.values())
    print(f"there are {affected} points")


if __name__ == "__main__":
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "aoc.19"
    from intcode import execute_program

    with open("emitter.pi") as f:
        main(list(map(int, f.read().strip().split(","))))
