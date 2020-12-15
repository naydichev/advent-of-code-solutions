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

        binary = list(f"{address:b}".zfill(36))

        for index, char in enumerate(mask):
            if char == "0":
                continue

            binary[index] = char

        addresses = []
        count = mask.count("X")
        for i in range(pow(2, count)):
            b = list(f"{i:b}".zfill(count))
            local = binary[:]

            n = mask.find("X")

            while n != -1:
                local[n] = b.pop(0)
                n = mask.find("X", n + 1)

            address = int("".join(local), 2)
            addresses.append(address)


        for address in addresses:
            mem[address] = value

    print(f"the sum of all values in memory {sum(mem.values())}")


def parse(raw):
    output = []

    for line in raw:
        output.append(line)

    return output


if __name__ == "__main__":
    main()
