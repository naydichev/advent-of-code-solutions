#!/usr/bin/env python3

def main():
    with open("memory.pi") as f:
        data = parse(f.readlines())

    memory = dict()
    last = None
    for i, v in enumerate(data):
        memory[v] = i
        last = v

    del memory[last]

    while i < 2019:
        new = 0
        if last in memory:
            new = i - memory[last]

        memory[last] = i
        last = new
        i += 1

    print(f"the 2020th number is {last}")


def rindex(digits, value):
    index = 0
    digits.index(value, index)


def parse(raw):
    return [int(n) for n in raw[0].strip().split(",")]


if __name__ == "__main__":
    main()
