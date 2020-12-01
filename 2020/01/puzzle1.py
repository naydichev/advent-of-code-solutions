#!/usr/bin/env python3


def main():
    with open("day1.pi") as f:
        numbers = [int(n) for n in f.readlines()]

    digits = None

    while digits is None:
        n1 = numbers.pop(0)

        for n2 in numbers:
            if n1 + n2 == 2020:
                digits = n1, n2
                break

    print(f"{n1} + {n2} = {n1 + n2}")
    print(f"{n1} * {n2} = {n1 * n2}")


if __name__ == "__main__":
    main()
