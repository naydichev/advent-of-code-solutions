#!/usr/bin/env python3

from queue import LifoQueue


scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

openers = "([{<"
closers = ")]}>"
matches = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

def main():
    data = parse_input()

    total = 0
    for line in data:
        q = LifoQueue()

        for c in line:
            if c in openers:
                q.put(c)
            else:
                o = q.get()

                if matches[o] != c:
                    total += scores[c]

                    break

    print(f"Total score is {total}")



def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    processed = data

    return processed


if __name__ == "__main__":
    main()
