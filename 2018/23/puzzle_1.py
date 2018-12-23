#!/usr/bin/python

class Nanobot:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def __repr__(self):
        return "{}(x={}, y={}, z={}, radius={})".format(self.__class__.__name__, self.x, self.y, self.z, self.radius)

def main(nanobots):
    max_reach_nanobot = max(nanobots, key=lambda k: k.radius)


    in_radius = 0
    for nanobot in nanobots:
        if distance(nanobot, max_reach_nanobot) <= max_reach_nanobot.radius:
            in_radius += 1

    print("there are {} nanobots in range".format(in_radius))

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
