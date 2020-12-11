#!/usr/bin/env python3

EMPTY_SEAT = "L"
FILLED_SEAT = "#"
FLOOR = "."

def main():
    # with open("sample.pi") as f:
    with open("seats.pi") as f:
        layout = parse(f.readlines())

    seats_changed = True

    while seats_changed:
        seats_changed = do_iteration(layout)

    total_occupied = sum([row.count(FILLED_SEAT) for row in layout])

    print(f"there are {total_occupied} seats occupied")


def do_iteration(layout):
    seats_changed = False
    local = [row[:] for row in layout]

    print_layout(local)
    print()
    for y, row in enumerate(local):
        for x, col in enumerate(row):
            if col == FLOOR:
                continue

            if col == EMPTY_SEAT and no_occupied_seats(local, x, y):
                layout[y][x] = FILLED_SEAT
                seats_changed = True
            elif col == FILLED_SEAT and adjacent_occupied(local, x, y) >= 5:
                layout[y][x] = EMPTY_SEAT
                seats_changed = True

    return seats_changed


def no_occupied_seats(layout, x, y):
    return all([seat != FILLED_SEAT for seat in get_adjacent_items(layout, x, y)])


def adjacent_occupied(layout, x, y):
    return sum([1 if seat == FILLED_SEAT else 0 for seat in get_adjacent_items(layout, x, y)])


def get_adjacent_items(layout, x, y):
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    adjacents = []
    for dx, dy in directions:
        i = 0
        while True:
            i += 1
            nx = x + (dx * i)
            ny = y + (dy * i)

            if ny < 0 or ny >= len(layout):
                break

            row = layout[ny]

            if nx < 0 or nx >= len(row):
                break

            if row[nx] != FLOOR:
                adjacents.append(row[nx])
                break

    return adjacents


def print_layout(layout):
    for row in layout:
        print("".join(row))


def parse(raw):
    output = []

    for line in raw:
        output.append(list(line.strip()))

    return output


if __name__ == "__main__":
    main()
