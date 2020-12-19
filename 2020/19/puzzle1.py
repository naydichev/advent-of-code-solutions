#!/usr/bin/env python3

from collections import namedtuple
import re

SUBLIST = "sublist"
CHARACTER = "character"

Rule = namedtuple("Rule", ["kind", "data"])


def main():
    with open("messages.pi") as f:
        rules, messages = parse(f.readlines())

    regex = f"^{build_regex(rules, rules[0])}$"
    pattern = re.compile(regex)
    valid = len(list(filter(lambda v: pattern.fullmatch(v) is not None, messages)))

    print(f"there are {valid} valid messages")


def build_regex(rules, rule):
    if rule.kind == CHARACTER:
        return rule.data

    if "|" in rule.data:
        p1, p2 = [Rule(SUBLIST, r) for r in rule.data.split(" | ")]
        return f"({build_regex(rules, p1)}|{build_regex(rules, p2)})"

    if " " in rule.data:
        idx1, idx2 = [int(i) for i in rule.data.split(" ")]

        return f"({build_regex(rules, rules[idx1])}{build_regex(rules, rules[idx2])})"

    return build_regex(rules, rules[int(rule.data)])


def parse_rules(rules):
    parsed = dict()
    for rule in rules:
        idx, data = rule.split(": ")
        kind = SUBLIST

        if '"' in data:
            kind = CHARACTER
            data = data[1:-1]

        parsed[int(idx)] = Rule(kind, data)

    return parsed


def parse(raw):
    rules = []
    messages = []

    is_messages = False
    for line in raw:
        line = line.strip()

        if line == "":
            is_messages = True
            continue

        obj = rules
        if is_messages:
            obj = messages

        obj.append(line)

    return parse_rules(rules), messages


if __name__ == "__main__":
    main()
