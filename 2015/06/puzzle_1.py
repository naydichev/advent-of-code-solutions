#!/usr/bin/env python3

import re
from collections import defaultdict


def main(raw_lights):
    lights = parse(raw_lights)

    total = sum([1 if x else 0 for x in lights.values()])
    print(f"there are {total} lights on.")


TURN_ON = 'turn on'
TURN_OFF = 'turn off'
TOGGLE = 'toggle'
OPERATIONS = {
    TURN_ON: lambda x: True,
    TURN_OFF: lambda x: False,
    TOGGLE: lambda x: not x,
}
def parse(raw):
    lights = defaultdict(lambda: False)
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
