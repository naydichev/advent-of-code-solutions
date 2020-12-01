#!/usr/bin/env python3

from collections import namedtuple

INTO_NEW = "into new stack"
WITH_INC = "with increment"
CUT = "cut"

Operation = namedtuple("Operation", ["kind", "value"], defaults=[INTO_NEW, None])


def main(raw, num_cards=10007):
    operations = parse(raw)

    for i in range(101741582076661):
        if i % 10 == 0:
            print(i)
        cards = execute(operations, num_cards)


    print(cards[2020])


def execute(operations, num_cards):
    cards = range(num_cards)

    for op in operations:
        if op.kind == INTO_NEW:
            cards = reversed(cards)
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
    import resource
    resource.setrlimit(resource.RLIMIT_RSS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

    with open("shuffle.pi") as f:
        main(f.read().strip().split("\n"), 119315717514047)
