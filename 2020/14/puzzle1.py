#!/usr/bin/env python3

from collections import defaultdict
import re

MEM_PATTERN = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def main():
    # with open("sample.pi") as f:
    with open("bitmask.pi") as f:
        program = parse(f.readlines())

    mask = None
    mem = defaultdict(int)

    for line in program:
        if line.startswith("mask ="):
            mask = line.strip().split(" ")[2]
            continue

        match = MEM_PATTERN.match(line)
        address = int(match.group(1))
        value = int(match.group(2))

        binary = list(f"{value:b}".zfill(36))

        for index, char in enumerate(mask):
            if char == "X":
                continue

            binary[index] = char

        value = int("".join(binary), 2)
        mem[address] = value

    print(f"the sum of all values in memory {sum(mem.values())}")


def parse(raw):
    output = []

    for line in raw:
        output.append(line)

    return output


if __name__ == "__main__":
    main()
