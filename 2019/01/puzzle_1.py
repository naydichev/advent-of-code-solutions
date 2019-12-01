#!/usr/bin/env python3

import math

def fuel_for_mass(mass):
    return math.floor(int(line) / 3) - 2

fuel = 0
with open("mass_values.pi") as f:
    for line in f:
        fuel += fuel_for_mass(int(line))

print("fuel required", fuel)
