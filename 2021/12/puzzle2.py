#!/usr/bin/env python3

from collections import defaultdict

def main():
    data = parse_input()

    paths = find_paths(data)
    unique = set(["-".join(p) for p in paths])

    print(f"The total number of paths is {len(unique)}")


def find_paths(data, seen={"start"}, position="start", current=["start"], double=None):
    if position == "end":
        return [current]

    paths = []
    for option in data[position]:
        nseen = seen.copy()
        ncurrent = current[:]
        ncurrent.append(option)

        if option not in seen or option.isupper():
            paths.extend(find_paths(data, nseen | {option}, option, ncurrent, double))

        if double:
            continue

        if not option.isupper():
            nseen.add(option)

        paths.extend(find_paths(data, nseen, option, ncurrent, True))

    return paths


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    caves = defaultdict(list)

    for line in data:
        a, b = line.split("-")

        if b != "start":
            caves[a].append(b)
        if a != "start":
            caves[b].append(a)

    return caves


if __name__ == "__main__":
    main()
