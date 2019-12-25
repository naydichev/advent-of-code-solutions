#!/usr/bin/env python3

from collections import defaultdict
from functools import partial
from itertools import combinations

ITEMS = [ "fuel cell", "easter egg", "cake", "ornament", "hologram", "hypercube", "klein bottle", "dark matter" ]

def attempts():
    i = 1
    while i < len(ITEMS):
        for op in combinations(ITEMS, i):
            yield op
        i += 1

def producer(data, held, choices):
    if len(data) == 0 and len(held):
        h = [f"drop {i}" for i in held]
        data.extend(list("\n".join(h)))
        data.append("\n")
        print(f"DROPPING {held}")
        print(f"COMMANDS: {''.join(data)}")
        held.clear()
    elif len(data) == 0 and len(held) == 0:
        choice = next(choices)
        h = [f"take {i}" for i in choice] + ["west"]
        data.extend(list("\n".join(h)))
        data.append("\n")
        held.extend(choice)
        print(f"HOLDING {held}")
        print(f"COMMANDS: {''.join(data)}")
        # prompt = input(">")
        # data.extend(list(prompt))
        # data.append("\n")

    v = data.pop(0)
    return ord(v)


def consumer(data, value):
    data.append(chr(value))

    if value == 10:
        print("".join(data))
        data.clear()


def main(instructions):
    in_data = list("\n".join([
        "south",
        "west",
        "take fuel cell",
        "west",
        "take easter egg",
        "east",
        "east",
        "north",
        "north",
        "north",
        "east",
        "east",
        "take cake",
        "west",
        "west",
        "south",
        "south",
        "east",
        "take ornament",
        "east",
        "take hologram",
        "east",
        "take dark matter",
        "north",
        "north",
        "east",
        "east",
        "take klein bottle",
        "north",
        "take hypercube",
        "north",
        ""
    ]))
    held = ITEMS.copy()
    choices = attempts()
    out_data = []
    thread = execute_program(instructions.copy(), partial(producer, in_data, held, choices), partial(consumer, out_data), False)
    thread.start()
    thread.join()

if __name__ == "__main__":
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "aoc.25"
    from intcode import execute_program

    with open("droid.pi") as f:
        main(list(map(int, f.read().strip().split(","))))
