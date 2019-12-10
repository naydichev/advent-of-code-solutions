#!/usr/bin/env python3

from collections import namedtuple
from itertools import combinations

Vessel = namedtuple("Vessel", ["amount", "id"])

def main(containers, amount):
    vessels = [Vessel(x, i) for i, x in enumerate(containers)]

    n = 0
    for i in range(len(vessels)):
        for option in combinations(vessels, i):
            if sum([o.amount for o in option]) == amount:
                n += 1

    print(f"there are {n} ways to fill {amount}")


if __name__ == "__main__":
    # main([20, 15, 10, 5, 5], 25)
    with open("containers.pi") as f:
        main([int(x) for x in f.read().strip().split("\n")], 150)
