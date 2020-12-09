#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations


def main():
    # with open("sample.pi") as f:
    with open("xmas.pi") as f:
        data = parse(f.readlines())

    preamble = 25

    target = find_missing_sum(preamble, data)

    for i in range(2, len(data)):
        n = target - data[i]

        start = i
        while i >= 0 and n > 0:
            i -= 1
            n -= data[i]

        if n == 0:
            nums = data[i:start]
            maxnum = max(nums)
            minnum = min(nums)
            weakness = maxnum + minnum
            print(f"I think you want {weakness}")
            break


def find_missing_sum(preamble, data):
    for i in range(preamble, len(data)):
        sums = [sum(pair) for pair in combinations(data[i - preamble:i], 2)]

        if data[i] not in sums:
            return data[i]

    return None


def parse(raw):
    return [int(l.strip()) for l in raw]


if __name__ == "__main__":
    main()
