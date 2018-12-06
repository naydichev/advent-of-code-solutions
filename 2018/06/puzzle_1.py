#!/usr/bin/python

from collections import defaultdict

class Coordinate:
    ID = 0
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.id = Coordinate.ID

        Coordinate.ID += 1

    def distance_from_xy(self, y, x):
        return abs(x - self.center_x) + abs(y - self.center_y)

    def distance_from_coordinate(self, other):
        return self.distance_from_xy(other.center_x, other.center_y)

    def __repr__(self):
        return "Coordinate(x={}, y={}, id={})".format(self.center_x, self.center_y, self.id)


def main():
    with open("coordinates.pi") as f:
        raw_coordinates = f.read().split("\n")

    coordinates = parse_coordinates(raw_coordinates)

    bounds = calculate_bounds(coordinates)

    board = populate_board(bounds, coordinates)

    print("populated board")
    print_board(board, bounds)

    fill_board(board, bounds, coordinates)
    print("filled board")
    print_board(board, bounds)

    max_spaces = calculate_max_spaces(board, bounds)

    print(max_spaces)

def parse_coordinates(raw_coordinates):
    return [ Coordinate(int(x[0]), int(x[1])) for x in (y.split(", ") for y in raw_coordinates) ]

def calculate_bounds(coordinates):
    class Bounds:
        def __init__(self, min_x, min_y, max_x, max_y):
            self.min_x = min_x
            self.min_y = min_y
            self.max_x = max_x
            self.max_y = max_y

        def __repr__(self):
            return "Bounds(min_x={}, min_y={}, max_x={}, max_y={})".format(
                self.min_x,
                self.min_y,
                self.max_x,
                self.max_y
            )

    c1 = coordinates[0]
    bounds = Bounds(c1.center_x, c1.center_y, c1.center_x, c1.center_y)

    for coord in coordinates[1:]:
        if coord.center_x < bounds.min_x:
            bounds.min_x = coord.center_x
        elif coord.center_x > bounds.max_x:
            bounds.max_x = coord.center_x

        if coord.center_y < bounds.min_y:
            bounds.min_y = coord.center_y
        elif coord.center_y > bounds.max_y:
            bounds.max_y = coord.center_y

    return bounds

def populate_board(bounds, coordinates):
    board = defaultdict(lambda: defaultdict(lambda: None))

    for coord in coordinates:
        board[coord.center_x][coord.center_x] = coord

    return board

def fill_board(board, bounds, coordinates):
    for coord in coordinates:
        for i in range(bounds.min_x, bounds.max_x + 1):
            for j in range(bounds.min_y, bounds.max_y + 1):
                if board[i][j] is None:
                    board[i][j] = coord
                    continue

                multiple = False
                if isinstance(board[i][j], list):
                    c = board[i][j][0]
                    multiple = True
                else:
                    c = board[i][j]
                c_dist = c.distance_from_xy(i, j)
                coord_dist = coord.distance_from_xy(i, j)
                if c_dist > coord_dist:
                    board[i][j] = coord
                elif c_dist == coord_dist:
                    if not multiple:
                        board[i][j] = [c]
                    board[i][j].append(coord)

def calculate_max_spaces(board, bounds):
    spaces = defaultdict(int)

    for i in board.keys():
        for j in board[i].keys():
            if board[i][j] is None or isinstance(board[i][j], list):
                board[i][j] = None
                continue

            spaces[board[i][j]] += 1

    for i in range(bounds.min_x, bounds.max_x):
        spaces.pop(board[i][bounds.min_y], None)
        spaces.pop(board[i][bounds.max_y], None)

    for i in range(bounds.min_y, bounds.max_y):
        spaces.pop(board[bounds.min_x][i], None)
        spaces.pop(board[bounds.max_x][i], None)

    return max(spaces.iteritems(), key=lambda x: x[1])[1]

def print_board(board, bounds):
    for i in range(bounds.min_x, bounds.max_x + 1):
        row = []
        for j in range(bounds.min_y, bounds.max_y + 1):
            if board[i][j] is None:
                row.append("[]")
            elif isinstance(board[i][j], list):
                row.append("..")
            else:
                row.append("{:02d}".format(board[i][j].id))

        print(" ".join(row))

if __name__ == "__main__":
    main()
