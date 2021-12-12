#!/usr/bin/env python3

from collections import defaultdict

def main():
    data = parse_input()

    paths = find_paths(data)
    unique = set(["-".join(p) for p in paths])

    print(f"The total number of paths is {len(unique)}")


def find_paths(data, seen={"start"}, position="start", current=["start"]):
    if position == "end":
        return [current]

    paths = []
    for option in data[position]:
        if option in seen:
            continue

        nseen = seen.copy()
        if not option.isupper():
            nseen.add(option)

        ncurrent = current[:]
        ncurrent.append(option)

        paths.extend(find_paths(data, nseen, option, ncurrent))

    return paths


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    caves = defaultdict(list)

    for line in data:
        a, b = line.split("-")

        caves[a].append(b)
        caves[b].append(a)

    return caves


if __name__ == "__main__":
    main()
