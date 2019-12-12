#!/usr/bin/env python3

from collections import namedtuple

Replacement = namedtuple("Replacement", "char to")


def main(molecule, raw_replacements):
    replacements = parse(raw_replacements)

    possibles = set()

    for rep in replacements:
        loc = molecule.find(rep.char, 0)
        while loc != -1:
            sub = molecule[loc:]
            option = molecule[:loc] + sub.replace(rep.char, rep.to, 1)
            possibles.add(option)
            loc = molecule.find(rep.char, loc + 1)

    print(f"there are {len(possibles)} different molecules")


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
