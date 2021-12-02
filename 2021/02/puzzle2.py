#!/usb/bin/env python3


def main():
    with open("input.aoc") as f:
        instructions = [x.strip().split(" ") for x in f.readlines()]

    x, y, aim = 0, 0, 0
    for cmd, rawdist in instructions:
        distance = int(rawdist)

        if cmd == "down":
            aim += distance
        elif cmd == "up":
            aim -= distance
        else:
            x += distance
            y += (distance * aim)

    print(f"Final coordinates: ({x}, {y}). Answer is {x * y}")




if __name__ == "__main__":
    main()
