#!/usr/bin/env python3

import re
from collections import defaultdict


def main(raw_lights):
    lights = parse(raw_lights)

    total = sum(lights.values())

    print(f"total brightness is {total}")


TURN_ON = 'turn on'
TURN_OFF = 'turn off'
TOGGLE = 'toggle'
OPERATIONS = {
    TURN_ON: lambda x: x + 1,
    TURN_OFF: lambda x: max(0, x - 1),
    TOGGLE: lambda x: x + 2,
}
def parse(raw):
    lights = defaultdict(lambda: 0)
    pattern = re.compile("(\d+,\d+) through (\d+,\d+)")

    for light in raw:
        instruction = TURN_ON

        if light.startswith(TURN_OFF):
            instruction = TURN_OFF
        elif light.startswith(TOGGLE):
            instruction = TOGGLE

        op = OPERATIONS[instruction]
        match = pattern.search(light)
        start = [int(i) for i in match.group(1).split(",")]
        end = [int(i) for i in match.group(2).split(",")]

        for x in range(end[0] - start[0] + 1):
            for y in range(end[1] - start[1] + 1):
                point = (start[0] + x, start[1] + y)
                lights[point] = op(lights[point])

    return lights


if __name__ == "__main__":
    with open("lights.pi") as f:
        main(f.read().rstrip().split("\n"))
