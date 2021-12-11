#!/usr/bin/env python3

from queue import Queue

ymax = 10
xmax = 10

def main():
    data = parse_input()

    # p(data, 0)

    step = 0
    while True:
        flashes = take_step(data)

        step += 1

        if flashes == 100:
            break
        # p(data, _ + 1)

    print(f"They all flash at step {step}")


def p(data, i):
    print(f"After step {i}")
    for row in data:
        print("".join(map(str, row)))

    print("")

def take_step(data):
    flashes = []
    to_flash = Queue()
    for y in range(ymax):
        for x in range(xmax):
            data[y][x] += 1

            if data[y][x] > 9:
                to_flash.put((x, y))
                flashes.append((x, y))

    while not to_flash.empty():
        x, y = to_flash.get()


        for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx = x + dx
            ny = y + dy

            if nx < 0 or nx >= xmax:
                continue
            elif ny < 0 or ny >= ymax:
                continue

            data[ny][nx] += 1
            if data[ny][nx] > 9 and (nx, ny) not in flashes:
                to_flash.put((nx, ny))
                flashes.append((nx, ny))

    for x, y in flashes:
        data[y][x] = 0

    return len(flashes)


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    processed = [[int(x) for x in line] for line in data]

    return processed


if __name__ == "__main__":
    main()
