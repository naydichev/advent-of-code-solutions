#!/usr/bin/env python3

import sys
from functools import reduce
from itertools import combinations, permutations


def main(packages):
    target = sum(packages) // 4

    qe = find_group(packages, target)
    print(f"lowest qe is {qe}")


def find_group(packages, target):
    for possible, possible_qe in generate_first_grouping(packages, target):
        p_copy = packages - set(possible)

        for suboption in permutations(p_copy):
            if can_be_split_evenly(set(suboption)):
                return possible_qe


def generate_first_grouping(packages, target):
    def product(group):
        return reduce(lambda a, b: a * b, group)

    first = 1
    while first < len(packages):
        possibles = []
        for option in combinations(packages, first):
            if sum(option) == target:
                possibles.append(option)

        first += 1
        if len(possibles):
            for possible in sorted(possibles, key=product):
                yield possible, product(possible)


def can_be_split_evenly(packages):
    target = sum(packages) // 3
    for possible, _ in generate_first_grouping(packages, target):
        p_copy = packages - set(possible)
        for subpossible, _ in generate_first_grouping(p_copy, target):
            return True

    return False


if __name__ == "__main__":
    with open("packages.pi") as f:
        main({int(i) for i in f.read().strip().split("\n")})
