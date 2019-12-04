#!/usr/bin/env python3


def main(strings):
    count = 0
    for s in strings:
        # add one for each \ and for each ", add two for the new quotes
        count += s.count('\\') + s.count('"') + 2

    print(f"the new value is {count}")


if __name__ == "__main__":
    with open("strings.pi") as f:
        main(f.read().rstrip().split("\n"))
