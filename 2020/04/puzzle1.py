#!/usr/bin/env python3


def main():
    with open("passports.pi") as f:
        passports = parse_passports(f.readlines(), ["cid"])

    required_keys = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

    valid_passports = list(filter(lambda passport: passport.keys() == required_keys, passports))

    print(f"there are {len(valid_passports)} valid passports")


def parse_passports(raw, remove_fields=[]):
    passports = []
    passport = {}

    for line in raw:
        line = line.strip()
        if line == "":
            passports.append(passport)

            for field in remove_fields:
                if field in passport:
                    del passport[field]
            passport = {}
            continue

        pieces = line.split(" ")
        for piece in pieces:
            key, value = piece.split(":")
            passport[key] = value

    if len(passport) != 0:
        passports.append(passport)

    return passports

if __name__ == "__main__":
    main()
