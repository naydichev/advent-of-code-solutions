#!/usr/bin/env python3

import math
from itertools import combinations
from recordtype import recordtype


Position = recordtype("Position", "x y z")
Velocity = recordtype("Velocity", "x y z")
Moon = recordtype("Moon", "id position velocity")

def main(raw):
    initial = parse(raw)
    moons = parse(raw)

    loop_x = calculate_loop(moons, 0)
    loop_y = calculate_loop(moons, 1)
    loop_z = calculate_loop(moons, 2)

    cylce_time = lcm(loop_x, lcm(loop_y, loop_z))

    print(f"it takes {cylce_time} steps to return to an initial condition")


def calculate_loop(moons, pos):
    moon_pos = [[list(m.position)[pos], list(m.velocity)[pos]] for m in moons]
    first_state = [m.copy() for m in moon_pos]

    steps = 0
    while True:
        for a, b in combinations(moon_pos, 2):
            if a[0] > b[0]:
                a[1] -= 1
                b[1] += 1
            elif b[0] > a[0]:
                a[1] += 1
                b[1] -= 1
        for m in moon_pos:
            m[0] += m[1]

        steps += 1
        print(first_state, moon_pos, first_state == moon_pos)
        if first_state == moon_pos:
            return steps


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


def parse(raw):
    moons = []

    for i, moon in enumerate(raw):
        parts= [int(x.strip()[2:]) for x in moon[1:-1].split(",")]
        moons.append(
            Moon(i, Position(parts[0], parts[1], parts[2]), Velocity(0, 0, 0))
        )

    return moons


if __name__ == "__main__":
    with open("moons.pi") as f:
        main(f.read().strip().split("\n"))
