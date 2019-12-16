#!/usr/bin/env python3

import itertools


def main(digits, offset, phases=100):
    digits = digits * 10000
    for _ in range(phases):
        digits = apply_phase(digits, offset)

    first_eight = ''.join(str(i) for i in digits[offset:offset+8])
    print(f"the first 8 digits are {first_eight}")


def apply_phase(digits, offset):
    num_digits = len(digits)
    partial = sum(digits[i] for i in range(offset, num_digits))

    for i in range(offset, num_digits):
        d = digits[i]
        digits[i] = abs(partial) % 10
        partial -= d

    return digits


if __name__ == "__main__":
    with open("digits.pi") as f:
        digits = f.read().strip()
        offset = int(digits[:7], 10)
        main(list(map(int, digits)), offset)
