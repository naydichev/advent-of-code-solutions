#!/usr/bin/env python3

from collections import namedtuple

Instruction = namedtuple('Instruction', ['code', 'value'])

OPERATIONS = {
    'N': lambda v, wx, wy, x, y: (wx, wy + v, x, y),
    'E': lambda v, wx, wy, x, y: (wx + v, wy, x, y),
    'W': lambda v, wx, wy, x, y: (wx - v, wy, x, y),
    'S': lambda v, wx, wy, x, y: (wx, wy - v, x, y),
    'R': lambda v, wx, wy, x, y: rotate_waypoint_right(v, wx, wy, x, y),
    'L': lambda v, wx, wy, x, y: rotate_waypoint_left(v, wx, wy, x, y),
    'F': lambda v, wx, wy, x, y: (wx, wy, x + (v * wx), y + (v * wy))
}


def main():
    # with open("sample.pi") as f:
    with open("storm.pi") as f:
        data = parse(f.readlines())

    wx, wy, x, y = 10, 1, 0, 0

    for instruction in data:
        wx, wy, x, y = OPERATIONS[instruction.code](
                instruction.value,
                wx,
                wy,
                x,
                y)

    print(f"manhattan distance to ({x}, {y}) = {abs(x) + abs(y)}")


def rotate_waypoint_right(v, wx, wy, x, y):
    if v == 0 or v == 180:
        return -wx, -wy, x, y
    elif v == 90:
        return wy, -wx, x, y
    else:
        return -wy, wx, x, y


def rotate_waypoint_left(v, wx, wy, x, y):
    return rotate_waypoint_right(((v + 180) % 360), wx, wy, x, y)


def parse(raw):
    output = []

    for line in raw:
        output.append(Instruction(line[0], int(line[1:])))

    return output


if __name__ == "__main__":
    main()
