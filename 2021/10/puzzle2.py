#!/usr/bin/env python3

from queue import LifoQueue


scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
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

    totals = []
    for line in data:
        q = LifoQueue()
        corrupt = False

        for c in line:
            if c in openers:
                q.put(c)
            else:
                o = q.get()

                if matches[o] != c:
                    corrupt = True

                    break
        if corrupt:
            continue

        localscore = 0
        while not q.empty():
            localscore *= 5
            localscore += scores[matches[q.get()]]

        if localscore > 0:
            totals.append(localscore)


    print(f"Total score is {sorted(totals)[len(totals) // 2]}")



def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    processed = data

    return processed


if __name__ == "__main__":
    main()
