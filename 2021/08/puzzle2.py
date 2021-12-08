#!/usr/bin/env python3

from collections import Counter, namedtuple

SegmentData = namedtuple("SegmentData", "inputs, outputs")

digits = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg"
]

digits_to_values = {i: v for i, v in enumerate(digits)}

values_to_digits = {v: k for k, v in digits_to_values.items()}

def main():
    segmentdata = parse_input()

    total = 0
    for segment in segmentdata:
        total += decrypt_segment(segment)

    print(f"The total value of all segments is {total}")


def decrypt_segment(segment):
    # start with the easy ones
    mapping = determine_mapping(segment.inputs)

    num = []
    for o in segment.outputs:
        mapped = "".join(sorted([mapping[l] for l in o]))

        num.append(digits.index(mapped))

    return int("".join(map(str, num)))


def determine_mapping(inputs):
    mapping = dict()

    one = set([x for x in inputs if len(x) == 2][0])
    four = set([x for x in inputs if len(x) == 4][0])
    seven = set([x for x in inputs if len(x) == 3][0])

    mapping["a"] = (seven - one).pop()

    fourp = set(four)
    fourp.add(mapping["a"])
    nine = set([x for x in inputs if len(x) == 6 and (len(set(x) - fourp) + len(fourp - set(x))) == 1][0])

    mapping["g"] = (nine - fourp).pop()

    fourpp = set(four) - one
    fourpp.add(mapping["a"])
    fourpp.add(mapping["g"])

    five = set([x for x in inputs if len(x) == 5 and (len(set(x) - fourpp) + len(fourpp - set(x))) == 1][0])

    mapping["f"] = (five - fourpp).pop()
    mapping["c"] = (one - set(mapping["f"])).pop()

    mthree = set([mapping["a"], mapping["c"], mapping["f"], mapping["g"]])

    three = set([x for x in inputs if len(x) == 5 and (len(set(x) - mthree) + len(mthree - set(x))) == 1][0])

    mapping["d"] = (three - mthree).pop()
    mapping["b"] = (four - one - set(mapping["d"])).pop()

    eight = set([x for x in inputs if len(x) == 7][0])

    mapping["e"] = (eight - set(mapping.values())).pop()

    return {v: k for k, v in mapping.items()}

def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    transform = lambda part: ["".join(sorted(p)) for p in part.split(" ")]
    all_outputs = []
    for line in data:
        parts = line.split(" | ")
        inputs = transform(parts[0])
        outputs = transform(parts[1])
        all_outputs.append(SegmentData(inputs, outputs))

    return all_outputs


if __name__ == "__main__":
    main()
