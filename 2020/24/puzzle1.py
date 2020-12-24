#!/usr/bin/env python3

from collections import defaultdict

DIRECTIONS = {
    'e': (2, 0),
    'w': (-2, 0),
    'ne': (1, 1),
    'nw': (-1, 1),
    'se': (1, -1),
    'sw': (-1, -1)
}

BLACK = "black"
WHITE = "white"

def main():
    with open("hexes.pi") as f:
        data = parse(f.readlines())

    grid = defaultdict(lambda: defaultdict(lambda: WHITE))

    num_black = 0
    for line in data:
        hexx, hexy = find_hex(line)

        color = grid[hexy][hexx]
        new_color = BLACK
        if color == WHITE:
            num_black += 1
        else:
            num_black -= 1
            new_color = WHITE

        grid[hexy][hexx] = new_color

    print(f"there are {num_black} black hexes")


def find_hex(line):
    instr = list(line)


    x, y = 0, 0
    while len(instr):
        direction = instr.pop(0)
        if direction not in ['e', 'w']:
            direction = f"{direction}{instr.pop(0)}"

        adj = DIRECTIONS[direction]
        x += adj[0]
        y += adj[1]

    return x, y


def parse(raw):
    output = []

    for line in raw:
        output.append(line.strip())

    return output


if __name__ == "__main__":
    main()
