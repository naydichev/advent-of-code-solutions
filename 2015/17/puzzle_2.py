#!/usr/bin/env python3

from collections import namedtuple
from itertools import combinations

Vessel = namedtuple("Vessel", ["amount", "id"])

def main(containers, amount):
    vessels = [Vessel(x, i) for i, x in enumerate(containers)]

    n = 0
    for i in range(len(vessels)):
        n_i = 0
        for option in combinations(vessels, i):
            if sum([o.amount for o in option]) == amount:
                n_i += 1

        if n == 0 and n_i != 0:
            print(f"there are {n_i} ways to fill {amount} with {i} bottles")
        n += n_i

    print(f"there are {n} ways to fill {amount}")


if __name__ == "__main__":
    # main([20, 15, 10, 5, 5], 25)
    with open("containers.pi") as f:
        main([int(x) for x in f.read().strip().split("\n")], 150)
