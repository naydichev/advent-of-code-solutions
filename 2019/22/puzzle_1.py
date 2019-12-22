#!/usr/bin/env python3

from collections import namedtuple

INTO_NEW = "into new stack"
WITH_INC = "with increment"
CUT = "cut"

Operation = namedtuple("Operation", ["kind", "value"], defaults=[INTO_NEW, None])


def main(raw, num_cards=10007):
    operations = parse(raw)
    cards = execute(operations, num_cards)

    print(cards.index(2019))


def execute(operations, num_cards):
    cards = list(range(num_cards))

    for op in operations:
        if op.kind == INTO_NEW:
            cards = list(reversed(cards))
        elif op.kind == CUT:
            cards = cards[op.value:] + cards[0:op.value]
        else:
            cards = deal_with_increment(cards, op.value)

    return cards


def deal_with_increment(cards, inc):
    card_len = len(cards)
    new_deck = {0: cards.pop(0)}
    i = 0

    while len(cards):
        i = (i + inc) % card_len
        new_deck[i] = cards.pop(0)

    return [new_deck[v] for v in sorted(new_deck.keys())]


def parse(raw):
    operations = []
    for line in raw:
        parts = line.split()
        kind = INTO_NEW
        value = None
        if line.startswith(CUT):
            kind = CUT
            value = int(parts[-1])
        elif WITH_INC in line:
            kind = WITH_INC
            value = int(parts[-1])

        operations.append(Operation(kind, value))

    return operations


if __name__ == "__main__":
    with open("shuffle.pi") as f:
        main(f.read().strip().split("\n"))
