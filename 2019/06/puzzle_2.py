#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import permutations


def main(raw_orbits):
    orbits = [o.split(")") for o in raw_orbits]
    objects = {o[1] for o in orbits}
    starmap = make_starmap(orbits)

    start = "YOU"
    destination = "SAN"

    dist = find_path_to(start, destination, starmap)

    print(f"shortest path is {dist}")


def find_path_to(start, finish, starmap, visited=set()):
    if finish in starmap[start]:
        return -1

    local = visited.copy()
    local.add(start)
    next_steps = [p for p in starmap[start] if p not in local]

    if len(next_steps):
        return min([1 + find_path_to(p, finish, starmap, local) for p in next_steps])
    else:
        return sys.maxsize


def make_starmap(orbits):
    starmap = defaultdict(lambda: [])

    for o in orbits:
        starmap[o[0]].append(o[1])
        starmap[o[1]].append(o[0])

    return starmap


if __name__ == "__main__":
    with open("orbits.pi") as f:
        main(f.read().rstrip().split())
