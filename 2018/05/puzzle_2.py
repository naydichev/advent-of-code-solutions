#!/usr/bin/python

from collections import defaultdict

def main():
    with open("polymer.pi") as f:
        polymers = f.read().strip()

    lowest_n = None
    lowest = None
    for c in "abcdefghijklmnopqrstuvwxyz":
        removed = remove_letters(polymers, c)
        remaining = reduce_chain(removed)

        rlen = len(remaining)
        if lowest_n is None or rlen < lowest_n:
            lowest_n = rlen
            lowest = remaining

    print("done!")
    print(lowest)
    print(lowest_n)

def reduce_chain(polymers):
    popped = True
    poly_len = len(polymers)
    poly_list = list(polymers)

    while popped:
        popped = False
        i = 0

        while i < poly_len + 1:
            j = i + 1
            if j >= poly_len:
                break

            if poly_list[i] != poly_list[j] and poly_list[i].lower() == poly_list[j].lower():
                poly_list.pop(i)
                poly_list.pop(i)
                poly_len -= 2
                popped = True
            else:
                i += 1

    return "".join(poly_list)

def count_frequencies(polymers):
    letters = defaultdict(int)

    for i in range(len(polymers)):
        l = polymers[i].lower()
        n = letters[l]
        letters[l] = n + 1

    return letters

def remove_letters(polymers, letter):
    i = 0
    poly_list = list(polymers)
    poly_len = len(poly_list)

    while i < poly_len:
        if poly_list[i].lower() == letter:
            poly_list.pop(i)
            poly_len -= 1
        else:
            i += 1

    return "".join(poly_list)

if __name__ == "__main__":
    main()
