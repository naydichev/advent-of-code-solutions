#!/usr/bin/env python3

import re

PAIR_PATTERN = re.compile(r"([a-z])\1")
FORBIDDEN = 'iol'
FORBIDDEN_LIST = list(FORBIDDEN)


def straight(data):
    o = [ord(d) for d in data]

    for i in range(len(o) - 3):
        if o[i + 1] - o[i] == 1 and o[i + 2] - o[i + 1] == 1:
            return True

    return False


def distinct_pairs(data):
    letters = set()

    match = PAIR_PATTERN.search(data, 0)
    start = 0
    while match is not None:
        letters.add(match.group(1))

        match = PAIR_PATTERN.search(data, match.pos + 1)

    return len(letters) > 1


def invalid_characters(password):
    return not any([x in FORBIDDEN for x in password])

RULES = [
    invalid_characters,
    distinct_pairs,
    straight
]

def main(starting):

    incremented = starting
    valid = False

    while valid is False:
        incremented = increment(incremented)
        print(incremented)
        valid = is_valid(incremented)

    print(f"the next valid password after {starting} is {incremented}")
    return incremented


def inc(c):
    return chr(ord(c) + 1)

def increment(password):
    incremented = []
    p = list(password)

    match = next((x for x in FORBIDDEN_LIST if x in p), False)
    if match is not False:
        i = p.index(match)
        p[i] = inc(match)
        p[i + 1:] = ['a'] * (len(p) - i - 1)
        print(f"found a thing {match}, it was at {i}. new thing is {p}")
        return "".join(p)

    flipped = password[::-1]
    for i, c in enumerate(flipped):
        if c == 'z':
            incremented.append('a')
        else:
            d = inc(c)
            while d in 'iol':
                d = inc(d)
            incremented.append(d)
            incremented.extend(flipped[i + 1:])
            break


    return "".join(reversed(incremented))


def is_valid(password):
    return all([rule(password) for rule in RULES])


if __name__ == "__main__":
   main(main('cqjxjnds'))
