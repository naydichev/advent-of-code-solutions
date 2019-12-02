#!/usb/bin/env python3


def main(things):
    count = 0
    for string in things:
        if nice(string):
            count += 1

    print(f"found {count} nice strings")


def nice(string):
    return contains_pairs(string) \
            and contains_sandwich(string)


def contains_pairs(string):
    length = len(string)
    for i in range(length):
        if i + 1 < length:
            pair = string[i:i + 2]
            substring = "".join(string[i + 2:])
            if pair in substring:
                return True

    return False


def contains_sandwich(string):
    length = len(string)
    for i in range(length):
        if i + 2 < length \
            and string[i] == string[i + 2] \
            and string[i] != string[i + 1]:
                return True

    return False


if __name__ == "__main__":
    with open("input.pi") as f:
        main(f.read().rstrip().split("\n"))
