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

    grid = build_grid(data)

    num_black = 0
    for i in range(100):
        new_grid = empty_grid()
        num_black = 0

        miny = min(grid.keys()) - 1
        maxy = max(grid.keys()) + 1
        minx = min([min(g.keys()) for g in [g for g in grid.values()]]) - 1
        maxx = max([max(g.keys()) for g in [g for g in grid.values()]]) + 1

        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                color = grid[y][x]
                my_neighbors = neighbors(grid, x, y)
                black_neighbors = my_neighbors.count(BLACK)

                new_color = color
                if color == BLACK and (black_neighbors == 0 or black_neighbors > 2):
                    new_color = WHITE

                if color == WHITE and black_neighbors == 2:
                    new_color = BLACK

                new_grid[y][x] = new_color
                if new_color == BLACK:
                    num_black += 1

        grid = new_grid

    print(f"after 100 times, there are {num_black} black tiles")


def neighbors(grid, x, y):
    return [grid[y + dy][x + dx] for dx, dy in DIRECTIONS.values()]


def empty_grid():
    return defaultdict(lambda: defaultdict(lambda: WHITE))


def build_grid(data):
    grid = empty_grid()


    for line in data:
        hexx, hexy = find_hex(line)

        color = grid[hexy][hexx]
        new_color = BLACK
        if color != WHITE:
            new_color = WHITE

        grid[hexy][hexx] = new_color

    return grid


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
