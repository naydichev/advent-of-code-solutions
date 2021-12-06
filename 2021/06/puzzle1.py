#!/usr/bin/env python3

from collections import Counter


def main():
    fishes = Counter(parse_input())

    for day in range(80):
        new_fishes = Counter()
        for timer in fishes:
            if timer == 0:
                new_fishes[6] += fishes[timer]
                new_fishes[8] =  fishes[timer]
            else:
                new_fishes[timer - 1] += fishes[timer]
        fishes = new_fishes.copy()

    print(f"After 80 days {sum(fishes.values())}")


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    return [int(x) for x in data[0].split(",")]


if __name__ == "__main__":
    main()
