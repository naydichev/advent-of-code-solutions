#!/usr/bin/env python3

from collections import defaultdict

def main(wires):
    wire_map = defaultdict(lambda: set())

    i = 0
    for wire in wires:
        draw_wire(wire, i, wire_map)
        i += 1

    intersections = filter(lambda v: v is not None, [key if len(value) == 2 else None for key, value in wire_map.items()])
    min_distance = None
    min_location = None

    for cross in intersections:
        distance = sum([abs(x) for x in cross])

        if min_distance is None or distance < min_distance:
            min_distance = distance
            min_location = cross

    print(f"min distance is {min_distance} at location {min_location}")

DIRECTIONS = {
    'L': lambda location: (location[0] + 1, location[1]),
    'R': lambda location: (location[0] - 1, location[1]),
    'U': lambda location: (location[0], location[1] + 1),
    'D': lambda location: (location[0], location[1] - 1)
}

def draw_wire(wire, wire_num, wire_map):
    location = (0, 0)
    for part in wire:
        direction = DIRECTIONS[part[:1]]
        distance = int(part[1:])

        for i in range(distance):
            location = direction(location)
            wire_map[location].add(wire_num)

if __name__ == "__main__":
    with open("wires.pi") as f:
        main([line.rstrip().split(",") for line in f])
