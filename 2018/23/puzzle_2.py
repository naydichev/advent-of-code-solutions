#!/usr/bin/python

from collections import defaultdict
import sys; sys.path.append("/usr/local/lib/python2.7/site-packages")
import z3

class Nanobot:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def __repr__(self):
        return "{}(x={}, y={}, z={}, radius={})".format(self.__class__.__name__, self.x, self.y, self.z, self.radius)

    def in_range(self, x, y, z):
        return (abs(self.x - x) + abs(self.y - y) + abs(self.z - z)) <= self.radius

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __cmp__(self, other):
        if self.z == other.z and self.y == other.y:
            return self.x - other.x
        elif self.z == other.z:
            return self.y - other.y

        return self.z - other.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y  and self.z == other.z

    def __repr__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __hash__(self):
        return hash("({},{},{})".format(self.x, self.y, self.z))

def z3dist(a, b):
    d = a - b
    return z3.If(d >= 0, d, -d)

def manhattan_distance(p1, p2):
    return z3dist(p1[0], p2[0]) + z3dist(p1[1], p2[1]) + z3dist(p1[2], p2[2])

def main(nanobots):
    solver = z3.Optimize()
    bx = z3.Int("x")
    by = z3.Int("y")
    bz = z3.Int("z")
    d = z3.Int("d")

    bots = []
    for i, bot in enumerate(nanobots):
        print("adding bot {} to z3".format(i))
        b = z3.Int("b{:04}".format(i))
        solver.add(b == z3.If(manhattan_distance((bx, by, bz), (bot.x, bot.y, bot.z)) <= bot.radius, 1, 0))
        bots.append(b)

    print("adding constraints")
    solver.add(d == manhattan_distance((bx, by, bz), (0, 0, 0)))
    solver.maximize(z3.Sum(*bots))
    solver.minimize(d)

    print("solving...")
    print(solver.check())

    model = solver.model()
    print("answer:")
    print(model[d])

def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)

if __name__ == "__main__":
    with open("nanobots.pi") as f:
        raw = f.read().split("\n")

    nanobots = []
    for row in raw:
        rpos, rr =  row.split(" ")
        x, y, z = [int(p) for p in rpos[5:-2].split(",")]
        radius = int(rr.split("=")[1])

        nanobots.append(Nanobot(x, y, z, radius))

    main(nanobots)
