#!/usr/bin/env python3

from collections import namedtuple

FIELDS = [
    "children",
    "cats",
    "samoyeds",
    "pomeranians",
    "akitas",
    "vizslas",
    "goldfish",
    "trees",
    "cars",
    "perfumes"
]

SUE_DATA = dict(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1
)


Sue = namedtuple("Sue", ["number"] + FIELDS, defaults=[None] * (len(FIELDS) + 1))


def main(raw):
    sues = parse(raw)

    best_match = max(sues, key=lambda sue: calculate_score(sue))

    print(best_match)


def calculate_score(sue):
    matching_fields = 0

    for i, field in enumerate(FIELDS, 1):
        if sue[i] == SUE_DATA[field]:
            matching_fields += 1

    return matching_fields


def parse(raw):
    sues = []

    for sue in raw:
        parts = sue.replace(":", "").replace(",", "").split()
        deets = {}
        i = 2
        while i < len(parts):
            deets[parts[i]] = int(parts[i + 1])
            i += 2

        sues.append(Sue(number=int(parts[1]), **deets))

    return sues


if __name__ == "__main__":
    with open("sue.pi") as f:
        main(f.read().rstrip().split("\n"))
