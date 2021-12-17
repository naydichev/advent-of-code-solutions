#!/usr/bin/env python3


def main():
    data = parse_input()

    highest_y = 0

    for yvel in range(1, 200):
        for xvel in range(1, 200):
            hits, maxy = shoot((xvel, yvel), data)

            if hits and maxy > highest_y:
                highest_y = maxy

    print(f"The highest y goes is {highest_y}")


def shoot(velocity, bounds):
    x, y = 0, 0
    xbound, ybound = bounds
    highest_y = 0
    xvel, yvel = velocity

    while x < xbound[1]:
        if x >= xbound[0] and x <= xbound[1] and y >= ybound[0] and y <= ybound[1]:
            return True, highest_y

        elif y < ybound[0]:
            break

        x += xvel
        y += yvel

        if y > highest_y:
            highest_y = y

        if xvel > 0:
            xvel -= 1
        elif xvel < 0:
            xvel += 1

        yvel -= 1

    return False, None


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
