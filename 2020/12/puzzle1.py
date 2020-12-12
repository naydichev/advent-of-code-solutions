#!/usr/bin/env python3

from collections import namedtuple

Instruction = namedtuple('Instruction', ['code', 'value'])

OPERATIONS = {
    'N': lambda v, x, y, f: (x, y + v, f),
    'E': lambda v, x, y, f: (x + v, y, f),
    'W': lambda v, x, y, f: (x - v, y, f),
    'S': lambda v, x, y, f: (x, y - v, f),
    'R': lambda v, x, y, f: (x, y, turn_right(f, v)),
    'L': lambda v, x, y, f: (x, y, turn_left(f, v)),
    'F': lambda v, x, y, f: OPERATIONS[f](v, x, y, f)
}


def main():
    # with open("sample.pi") as f:
    with open("storm.pi") as f:
        data = parse(f.readlines())

    facing = 'E'
    x, y = 0, 0
    for instruction in data:
        x, y, facing = OPERATIONS[instruction.code](instruction.value, x, y, facing)

    print(f"manhattan distance to ({x}, {y}) = {abs(x) + abs(y)}")


def turn_left(f, v):
    return turn_right(f, ((v + 180) % 360))


def turn_right(f, v):
    if v == 0 or v == 180:
        return dict(N='S', E='W', W='E', S='N')[f]
    elif v == 90:
        return dict(N='E', E='S', S='W', W='N')[f]
    else:
        return dict(N='W', E='N', S='E', W='S')[f]


def parse(raw):
    output = []

    for line in raw:
        output.append(Instruction(line[0], int(line[1:])))

    return output


if __name__ == "__main__":
    main()
