#!/usr/bin/env python3


def main():
    data = parse_input()

    digits = [0] * len(data[0])

    for entry in data:
        for i, n in enumerate(entry):
            digits[i] += int(n)

    tlen = len(data)

    gamma = []
    epsilon = []

    for digit in digits:
        avg = (digit * 1.0) / tlen
        if avg >= 0.5:
            g = 1
            e = 0
        else:
            g = 0
            e = 1

        gamma.append(str(g))
        epsilon.append(str(e))

    gammaint = int("".join(gamma), 2)
    epsilonint = int("".join(epsilon), 2)

    print(f"Answer is {gammaint * epsilonint}")


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    processed = data

    return processed


if __name__ == "__main__":
    main()
