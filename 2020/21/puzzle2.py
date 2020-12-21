#!/usr/bin/env python3

from collections import defaultdict, namedtuple

Food = namedtuple("Food", ["ingredients", "allergens"])


def main():
    # with open("sample.pi") as f:
    with open("allergens.pi") as f:
        foods = parse(f.readlines())

    possibles = defaultdict(set)
    count = defaultdict(int)

    for food in foods:
        for allergen in food.allergens:
            if len(possibles[allergen]) == 0:
                possibles[allergen].update(food.ingredients)
            else:
                possibles[allergen].intersection_update(food.ingredients)

        for ingredient in food.ingredients:
            count[ingredient] += 1

    allergens = determine_allergens(possibles)

    sorted_allergens = []
    for k, v in sorted(allergens.items(), key=lambda x: x[1]):
        sorted_allergens.append(k)

    x = ",".join(sorted_allergens)
    print(f"these are dangerous: \n{x}")


def determine_allergens(possibles):
    candidates = defaultdict(set)

    for allergen, ingredients in possibles.items():
        for ingredient in ingredients:
            candidates[ingredient].add(allergen)

    allergens = dict()

    while len(allergens) < len(possibles):
        for ingredient, allergen in filter(lambda x: len(x[1]) == 1, candidates.items()):
            allergen = allergen.pop()
            if ingredient in allergens:
                continue
            allergens[ingredient] = allergen

            for v in candidates.values():
                if allergen in v:
                    v.remove(allergen)

    return allergens


def parse(raw):
    output = []

    for line in raw:
        line = line.strip()
        idx = line.find("(")
        allergens = None
        if idx != -1:
            allergens = line[idx + 10: -1].split(", ")
            line = line[:idx - 1]
        ingredients = line.split(" ")

        output.append(Food(ingredients, allergens))

    return output


if __name__ == "__main__":
    main()
