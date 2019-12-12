#!/usr/bin/env python3

from collections import namedtuple
from random import shuffle

Replacement = namedtuple("Replacement", "char to")


def main(molecule, raw_replacements):
    replacements = parse(raw_replacements)
    starters = [p for p in replacements if p.char == 'e']
    others = [p for p in replacements if p not in starters]

    n = 0
    while n == 0:
        n = backtrack(molecule, replacements)

    print(f"it takes {n} to make the molecule.")


def backtrack(molecule, replacements):
    copy = molecule[:]
    steps = 0
    previous = ''

    # force a different ordering
    shuffle(replacements)

    # until we can't make any further replcements
    while previous != copy:
        previous = copy

        # try each replacement
        for r in replacements:
            # until it's no longer in the source string
            while r.to in copy:
                steps += copy.count(r.to)
                copy = copy.replace(r.to, r.char)

    # it's only valid if the result is 'e'
    if copy != 'e':
        return 0
    return steps

def parse(raw):
    replacements = []
    for r in raw:
        parts = r.split(" => ")
        replacements.append(Replacement(parts[0], parts[1]))

    return replacements


if __name__ == "__main__":
    with open("molecules.pi") as f:
        lines = f.read().strip().split("\n")
        molecule = lines[-1]
        replacements = lines[:-2]

        main(molecule, replacements)
