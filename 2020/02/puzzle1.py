#!/usr/bin/env python3

from collections import namedtuple

PolicyAndPassword = namedtuple("PolicyAndPassword", ["minTimes", "maxTimes", "letter", "password"])


def main():
    with open("passwords.pi") as f:
        parsed_policies = [parse_policy(l) for l in f.readlines()]


    valid_policies = list(filter(is_password_valid, parsed_policies))

    print(f"there are {len(valid_policies)} valid policies")


def is_password_valid(policy):
    occurrences = policy.password.count(policy.letter)

    return occurrences >= policy.minTimes and occurrences <= policy.maxTimes


def parse_policy(raw_policy):
    rule, password = [l.strip() for l in raw_policy.split(":")]

    frequency, letter = [r.strip() for r in rule.split(" ")]
    minTimes, maxTimes = [int(m) for m in frequency.split("-")]

    return PolicyAndPassword(minTimes, maxTimes, letter, password)


if __name__ == "__main__":
    main()
