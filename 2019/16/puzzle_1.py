#!/usr/bin/env python3

import itertools

PATTERN = [0, 1, 0, -1]


def main(digits, phases=100):

    for _ in range(phases):
        digits = apply_phase(digits)


    first_eight = ''.join(str(i) for i in digits[0:8])
    print(f"the first 8 digits are {first_eight}")


def apply_phase(digits):
    post_phase_digits = []
    for i in range(1, len(digits) + 1):
        phase_pattern = list(itertools.chain.from_iterable([[j] * i for j in PATTERN]))
        phase_pattern = phase_pattern[1:] + [phase_pattern[0]]
        phase_digits = []

        for j, d in enumerate(digits):
            idx = j % len(phase_pattern)
            phase_digits.append(d * phase_pattern[idx])

        post_phase_digits.append(abs(sum(phase_digits)) % 10)

    return post_phase_digits

if __name__ == "__main__":
    with open("digits.pi") as f:
        main([int(i) for i in f.read().strip()])
