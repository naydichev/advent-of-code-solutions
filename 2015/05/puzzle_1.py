#!/usb/bin/env python3


def main(things):
    count = 0
    for string in things:
        if nice(string):
            count += 1

    print(f"found {count} nice strings")


def nice(string):
    return has_three_vowels(string) \
            and has_duplicate_letters(string) \
            and doesnt_have_forbidden(string)


VOWELS = ["a", "e", "i", "o", "u"]
def has_three_vowels(string):
    vowels = sum([string.count(v) for v in VOWELS])
    return vowels >= 3


def has_duplicate_letters(string):
    length = len(string)
    for i in range(length):
        if i + 1 < length and string[i] == string[i + 1]:
            return True

    return False


FORBIDDEN = ["ab", "cd", "pq", "xy"]
def doesnt_have_forbidden(string):
    return not any([f in string for f in FORBIDDEN])


if __name__ == "__main__":
    with open("input.pi") as f:
        main(f.read().rstrip().split("\n"))
