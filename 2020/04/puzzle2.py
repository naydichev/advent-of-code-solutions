#!/usr/bin/env python3

import re

EYE_COLORS = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
HCL_PATTERN = re.compile("^#[a-f0-9]{6}$")
PID_PATTERN = re.compile("^[0-9]{9}$")


def main():
    with open("passports.pi") as f:
        passports = parse_passports(f.readlines(), ["cid"])

    required_keys = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

    valid_passports = list(
            filter(
                lambda passport: passport.keys() == required_keys \
                        and is_passport_valid(passport),
                        passports))

    print(f"there are {len(valid_passports)} valid passports")


def is_passport_valid(passport):
    return all([FIELDS[field](value) for field, value in passport.items()])


def is_height_valid(hgt):
    if len(hgt) < 3:
        return False

    num = int(hgt[:-2])
    unit = hgt[-2:]

    if unit == "cm":
        return num >= 150 and num <= 193
    return num >= 59 and num <= 76


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


FIELDS = dict(
    byr=lambda byr: int(byr) >= 1920 and int(byr) <= 2002,
    iyr=lambda iyr: int(iyr) >= 2010 and int(iyr) <= 2020,
    eyr=lambda eyr: int(eyr) >= 2020 and int(eyr) <= 2030,
    hgt=is_height_valid,
    hcl=lambda hcl: HCL_PATTERN.match(hcl) is not None,
    ecl=lambda ecl: ecl in EYE_COLORS,
    pid=lambda pid: PID_PATTERN.match(pid) is not None
)


if __name__ == "__main__":
    main()
