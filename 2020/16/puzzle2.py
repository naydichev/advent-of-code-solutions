#!/usr/bin/env python3

from collections import defaultdict, namedtuple

Field = namedtuple("Field", ["name", "rule", "validator"])


def main():
    with open("tickets.pi") as f:
        fields, my_ticket, nearby_tickets = parse(f.readlines())

    valid_fields = defaultdict(set)

    for ticket in nearby_tickets:
        is_ticket_valid = True
        possible_fields = defaultdict(set)

        for i, value in enumerate(ticket):
            is_any_field_valid = False
            for field in fields:
                if field.validator(value):
                    is_any_field_valid = True

                    possible_fields[field.name].add(i)

            if not is_any_field_valid:
                is_ticket_valid = False
                break

        if is_ticket_valid:
            for field, indexes in possible_fields.items():
                if len(valid_fields[field]) == 0:
                    valid_fields[field].update(indexes)
                else:
                    valid_fields[field].intersection_update(indexes)


    num = 1
    used_indexes = set()
    for field, indexes in sorted(valid_fields.items(), key=lambda k: len(k[1])):
        actual_indexes = indexes - used_indexes
        index = actual_indexes.pop()
        used_indexes.add(index)
        if field.startswith("departure"):
            num *= my_ticket[index]

    print(f"the multiplication of all departure fields is {num}")


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
