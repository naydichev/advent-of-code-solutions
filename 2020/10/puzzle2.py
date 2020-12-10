#!/usr/bin/env python3

from collections import defaultdict


def main():
    with open("jolts.pi") as f:
        jolts = parse(f.readlines())

    possibles = defaultdict(int)
    jolts =  list(sorted(jolts))

    possibles[0] = 1
    for jolt in jolts:
        possibles[jolt] = sum([possibles[jolt - p] for p in range(1, 4)])

    print(possibles[jolts[-1]])


def parse(raw):
    return map(int, raw)


if __name__ == "__main__":
    main()
