#!/usr/bin/env python3

import math

def fuel_for_mass(mass):
    return math.floor(mass / 3) - 2

fuel = 0
with open("mass_values.pi") as f:
    for line in f:
        fuel_for_line = fuel_for_mass(int(line))
        while fuel_for_line > 0:
            fuel += fuel_for_line
            fuel_for_line = fuel_for_mass(fuel_for_line)

print("fuel required, with fuel for fuel", fuel)
