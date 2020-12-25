#!/usr/bin/env python3

def main():
    # with open("sample.pi") as f:
    with open("encryption.pi") as f:
        card_public_key, door_public_key = parse(f.readlines())

    value = 1
    subject_number = 7
    loop = 0
    card_loop_size, door_loop_size = None, None

    while card_loop_size is None or door_loop_size is None:
        value *= subject_number
        value %= 20201227

        loop += 1
        if value == card_public_key and card_loop_size is None:
            card_loop_size = loop 
        if value == door_public_key and door_loop_size is None:
            door_loop_size = loop

    loop_size, subject_number = min((door_loop_size, card_public_key), (card_loop_size, door_public_key), key=lambda x: x[0])

    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227

    print(f"the encryption key is {value}")


def parse(raw):
    output = []

    for line in raw:
        output.append(int(line.strip()))

    return output


if __name__ == "__main__":
    main()
