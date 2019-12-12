#!/usr/bin/env python3

from functools import reduce

def main(target):
    house = 1
    gifts = 10

    while gifts < target:
        house += 1
        gifts = sum([f * 10 for f in factors(house)])
        # print(f"house {house} gets {gifts} gifts.")

    print(f"house {house} gets {gifts} gifts.")

# https://stackoverflow.com/a/6800214/347924
def factors(n):
    return set(reduce(list.__add__,
        ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

if __name__ == "__main__":
    main(29000000)
