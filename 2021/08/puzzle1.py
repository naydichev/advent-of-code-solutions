#!/usr/bin/env python3

from collections import Counter

def main():
    data = parse_input()

    result = data[2] + data[3] + data[4] + data[7]

    print(f"There are {result} copies of 1, 4, 7, 8")


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    outputs = []
    for line in data:
        parts = line.split(" | ")
        output = parts[1].split(" ")
        outputs.extend(output)

    return Counter([len(x) for x in outputs])


if __name__ == "__main__":
    main()
