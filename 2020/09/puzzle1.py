#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations


def main():
    # with open("sample.pi") as f:
    with open("xmas.pi") as f:
        data = parse(f.readlines())

    preamble = 25
    for i in range(preamble, len(data)):
        sums = [sum(pair) for pair in combinations(data[i - preamble:i], 2)]

        if data[i] not in sums:
            print(f"{data[i]} not in sum of previous {preamble} combinations")
            break


def parse(raw):
    return [int(l.strip()) for l in raw]


if __name__ == "__main__":
    main()
