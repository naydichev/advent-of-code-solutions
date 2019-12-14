#!/usr/bin/env python3


import math
from collections import defaultdict, namedtuple

Recipe = namedtuple("Recipe", ["requirements", "produces"])
Material = namedtuple("Material", ["quantity", "name"])


def main(raw):
    recipes = parse(raw)

    producer = { r.produces.name: r for r in recipes }
    ore_for_a_fuel = make_fuel(producer, 1)
    ore_available = 1000000000000

    fuel = 0
    attempt = ore_available // ore_for_a_fuel
    extra = defaultdict(int)

    while ore_available and attempt:
        extra_copy = defaultdict(int, extra)
        amount_required = make_fuel(producer, attempt, extra_copy)

        if amount_required > ore_available:
            attempt //= 2
        else:
            fuel += attempt
            ore_available -= amount_required
            extra = extra_copy

    print(f"can make {fuel} fuel with 1 trillion ORE")


def make_fuel(producer, fuel_amt, extra=defaultdict(int)):
    materials_required = defaultdict(int)
    totals = defaultdict(int)
    materials_required["FUEL"] = fuel_amt

    while list(materials_required.keys()) != ["ORE"]:
        req, qty = materials_required.popitem()
        if req == "ORE":
            req2, qt2 = materials_required.popitem()
            materials_required[req] = qty
            req = req2
            qty = qt2

        p = producer[req]
        n_qty = qty - extra[req]
        adjusted_qty = math.ceil(n_qty / p.produces.quantity) * p.produces.quantity
        totals[req] += adjusted_qty
        extra[req] += adjusted_qty - qty
        for r in p.requirements:
            materials_required[r.name] += (r.quantity * adjusted_qty) // p.produces.quantity

    return materials_required["ORE"]


def parse(raw):
    recipes = []

    for r in raw:
        parts = r.split(" => ")
        pqty, pname = parts[1].split()
        materials = []
        for m in parts[0].split(", "):
            qty, name = m.split()
            materials.append(Material(int(qty), name))

        recipes.append(
            Recipe(materials, Material(int(pqty), pname))
        )

    return recipes


if __name__ == "__main__":
    with open("materials.pi") as f:
        main(f.read().strip().split("\n"))
