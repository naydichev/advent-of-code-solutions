#!/usr/bin/python

import re
from collections import defaultdict

P = re.compile(r"^position=<(\s?-?\d+), (\s?-?\d+)> velocity=<(\s?-?\d+), (\s?-?\d+)>$")
class Star:
    def __init__(self, x, y, vx, vy):
        self.x = x;
        self.y = y;
        self.velocity_x = vx
        self.velocity_y = vy

    def inc(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

    def __repr__(self):
        return "%s(x=%d, y=%d, vx=%d, vy=%d)" % (self.__class__.__name__, self.x, self.y, self.velocity_x, self.velocity_y)

def main():
    with open("stars.pi") as f:
        raw_stars = f.read().split("\n")

    stars = parse_stars(raw_stars)

    for i in range(40000):
        plot_stars(stars, i)
        [s.inc() for s in stars]

def plot_stars(stars, i):
    min_x = min(stars, key=lambda x: x.x).x
    min_y = min(stars, key=lambda x: x.y).y
    max_x = max(stars, key=lambda x: x.x).x
    max_y = max(stars, key=lambda x: x.y).y

    if max_x - min_x > 300 or max_y - min_y > 300:
        return

    plot = defaultdict(lambda: defaultdict(lambda: "."))
    print("min_x", min_x, "min_y", min_y, "max_x", max_x, "max_y", max_y)

    for star in stars:
        plot[star.x][star.y] = "#"

    with open("%d.stars" % i, "w") as f:
        for y in range(min_y, max_y + 1):
            line = []
            for x in range(min_x, max_x + 1):
                line.append(plot[x][y])

            f.write("".join(line))
            f.write("\n")

def parse_stars(raw_stars):
    stars = []
    for star in raw_stars:
        m = P.match(star)
        if not m:
            print(star)
            continue
        stars.append(Star(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    return stars

if __name__ == "__main__":
    main()
