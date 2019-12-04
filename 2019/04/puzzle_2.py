#!/usr/bin/env python3

import re

adjacent_pattern = re.compile(r"(\d)(\1)")
duplicate_pattern = re.compile(r"(\d)(\1+)")

def main(the_range):
    minN, maxN = the_range

    possibles = 0
    for i in range(maxN - minN + 1):
        n = str(minN + i)

        if only_increasing(n) \
            and adjacent_digits(n) \
            and duplicate_digits(n):
                    possibles += 1

    print(f"{possibles} possible numbers.")


def adjacent_digits(n):
    return adjacent_pattern.search(str(n)) is not None


def duplicate_digits(n):
    start = 0
    match = duplicate_pattern.search(n, start)

    while match is not None:
        m_len = len(match.group(2))
        if m_len % 2 == 0:
            print(n, False)
            return False

        start += m_len + 1
        match = duplicate_pattern.search(n, start)

    print(n, True)
    return True


def only_increasing(n):
    n_p = n[0]

    for i in n[1:]:
        if i < n_p:
            return False
        n_p = i
    return True


if __name__ == "__main__":
    with open("input.pi") as f:
        main([int(n) for n in f.read().rstrip().split("-")])
