#!/usr/bin/env python3

from collections import defaultdict, namedtuple

BagAndQty = namedtuple("BagAndQty", ["bag", "qty"])


def main():
    with open("luggage.pi") as f:
        luggage = parse(f.readlines())

    inverse_luggage = inverse(luggage)
    my_bag = "shiny gold bag"

    terminal = "no other bags"
    bag_contents = defaultdict(lambda: 0)
    to_visit = []
    for item in inverse_luggage[terminal]:
        bag_contents[item] = 0

        for parent in inverse_luggage[item]:
            nested = luggage[parent]
            if all([x.bag in bag_contents for x in nested]):
                to_visit.append(parent)


    while len(to_visit):
        item = to_visit.pop(0)
        nested = luggage[item]
        contents = sum([(bag_contents[x.bag] + 1) * x.qty for x in nested])

        bag_contents[item] = contents

        for parent in inverse_luggage[item]:
            nested = luggage[parent]
            if all([x.bag in bag_contents for x in nested]):
                to_visit.append(parent)

    print(f"{my_bag} holds {bag_contents[my_bag]} bags")


def inverse(luggage):
    inversed = defaultdict(list)

    for kind, held in luggage.items():
        for each in held:
            inversed[each.bag].append(kind)

    return inversed


def parse(raw):
    bags = defaultdict(list)

    for line in raw:
        line = line.strip()[:-1] # remove newline and period
        bag, holds = line.split(" contain ")
        bag = bag[:-1] # remove plural
        held = []
        for bagqty in holds.split(", "):
            amount = bagqty.split(" ")[0]
            cont = bagqty[len(amount) + 1:]

            if amount == "no":
                cont = f"{amount} {cont}"
                amount = 0
            elif int(amount) > 1:
                cont = cont[:-1] # remove plural

            bags[bag].append(BagAndQty(cont, int(amount)))

    return bags


if __name__ == "__main__":
    main()
