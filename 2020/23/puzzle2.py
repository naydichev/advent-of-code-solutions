#!/usr/bin/env python3

def main():
    # with open("sample.pi") as f:
    with open("cups.pi") as f:
        cups = parse(f.readlines())

    m = max(cups)
    while len(cups) < 1000000:
        n = m + 1
        cups.append(n)
        m = n

    current = 0
    iteration = 0
    cup_length = len(cups)
    move = 0

    while iteration < 10000000:
        current_val = cups[current]
        start_idx = (current + 1) % cup_length
        end_idx = (current + 4) % cup_length

        if end_idx < start_idx:
            start_idx = start_idx - cup_length
            next_cups = cups[start_idx:] + cups[:end_idx]
            del cups[start_idx:]
            del cups[:end_idx]
        else:
            next_cups = cups[start_idx:end_idx]
            del cups[start_idx:end_idx]

        destination = None
        i = 1
        while destination is None:
            if current_val - i > 0:
                try:
                    destination = cups.index(current_val - i)
                except ValueError:
                    i += 1
            else:
                m = max(cups)
                destination = cups.index(m)

        i = 1
        while i <= 3:
            cups.insert(destination + i, next_cups.pop(0))
            i += 1

        current = (cups.index(current_val) + 1) % cup_length
        iteration += 1

    one_idx = cups.index(1)
    a1_idx = (one_idx + 1) % len(cups)
    a2_idx = (one_idx + 2) % len(cups)
    a1 = cups[a1_idx]
    a2 = cups[a2_idx]
    print(f"the thing is {a1 * a2}")



def parse(raw):
    return [int(i) for i in list(raw[0].strip())]


if __name__ == "__main__":
    main()
