#!/usr/bin/env python3

from collections import namedtuple

RowAndColumn = namedtuple("RowAndColumn", ["row", "column"])


def main():
    with open("seats.pi") as f:
        seats = parse(f.readlines())

    sid = lambda seat: seat.row * 8 + seat.column
    sids = sorted([sid(seat) for seat in seats])

    prev = sids[0]
    for i, seatid in enumerate(sids[1:]):
        if prev + 2 == seatid:
            print(f"{seatid - 1} is your sid")
            break

        prev = seatid


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
