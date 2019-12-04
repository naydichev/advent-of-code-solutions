#!/usr/bin/env python3

import re

adjacent_pattern = re.compile(r"(\d)(\1)")

def main(the_range):
    minN, maxN = the_range

    possibles = 0
    for i in range(maxN - minN):
        n = minN + i

        if adjacent_digits(n) and \
            only_increasing(n):
            possibles += 1

    print(f"{possibles} possible numbers.")


def adjacent_digits(n):
    return adjacent_pattern.search(str(n)) is not None


def only_increasing(n):
    n_str = str(n)

    n_p = n_str[0]

    for i in n_str[1:]:
        if i < n_p:
            return False
        n_p = i
    return True


if __name__ == "__main__":
    with open("input.pi") as f:
        main([int(n) for n in f.read().rstrip().split("-")])
