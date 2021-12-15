#!/usr/bin/env python3

def main():
    template, rules = parse_input()


    for i in range(10):
        template = apply_rules(template, rules)

    tset = set(template)
    counts = {}
    for t in tset:
        counts[t] = template.count(t)

    most = max(counts, key=lambda x: counts[x])
    least = min(counts, key=lambda x: counts[x])

    print(f"The thing is {counts[most] - counts[least]}")


def apply_rules(template, rules):
    new_template = []
    length = len(template)
    for i, l in enumerate(template):

        new_template.append(l)
        if (i + 1) >= length:
            break

        new_template.append(rules[f"{l}{template[i + 1]}"])

    return new_template


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    template = data[0]
    rules = {}

    # process data
    for line in data[2:]:
        source, target = line.split(" -> ")
        rules[source] = target

    return template, rules


if __name__ == "__main__":
    main()
