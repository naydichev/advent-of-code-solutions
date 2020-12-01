#!/usr/bin/env python3


def main():
    with open("day1.pi") as f:
        numbers = [int(n) for n in f.readlines()]

    digits = None

    while digits is None and len(numbers):
        n1 = numbers.pop(0)

        for n2 in numbers:
            diff = 2020 - n1 - n2
            if diff in numbers:
                n3 = diff
                digits = n1, n2, n3
                break

    print(f"{n1} + {n2} + {n3} = {n1 + n2 + n3}")
    print(f"{n1} * {n2} * {n3} = {n1 * n2 * n3}")


if __name__ == "__main__":
    main()
