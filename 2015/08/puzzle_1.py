#!/usr/bin/env python3


def main(strings):
    code = count_codes(strings)
    values = count_values(strings)

    print(f"there are {code} codes and {values} values. the answer is {code - values}")


def count_codes(strings):
    return sum([len(s) for s in strings])


def count_values(strings):
    return sum(len(eval(s)) for s in strings)


if __name__ == "__main__":
    with open("strings.pi") as f:
        main(f.read().rstrip().split("\n"))
