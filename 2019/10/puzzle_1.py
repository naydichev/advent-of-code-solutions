#!/usr/bin/env python3

from collections import defaultdict, namedtuple
import math

Point = namedtuple("Point", ["x", "y"])

def main(raw):
    starmap = make_map(raw)
    asteroids = [x for x in starmap.keys() if starmap[x]]

    best = {}
    for a in asteroids:
        visible = calculate_visible_asteroids(a, asteroids)
        if len(visible) > len(best):
            best = visible

    print(f"the most visible asteroids are {len(best)}")


def calculate_visible_asteroids(source, asteroids):
    targets = defaultdict(list)

    for target in asteroids:
        if source == target:
            continue

        dx = target.x - source.x
        dy = target.y - source.y
        dist = math.gcd(abs(dx), abs(dy))
        dx /= dist
        dy /= dist

        targets[Point(dx, dy)].append((dist, target))

    return targets


def make_map(raw):
    starmap = dict()

    for y, row in enumerate(raw):
        for x, c in enumerate(row):
            v = True
            if c is ".":
                v = False
            starmap[Point(x, y)] = v

    return starmap


if __name__ == "__main__":
    with open("asteroids.pi") as f:
        main(f.read().rstrip().split("\n"))
