#!/urs/bin/env python3

from collections import namedtuple

Ingredient = namedtuple("Ingredient", ["name", "capacity", "durability", "flavor", "texture", "calories"])


def main(raw):
    ingredients = parse(raw)
    for i in ingredients:

    max_total = 0
    for i in range(101):
        for j in range(101 - i):
            for k in range(101 - i - j):
                combination = [i, j, k, max(0, (100 - i - j - k))]
                totals = {k: 0 for k in Ingredient._fields[1:]}

                for n,ing in enumerate(ingredients):
                    totals["capacity"]   += ing.capacity   * combination[n]
                    totals["durability"] += ing.durability * combination[n]
                    totals["flavor"]     += ing.flavor     * combination[n]
                    totals["texture"]    += ing.texture    * combination[n]
                    totals["calories"]   += ing.calories   * combination[n]

                if totals["calories"] != 500:
                    continue

                x = max(0, totals["capacity"]) * max(0, totals["durability"]) * max(0, totals["flavor"]) * max(0, totals["texture"])
                if x > max_total:
                    max_total = x

    print(f"highest score {max_total} with only 500 calories")


def parse(raw):
    data = []
    for row in raw:
        parts = row.split()

        data.append(Ingredient(parts[0][:-1], int(parts[2][:-1]), int(parts[4][:-1]), int(parts[6][:-1]), int(parts[8][:-1]), int(parts[10])))

    return data

if __name__ == "__main__":
    with open("ingredients.pi") as f:
        main(f.read().rstrip().split("\n"))
