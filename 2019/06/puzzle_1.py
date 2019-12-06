#!/usr/bin/env python3


def main(raw_orbits):
    orbits = [o.split(")") for o in raw_orbits]
    objects = {o[1] for o in orbits}
    starmap = {o[1]: o[0] for o in orbits}

    print(starmap)

    num_orbits = 0
    for o in objects:
        k = o
        while k != "COM":
            k = starmap[k]
            num_orbits += 1

    print(f"total number of orbits is {num_orbits}")

if __name__ == "__main__":
    with open("orbits.pi") as f:
        main(f.read().rstrip().split())
