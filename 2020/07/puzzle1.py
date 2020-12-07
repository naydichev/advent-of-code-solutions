#!/usr/bin/env python3

from collections import defaultdict


def main():
    with open("luggage.pi") as f:
        luggage = parse(f.readlines())

    inverse_luggage = inverse(luggage)
    my_bag = "shiny gold bag"

    to_visit = list(inverse_luggage[my_bag])
    terminal = "no other bags"

    visited = set()
    for item in to_visit:
        if item in visited:
            continue

        if item == terminal:
            continue

        visited.add(item)
        to_visit.extend(inverse_luggage[item])

    print(f"{len(visited)} bags can hold {my_bag}")


def inverse(luggage):
    inversed = defaultdict(set)

    for kind, held in luggage.items():
        for each in held:
            inversed[each].add(kind)

    return inversed


def parse(raw):
    bags = defaultdict(set)

    for line in raw:
        line = line.strip()[:-1] # remove newline and period
        bag, holds = line.split(" contain ")
        bag = bag[:-1] # remove plural
        held = []
        for bagqty in holds.split(", "):
            amount = bagqty.split(" ")[0]
            cont = bagqty[len(amount) + 1:]

            if amount == "no":
                amount = 0
                cont = f"{amount} {cont}"
            elif int(amount) > 1:
                cont = cont[:-1] # remove plural

            held.append(cont)

        bags[bag].update(held)

    return bags


if __name__ == "__main__":
    main()
