#!/usr/bin/python

def main():
    with open("ids.pi") as f:
        ids = [x.strip() for x in f.readlines()]

    for i in range(0, len(ids)):
        id1, id2 = find_matching_ids(ids[i], ids[i + 1:])

        if id2 is not None:
            answer = remove_differing_letter(id1, id2)
            print("The two similar ids are %s and %s, removing the differing character, the answer is %s" % (id1, id2, answer))
            break

def find_matching_ids(a, ids):
    len_a = len(a)
    for b in ids:
        differing = 0
        for i in range(0, len_a):
            if i > len(b):
                return a, None

            if a[i] is not b[i]:
                differing += 1

        if differing == 1:
            return a, b

    return a, None

def remove_differing_letter(a, b):
    for i in range(0, len(a)):
        if a[i] is not b[i]:
            return a[0:i] + a[i+1:]

if __name__ == "__main__":
    main()
