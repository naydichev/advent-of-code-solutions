#!/usr/bin/env python3

import re

NUMBER_PATTERN = re.compile(r"(-?\d+)")


def main(blob):
    numbers = []
    match = NUMBER_PATTERN.search(blob)

    while match is not None:
        numbers.append(int(match.group(1)))

        match = NUMBER_PATTERN.search(blob, match.end() + 1)

    print(f"the sum of all the numbers: {sum(numbers)}")


if __name__ == "__main__":
    with open("json.pi") as f:
        main(f.read().rstrip())
