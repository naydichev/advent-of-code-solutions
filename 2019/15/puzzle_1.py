#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from threading import Thread
from intcode import run_program

Point = namedtuple("Point", ["x", "y"])

EMPTY = None
WALL = 0
VALID = 1
DESTINATION = 2

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIRECTIONS = {
    NORTH: (0, 1),
    SOUTH: (0, -1),
    WEST: (1, 0),
    EAST: (-1, 0)
}


def update_position(position, direction_moved):
    d = DIRECTIONS[direction_moved]
    return Point(position.x + d[0], position.y + d[1])


def valid_moves(ship, position):
    # first find valid_directions
    new_positions = {d: update_position(position, d) for d in DIRECTIONS}
    valid_positions = {d: p for d, p in new_positions.items() if ship[p] != WALL}

    return valid_positions


D = {
    WALL: "#",
    VALID: ".",
    EMPTY: "?",
    DESTINATION: "*"
}

FG_RED = "\33[31m"
FG_BLUE = "\33[34m"
RESET = "\33[0m"


def print_map(ship, target=None, color=FG_RED):
    all_points = ship.keys()
    min_y = min([p.y for p in all_points])
    max_y = max([p.y for p in all_points])
    min_x = min([p.x for p in all_points])
    max_x = max([p.x for p in all_points])

    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            m = D[ship[p]]
            if target == p:
                line.append(f"{color}{m}{RESET}")
            else:
                line.append(m)

        print("".join(line))

    print()


def compute_move(ship, position, moves):
    valid_positions = valid_moves(ship, position)

    # print_map(ship, position)

    if len(valid_positions) == 1:
        return list(valid_positions.keys())

    for d, p in valid_positions.items():
        if ship[p] == EMPTY:
            return [d]

    path = find_path(ship, position, EMPTY, [], set())
    return path


def main(instructions):
    ship = defaultdict(lambda: EMPTY)
    position = Point(0, 0)
    ship[position] = VALID
    moves = []
    computed_path = []
    map_done = False

    def program_output(output):
        nonlocal position, ship

        attempted_position = update_position(position, moves[-1])
        if output == 2:
            position = attempted_position
            ship[position] = DESTINATION
        elif output == 0:
            attempted_position = update_position(position, moves[-1])
            ship[attempted_position] = WALL
        else:
            position = attempted_position
            ship[position] = VALID

    def program_input():
        if len(computed_path) == 0:
            path = compute_move(ship, position, moves)
            if path is None:
                nonlocal map_done
                # we've explored the whole map
                map_done = True
                return None
            computed_path.extend(path)

        next_move = computed_path.pop(0)
        moves.append(next_move)
        return next_move

    program = Thread(target=run_program, args=(instructions, program_input, program_output), kwargs=dict(debug=False),
                     name="program-thread", daemon=True)
    program.start()
    while not map_done:
        program.join(timeout=3)

    print("map has been generated")
    destination_point = [p for p, v in ship.items() if v == DESTINATION][0]
    print_map(ship, destination_point)

    # find shortest path
    path = find_path(ship, Point(0, 0), DESTINATION, [], set())
    print(f"shortest path to the target is {len(path)}")


def find_path(ship, position, target, moves=[], visited=set()):
    valid = valid_moves(ship, position)
    if target == DESTINATION:
        print_map(ship, position, FG_BLUE)
    options = []

    visited.add(position)

    for m, p in valid.items():
        if p in visited:
            continue

        new_moves = moves + [m]
        if ship[p] == target:
            return new_moves

        options.append(find_path(ship, p, target, new_moves, visited))

    filtered = list(filter(None, options))
    if len(filtered) == 0:
        return None
    return min(filtered, key=lambda p: len(p))


if __name__ == "__main__":
    with open("program.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")])
