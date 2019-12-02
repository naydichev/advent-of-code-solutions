#!/usr/bin/env python3

with open("input.pi") as f:
    line = f.read()

    floor = 0
    for c in line:
        if c is "(":
            floor += 1
        elif c is ")":
            floor -= 1

    print(f"he's on floor {floor}")
