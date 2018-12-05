#!/usr/bin/python

def main():
    with open("polymer.pi") as f:
        polymers = f.read()

    remaining = reduce_chain(polymers)

    print("done!")
    print(remaining)
    print(len(remaining))

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


if __name__ == "__main__":
    main()
