#!/usr/bin/env python3

from collections import namedtuple

Field = namedtuple("Field", ["name", "rule", "validator"])


def main():
    with open("tickets.pi") as f:
        fields, my_ticket, nearby_tickets = parse(f.readlines())

    tickets = [my_ticket] + nearby_tickets
    scanning_error_rate = []

    for ticket in tickets:
        for value in ticket:
            if not any([f.validator(value) for f in fields]):
                scanning_error_rate.append(value)


    print(f"the ticket scanning error rate is {sum(scanning_error_rate)}")


def parse(raw):
    fields = []
    my_ticket = None
    nearby_tickets = []

    is_my_ticket = False
    is_nearby_tickets = False
    for line in raw:

        line = line.strip()
        if line.startswith("your ticket:"):
            is_my_ticket = True
            continue
        elif line.startswith("nearby tickets:"):
            is_nearby_tickets = True
            continue
        elif line == "":
            continue


        if not is_my_ticket and not is_nearby_tickets:
            fields.append(parse_field(line))
        elif not is_nearby_tickets:
            my_ticket = [int(n) for n in line.split(",")]
        else:
            nearby_tickets.append([int(n) for n in line.split(",")])


    return fields, my_ticket, nearby_tickets


def parse_field(raw):
    name, rules = [r.strip() for r in raw.split(":")]

    rule1, rule2 = [[int(n) for n in r.split("-")] for r in rules.split(" or ")]


    def is_valid(value):
        return (value >= rule1[0] and value <= rule1[1]) or (value >= rule2[0] and value <= rule2[1])


    return Field(name, rules, is_valid)


if __name__ == "__main__":
    main()
