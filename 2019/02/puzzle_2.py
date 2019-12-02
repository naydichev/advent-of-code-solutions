#!/usr/bin/env python3


def main():
    with open("opcodes.pi") as f:
        line = f.read()
        opcodes = [int(l) for l in line.split(",")]


    for noun in range(100):
        for verb in range(100):
            duplicate = opcodes[:]
            duplicate[1] = noun
            duplicate[2] = verb

            if run_program(duplicate) == 19690720:
                print(f"found a match, noun = {noun}, verb = {verb}.")
                print(f"result: {noun * 100 + verb}")


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

    return codes[0]

if __name__ == "__main__":
    main()
