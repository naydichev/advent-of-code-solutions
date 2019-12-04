#!/usr/bin/env python3

import re

DUPLICATE_PATTERN = re.compile(r"(\d)(\1*)")


def main(sequence, n=40):
    seq = str(sequence)

    for i in range(n):
        seq = iteration(seq)

    print(f"after {n} iterations, we get {len(seq)}")


def iteration(sequence):
    new_seq = []

    c = 0
    while c < len(sequence):
        i = sequence[c]

        match = DUPLICATE_PATTERN.match(sequence, c)
        n = 1

        if match:
            span = match.span()
            n = len(match.group(0))
        new_seq.append(str(n))
        new_seq.append(i)

        c += n

    return "".join(new_seq)


if __name__ == "__main__":
    main(1113222113)
