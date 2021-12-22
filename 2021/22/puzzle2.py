#!/usr/bin/env python3

from collections import Counter, defaultdict, namedtuple

Instruction = namedtuple("Instruction", "target, xmin, xmax, ymin, ymax, zmin, zmax")


def main():
    data = parse_input()

    ons = set()

    for line in data:
        if line.target == "on":
            for x in range(line.xmin, line.xmax + 1):
                for y in range(line.ymin, line.ymax + 1):
                    for z in range(line.zmin, line.zmax + 1):
                            ons.add((x, y, z))
        else:
            for x in list(ons):
                if in_bounds(x, line):
                    ons.discard(x)

    print(f"There are {len(ons)} on")


def in_bounds(x, instruction):
    return x[0] >= instruction.xmin and x[0] <= instruction.xmin and \
            x[1] >= instruction.ymin and x[1] <= instruction.ymin and \
            x[2] >= instruction.zmin and x[2] <= instruction.zmin


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    instructions = []
    for line in data:
        target, rest = line.split(" ")
        coords = dict()
        for part in rest.split(","):
            key, bounds = part.split("=")
            minb, maxb = [int(b) for b in bounds.split("..")]
            coords[key] = [minb, maxb]

        instructions.append(Instruction(target, *coords["x"], *coords["y"], *coords["z"]))


    return instructions


if __name__ == "__main__":
    main()
