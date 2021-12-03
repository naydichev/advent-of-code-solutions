#!/usr/bin/env python3

from functools import partial


def main():
    data = parse_input()

    def o2func(avg, pos, num):
        d = 0
        if avg >= 0.5:
            d = 1

        return num[pos] == d

    def co2func(avg, pos, num):
        d = 1
        if avg >= 0.5:
            d = 0

        return num[pos] == d


    o2 = calculate_value(data, o2func)
    co2 = calculate_value(data, co2func)

    o2int = int("".join([str(i) for i in o2]), 2)
    co2int = int("".join([str(i) for i in co2]), 2)

    print(f"Answer is {o2int * co2int}")


def calculate_value(data, func, pos=0):
    if len(data) == 1:
        return data[0]

    s = 0
    for d in data:
        s += d[pos]

    avg = (s * 1.0) / len(data)
    pfunc = partial(func, avg, pos)
    return calculate_value(list(filter(pfunc, data)), func, pos + 1)


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    processed = []
    for d in data:
        processed.append([int(y) for y in d])

    return processed


if __name__ == "__main__":
    main()
