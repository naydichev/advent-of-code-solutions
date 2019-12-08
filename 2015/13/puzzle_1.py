#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from itertools import permutations

Happiness = namedtuple("Happiness", [ "a", "amount", "b" ])


def main(raw):
    data = parse(raw)

    people = to_people(data)

    max_happiness = 0
    for possible in permutations(people.keys()):
        happiness = 0
        for i, p in enumerate(possible):
            left = possible[i - 1]
            right = possible[(i + 1) % len(possible)]

            happiness += people[p][left].amount
            happiness += people[p][right].amount

        if happiness > max_happiness:
            max_happiness = happiness

    print(f"max happiness is {max_happiness}")


def to_people(happiness):
    names = {h.a for h in happiness}

    people = defaultdict(lambda: {})
    for person in names:
        people[person] = {h.b: h for h in happiness if h.a == person}

    return people


def parse(raw):
    parsed = []

    for h in raw:
        parts = h.split()
        amount = int(parts[3])
        if parts[2] != "gain":
            amount = -amount
        parsed.append(Happiness(parts[0], amount, parts[-1][:-1]))

    return parsed



if __name__ == "__main__":
    # sample = "Alice would gain 54 happiness units by sitting next to Bob.\nAlice would lose 79 happiness units by sitting next to Carol.\nAlice would lose 2 happiness units by sitting next to David.\nBob would gain 83 happiness units by sitting next to Alice.\nBob would lose 7 happiness units by sitting next to Carol.\nBob would lose 63 happiness units by sitting next to David.\nCarol would lose 62 happiness units by sitting next to Alice.\nCarol would gain 60 happiness units by sitting next to Bob.\nCarol would gain 55 happiness units by sitting next to David.\nDavid would gain 46 happiness units by sitting next to Alice.\nDavid would lose 7 happiness units by sitting next to Bob.\nDavid would gain 41 happiness units by sitting next to Carol."
    # main(sample.split("\n"))
    with open("happiness.pi") as f:
        main(f.read().rstrip().split("\n"))
