#!/usr/bin/env python3


def main():
    with open("opcodes.pi") as f:
        line = f.read()
        opcodes = [int(l) for l in line.split(",")]

    opcodes[1] = 12
    opcodes[2] = 2
    run_program(opcodes)


def run_program(codes):
    i = 0
    while i <= len(codes):
        if codes[i] == 99:
            break

        a = codes[codes[i + 1]]
        b = codes[codes[i + 2]]
        dest = codes[i + 3]
        result = a + b
        if codes[i] == 2:
            result = a * b

        codes[dest] = result
        i += 4

    print("value at 0", codes[0])


if __name__ == "__main__":
    main()
