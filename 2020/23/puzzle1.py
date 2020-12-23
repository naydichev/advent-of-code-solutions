#!/usr/bin/env python3

def main():
    with open("cups.pi") as f:
        cups = parse(f.readlines())

    current = 0
    iteration = 0
    cup_length = len(cups)
    move = 0

    while iteration < 100:
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

        move += 1
        print(f"""
        ---
        move {move}
        start_idx:\t{start_idx}
        end_idx:\t{end_idx}

        before insertion
        cups:\t\t\t{cups}
        next_cups:\t\t{next_cups}
        current:\t\t{current}
        current_val:\t\t{current_val}
        destination:\t\t{destination}
        destination_val:\t{cups[destination]}
        """)

        i = 1
        while i <= 3:
            cups.insert(destination + i, next_cups.pop(0))
            i += 1

        print(f"""
        after insertion
        cups:\t\t\t{cups}
        next_cups:\t\t{next_cups}
        current:\t\t{current}
        current_val:\t\t{current_val}
        destination:\t\t{destination}
        destination_val:\t{cups[destination]}
        ---
        """)

        current = (cups.index(current_val) + 1) % cup_length
        iteration += 1

    one_idx = cups.index(1)
    answer = cups[one_idx + 1:] + cups[:one_idx]
    answer = [str(s) for s in answer]
    answer = "".join(answer)
    print(f"the thing is {answer}")


def parse(raw):
    return [int(i) for i in list(raw[0].strip())]


if __name__ == "__main__":
    main()
