#!/usb/bin/env python3


def main():
    with open("input.aoc") as f:
        instructions = [x.strip().split(" ") for x in f.readlines()]

    x, y = 0, 0
    for cmd, rawdist in instructions:
        distance = int(rawdist)

        if cmd == "forward":
            x += distance
        elif cmd == "down":
            y += distance
        else:
            y -= distance

    print(f"Final coordinates: ({x}, {y}). Answer is {x * y}")




if __name__ == "__main__":
    main()
