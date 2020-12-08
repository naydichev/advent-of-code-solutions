#!/usr/bin/env python3

from collections import namedtuple

Instruction = namedtuple("Instruction", ["opcode", "value"])


def main():
    # with open("sample.pi") as f:
    with open("opcodes.pi") as f:
        instructions = parse(f.readlines())

    for i, instruction in enumerate(instructions):
        flipped = None
        value = instruction.value
        if instruction.opcode == "jmp":
            flipped = "nop"
        elif instruction.opcode == "nop":
            flipped = "jmp"
        else:
            continue

        print(f"flipping instruction at index {i}, {flipped} {value}")

        copy = instructions[::]
        copy[i] = Instruction(flipped, value)

        acc = runprogram(copy)

        if acc is not None:
            print(f"program successfully terminated, accumulator: {acc}")
            break


def runprogram(instructions):
    accumulator = 0
    pc = 0
    seen = set()

    while pc < len(instructions):
        instruction = instructions[pc]
        opcode = instruction.opcode
        value = instruction.value

        if pc in seen:
            return None

        seen.add(pc)
        if opcode == "acc":
            accumulator += value
            pc += 1
        elif opcode == "jmp":
            pc += value
        elif opcode == "nop":
            pc += 1

    return accumulator


def parse(raw):
    instructions = []

    for line in raw:
        opcode, value = line.split(" ")
        instructions.append(Instruction(opcode, int(value)))

    return instructions


if __name__ == "__main__":
    main()
