#!/usr/bin/env python3

from collections import namedtuple

Box = namedtuple("Box", ["length", "width", "height"])


def main(raw_dimensions):
    dims = parse(raw_dimensions)

    ribbon = 0

    for dim in dims:
        ribbon += ribbon_needed(dim)

    print(f"they need {ribbon} feet.")


def ribbon_needed(dim):
    cubic = dim.width * dim.length * dim.height

    return sum(sorted([dim.height, dim.width, dim.length])[:2]) * 2 + cubic


def parse(raw):
    result = []
    for item in raw:
        result.append(Box(*[int(i) for i in item.split("x")]))

    return result


if __name__ == "__main__":
    with open("input.pi") as f:
        main(f.read()[:-1].split("\n"))
