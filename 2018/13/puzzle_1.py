#!/usr/bin/python

from collections import defaultdict

UP = '^'
LEFT = '<'
DOWN = 'v'
RIGHT = '>'
RIGHT_TURN = '/'
LEFT_TURN = '\\'
INTERSECTION = '+'
NORTH_SOUTH = "|"
EAST_WEST = "-"

DIRECTIONS = [UP, LEFT, RIGHT, DOWN]
TRACKS = [LEFT_TURN, RIGHT_TURN, INTERSECTION, NORTH_SOUTH, EAST_WEST]

DIRECTION_TO_TRACK = {
    UP: NORTH_SOUTH,
    DOWN: NORTH_SOUTH,
    LEFT: EAST_WEST,
    RIGHT: EAST_WEST
}

TRACK_TO_DIRECTION = {
    LEFT_TURN: {
        UP: LEFT,
        RIGHT: DOWN,
        DOWN: RIGHT,
        LEFT: UP
    },
    RIGHT_TURN: {
        UP: RIGHT,
        RIGHT: UP,
        DOWN: LEFT,
        LEFT: DOWN
    }
}


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)

class Track:
    def __init__(self, direction, cart=None):
        self.direction = direction
        self.cart = cart
        self.collision = False

    def collide(self):
        self.collision = True

    def __repr__(self):
        if self.collision:
            return "X"
        elif self.cart is not None:
            return str(self.cart)
        else:
            return self.direction

    __str__ = __repr__

class Cart:
    def __init__(self, direction, location):
        self.location = location
        self.direction = direction
        self.turns = 0

    def turn(self):
        self.turns += 1
        # first turn
        if self.turns % 3 == 1:
            # LEFT
            if self.direction == UP:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = DOWN
            elif self.direction == RIGHT:
                self.direction = UP
            else:
                self.direction = RIGHT

        # second turn
        elif self.turns % 3 == 2:
            # STRAIGHT - do nothing
            pass
        # third turn
        else:
            # RIGHT
            if self.direction == UP:
                self.direction = RIGHT
            elif self.direction == LEFT:
                self.direction = UP
            elif self.direction == RIGHT:
                self.direction = DOWN
            else:
                self.direction = LEFT

    def __repr__(self):
        return self.direction

    __str__ = __repr__

    def __cmp__(self, other):
        if self.location.y == other.location.y:
            return self.location.x - other.location.x

        return self.location.y - other.location.y

def main():
    with open("tracks.pi") as f:
        raw_tracks = f.read().split("\n")

    tracks, carts = parse(raw_tracks)

    # print_tracks(tracks)

    collision = None
    while collision is None:
        collision = tick(tracks, carts)

    print_tracks(tracks)
    print("collision at", collision)

def print_tracks(tracks):
    maxX, maxY = find_max(tracks)

    for y in range(maxY + 1):
        row = []
        for x in range(maxX + 1):
            if y in tracks[x]:
                row.append(str(tracks[x][y]))
            else:
                row.append(" ")
        print("".join(row))


def parse(raw):
    tracks = defaultdict(dict)
    carts = []

    for y, row in enumerate(raw):
        for x, col in enumerate(row):
            if col in DIRECTIONS:
                cart = Cart(col, Location(x, y))
                carts.append(cart)
                tracks[x][y] = Track(DIRECTION_TO_TRACK[col], cart)
            elif col in TRACKS:
                tracks[x][y] = Track(col)

    return tracks, carts

def find_max(tracks):
    return  max(tracks.keys()), max([max(t.keys()) for t in tracks.values()])

def tick(tracks, carts):
    for cart in sorted(carts):
        x = cart.location.x
        y = cart.location.y
        newX = x
        newY = y

        if cart.direction == UP:
            newY = y - 1
        elif cart.direction == DOWN:
            newY = y + 1
        elif cart.direction == LEFT:
            newX = x - 1
        elif cart.direction == RIGHT:
            newX = x + 1

        direction = tracks[newX][newY].direction
        if direction == INTERSECTION:
            cart.turn()
        elif direction in [LEFT_TURN, RIGHT_TURN]:
            cart.direction = TRACK_TO_DIRECTION[direction][cart.direction]

        cart.location.x = newX
        cart.location.y = newY
        tracks[x][y].cart = None

        if tracks[newX][newY].cart is not None:
            tracks[newX][newY].collide()
            return (newX, newY)

        tracks[newX][newY].cart = cart


if __name__ == "__main__":
    main()
