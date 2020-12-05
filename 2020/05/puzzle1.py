#!/usr/bin/env python3

from collections import namedtuple

RowAndColumn = namedtuple("RowAndColumn", ["row", "column"])


def main():
    with open("seats.pi") as f:
        seats = parse(f.readlines())

    seatids = [s.row * 8 + s.column for s in seats]

    biggest = max(seatids)

    print(f"highest seat id is {biggest}")


def parse(raw):
    parsed = []

    for row in raw:
        row = row.strip()
        seat = int(row[:-3].replace("F", "0").replace("B", "1"), 2)
        col  = int(row[-3:].replace("L", "0").replace("R", "1"), 2)

        parsed.append(RowAndColumn(seat, col))

    return parsed


if __name__ == "__main__":
    main()
