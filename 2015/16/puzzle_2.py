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
    children=lambda x: x == 3,
    cats=lambda x: x > 7,
    samoyeds=lambda x: x == 2,
    pomeranians=lambda x: x < 3,
    akitas=lambda x: x == 0,
    vizslas=lambda x: x == 0,
    goldfish=lambda x: x < 5,
    trees=lambda x: x > 3,
    cars=lambda x: x == 2,
    perfumes=lambda x: x == 1
)


Sue = namedtuple("Sue", ["number"] + FIELDS, defaults=[None] * (len(FIELDS) + 1))


def main(raw):
    sues = parse(raw)

    best_match = max(sues, key=lambda sue: calculate_score(sue))

    print(best_match)


def calculate_score(sue):
    matching_fields = 0

    for i, field in enumerate(FIELDS, 1):
        if sue[i] is None:
            continue
        if SUE_DATA[field](sue[i]):
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
