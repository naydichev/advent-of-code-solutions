#!/usr/bin/python

from copy import deepcopy

def main():
    with open("instructions.pi") as f:
        raw_steps = f.read().split("\n")

    steps = parse_steps(raw_steps)

    order = determine_step_order(steps)
    print(order)


def parse_steps(raw_steps):
    steps = {chr(k): set() for k in range(ord('A'), ord('Z') + 1)}

    for step in raw_steps:
        parts = step.split()
        steps[parts[-3]].add(parts[1])

    return steps

def determine_step_order(steps):
    my_steps = deepcopy(steps)
    letters = []

    while len(my_steps):
        next_step = sorted([key for key, val in my_steps.items() if len(val) == 0])[0]

        letters.append(next_step)
        del my_steps[next_step]
        for key in my_steps.keys():
            my_steps[key].discard(next_step)

    return "".join(letters)

if __name__ == "__main__":
    main()
