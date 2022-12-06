#!/usr/bin/env python3

import re

from collections import defaultdict


def main():
    data = parse_input()

    current = 20151125

    target_row, target_column = data

    iterations = sum(
        range(target_row + target_column - 1)
        ) + target_column

    for _ in range(iterations - 1):
        current = calculate(current)

    print(f"Part One: {current}")


def calculate(code):
    return (code * 252533) % 33554393


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    match = re.findall(r'row (\d+), column (\d+)', data[0])
    processed = map(int, match[0])

    return list(processed)


if __name__ == "__main__":
    main()
