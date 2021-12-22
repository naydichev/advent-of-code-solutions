#!/usr/bin/env python3

from collections import Counter, defaultdict, namedtuple

Instruction = namedtuple("Instruction", "target, xmin, xmax, ymin, ymax, zmin, zmax")


def main():
    data = parse_input()

    ons = set()

    lower = lambda x: max(-50, x)
    upper = lambda x: min(51, x)

    for line in data:
        for x in range(lower(line.xmin), upper(line.xmax + 1)):
            for y in range(lower(line.ymin), upper(line.ymax + 1)):
                for z in range(lower(line.zmin), upper(line.zmax + 1)):
                    if line.target == "on":
                        ons.add((x, y, z))
                    else:
                        ons.discard((x, y, z))

    print(f"There are {len(ons)} on")


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
