#!/usr/bin/python

import re

PATTERN = re.compile(r"^#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)$")

def main():
    with open("fabric_data.pi") as f:
        raw_fabric_data = [x.strip() for x in f.readlines()]

    fabric_data = [parse_fabric_data(x) for x in raw_fabric_data]

    overlap_count = compute_overlaps(fabric_data)

    print("There are %d overlaps" % overlap_count)


def parse_fabric_data(fabric_item):
    match = PATTERN.match(fabric_item)

    return {
        "id": match.group(1),
        "left": int(match.group(2)),
        "top": int(match.group(3)),
        "width": int(match.group(4)),
        "height": int(match.group(5))
    }

def compute_overlaps(fabric_data):
    fabric = dict()

    for datum in fabric_data:
        for i in range(datum["left"], datum["left"] + datum["width"]):
            for j in range(datum["top"], datum["top"] + datum["height"]):
                fabric.setdefault(i, dict()).setdefault(j, []).append(datum["id"])

    overlaps = 0
    for i in fabric.keys():
        for j in fabric[i].keys():
            if len(fabric[i][j]) > 1:
                overlaps += 1

    return overlaps

if __name__ == "__main__":
    main()
