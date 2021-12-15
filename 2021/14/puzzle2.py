#!/usr/bin/env python3

from collections import Counter, defaultdict

def main():
    template, rules = parse_input()


    total_counter = Counter()
    for i in range(len(template) - 1):
        key = template[i:i + 2]
        key_counter = apply_rules(key, rules, 40)
        total_counter += Counter(key_counter)


    most = max(total_counter.values())
    least = min(total_counter.values())

    print(f"The thing is {most - least - 1}")


def apply_rules(template, rules, iteration, handled={}):
    polymers = defaultdict(int)
    if iteration == 0:
        for char in template:
            polymers[char] += 1

        return polymers

    template_and_iteration = (template, iteration)
    if template_and_iteration in handled:
        return handled[template_and_iteration]

    to_insert = rules[template]
    former = apply_rules(f"{template[0]}{to_insert}", rules, iteration - 1, handled)
    latter = apply_rules(f"{to_insert}{template[1]}", rules, iteration - 1, handled)

    for k, v in former.items():
        polymers[k] += v
    for k, v in latter.items():
        polymers[k] += v

    # this was double counted
    polymers[to_insert] -= 1

    handled[template_and_iteration] = polymers

    return polymers


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
