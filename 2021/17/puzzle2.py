#!/usr/bin/env python3


def main():
    data = parse_input()

    num_hits = 0

    for yvel in range(-150, 250):
        for xvel in range(0, 250):
            hits = shoot((xvel, yvel), data)

            if hits:
                num_hits += 1

    print(f"Hit the target {num_hits} times")


def shoot(velocity, bounds):
    x, y = 0, 0
    xbound, ybound = bounds
    xvel, yvel = velocity

    while x <= xbound[1]:
        if x >= xbound[0] and x <= xbound[1] and y >= ybound[0] and y <= ybound[1]:
            return True

        elif y < ybound[0]:
            break

        x += xvel
        y += yvel

        if xvel > 0:
            xvel -= 1
        elif xvel < 0:
            xvel += 1

        yvel -= 1

    return False


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()][0]

    _, target = data.split(": ")
    xrange, yrange = target.split(", ")
    _, xrange = xrange.split("=")
    _, yrange = yrange.split("=")
    xmin, xmax = map(int, xrange.split(".."))
    ymin, ymax = map(int, yrange.split(".."))

    return [(xmin, xmax), (ymin, ymax)]


if __name__ == "__main__":
    main()
