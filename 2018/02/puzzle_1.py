#!/usr/bin/python

def main():
    with open("ids.pi") as f:
        ids = [x.strip() for x in f.readlines()]

    num_doubles = sum([1 if has_doubles(x) else 0 for x in ids])
    num_triples = sum([1 if has_triples(x) else 0 for x in ids])

    print("Checksum is %d * %d => %d" % (num_doubles, num_triples, num_doubles * num_triples))


def has_doubles(idstr):

    return has_n_letters(idstr, 2)

def has_triples(idstr):
    return has_n_letters(idstr, 3)


def has_n_letters(idstr, n):
    chars = set(idstr)
    for char in chars:
        if idstr.count(char) == n:
            return True

    return False

if __name__ == "__main__":
    main()
