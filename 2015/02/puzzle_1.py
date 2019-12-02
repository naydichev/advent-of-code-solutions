#!/usr/bin/env python3

from collections import namedtuple

Box = namedtuple("Box", ["length", "width", "height"])


def main(raw_dimensions):
    dims = parse(raw_dimensions)

    paper = 0

    for dim in dims:
        paper += paper_needed(dim)

    print(f"they need {paper} feet.")


def paper_needed(dim):
    l = 2 * dim.height * dim.width
    w = 2 * dim.length * dim.height
    h = 2 * dim.length * dim.width

    return l + w + h + int(min(l, w, h) / 2)


def parse(raw):
    result = []
    for item in raw:
        result.append(Box(*[int(i) for i in item.split("x")]))

    return result


if __name__ == "__main__":
    with open("input.pi") as f:
        main(f.read()[:-1].split("\n"))
