#!/usr/bin/env python3

from itertools import combinations
from recordtype import recordtype


Position = recordtype("Position", "x y z")
Velocity = recordtype("Velocity", "x y z")
Moon = recordtype("Moon", "id position velocity")

def main(raw, steps):
    moons = parse(raw)

    for i in range(steps):
        calculate_gravity(moons)
        apply_velocity(moons)

    total_energy = calculate_energy(moons)
    print(f"total energy in the system {total_energy}")


def calculate_energy(moons):
    total = 0
    for moon in moons:
        pot = abs(moon.position.x) + abs(moon.position.y) + abs(moon.position.z)
        kin = abs(moon.velocity.x) + abs(moon.velocity.y) + abs(moon.velocity.z)

        total += (pot * kin)

    return total

def calculate_gravity(moons):
    for a, b in combinations(moons, 2):
        if a.position.x > b.position.x:
            a.velocity.x -= 1
            b.velocity.x += 1
        elif a.position.x < b.position.x:
            a.velocity.x += 1
            b.velocity.x -= 1

        if a.position.y > b.position.y:
            a.velocity.y -= 1
            b.velocity.y += 1
        elif a.position.y < b.position.y:
            a.velocity.y += 1
            b.velocity.y -= 1

        if a.position.z > b.position.z:
            a.velocity.z -= 1
            b.velocity.z += 1
        elif a.position.z < b.position.z:
            a.velocity.z += 1
            b.velocity.z -= 1


def apply_velocity(moons):
    for moon in moons:
        moon.position.x += moon.velocity.x
        moon.position.y += moon.velocity.y
        moon.position.z += moon.velocity.z


def parse(raw):
    moons = []

    for i, moon in enumerate(raw):
        parts= [int(x.strip()[2:]) for x in moon[1:-1].split(",")]
        moons.append(
            Moon(i, Position(parts[0], parts[1], parts[2]), Velocity(0, 0, 0))
        )

    return moons


if __name__ == "__main__":
    with open("moons.pi") as f:
        main(f.read().strip().split("\n"), 1000)
