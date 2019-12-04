#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from itertools import permutations

Path = namedtuple("Path", ["fro", "to", "distance"])


def main(raw_paths):
    paths = parse(raw_paths)

    cities = set([p.to for p in paths] + [p.fro for p in paths])
    destinations = calculate_destinations(paths)

    max_distance = -1
    for option in permutations(cities):
        size = 0
        fro = option[0]
        for to in option[1:]:
            size += destinations[fro][to]
            fro = to

        if size > max_distance:
            max_distance = size

    print(f"longest route is {max_distance}")

def calculate_destinations(paths):
    destinations = defaultdict(lambda: defaultdict(lambda: sys.maxsize))

    for p in paths:
        destinations[p.to][p.fro] = p.distance
        destinations[p.fro][p.to] = p.distance

    return destinations


def parse(raw):
    paths = []
    for p in raw:
        parts = p.split(" ")
        paths.append(Path(parts[0], parts[2], int(parts[-1])))

    return paths


if __name__ == "__main__":
    with open("cities.pi") as f:
        main(f.read().rstrip().split("\n"))
