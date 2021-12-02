#!/usb/bin/env python3


def main():
    with open("input.aoc") as f:
        depths = [int(x.strip()) for x in f.readlines()]

    windows = []

    for i in range(len(depths) - 2):
        windows.append(sum(depths[i : i + 3]))

    current = windows.pop(0)
    increases = 0

    for depth in windows:
        if depth > current:
            increases = increases + 1

        current = depth

    print(f"The depth increases {increases} times.")


if __name__ == "__main__":
    main()
