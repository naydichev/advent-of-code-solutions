#!/usr/bin/env python3

import math
import itertools
from collections import defaultdict, namedtuple

Point = namedtuple("Point", ["x", "y"])


def main(raw, nth_hit):
    starmap = make_map(raw)
    asteroids = [x for x in starmap.keys() if starmap[x]]

    best = {}
    for a in asteroids:
        visible = calculate_visible_asteroids(a, asteroids)
        if len(visible) > len(best):
            best = visible

    print(f"the most visible asteroids are {len(best)}")

    for direction in best:
        best[direction] = [t for dist, t in sorted(best[direction])]

    # sort by hit order
    hit_list = calculate_hit_list(best)

    target = hit_list[nth_hit - 1]
    print(f"the thingy is {target.x * 100 + target.y}")


def calculate_hit_list(targets):
    to_angle = lambda d: (math.degrees(math.atan2(d.y, d.x)) + 90) % 360

    keys = sorted(targets.keys(), key=to_angle)
    return list(
        filter(
            None,
            itertools.chain.from_iterable(
                itertools.zip_longest(*[targets[d] for d in keys])
            )
        )
    )

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
        main(f.read().rstrip().split("\n"), 200)
