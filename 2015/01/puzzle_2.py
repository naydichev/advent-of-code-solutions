#!/usr/bin/env python3

with open("input.pi") as f:
    line = f.read()

    floor = 0
    position = 0

    for c in line:
        position += 1
        if c is "(":
            floor += 1
        elif c is ")":
            floor -= 1

        if floor == -1:
            print(f"basement on position {position}")
            break
