#!/usr/bin/env python3


def main():
    starting = sorted(parse_input())

    chosen = starting[len(starting) // 2]

    lowest = calculate_fuel(starting, chosen)
    for i in range(0, starting[-1]):
        fuel = calculate_fuel(starting, i)
        if fuel < lowest:
            lowest = fuel

    print(f"It takes {lowest} fuel")


def calculate_fuel(starting, point):
    fuel = 0
    for loc in starting:
        dist = abs(loc - point)
        fuel += dist * (dist + 1) / 2

    return fuel


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    processed = [int(x) for x in data[0].split(",")]

    return processed


if __name__ == "__main__":
    main()
