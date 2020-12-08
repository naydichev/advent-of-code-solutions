#!/usr/bin/env python3

from collections import namedtuple

Instruction = namedtuple("Instruction", ["opcode", "value"])


def main():
    # with open("sample.pi") as f:
    with open("opcodes.pi") as f:
        instructions = parse(f.readlines())

    accumulator = 0
    pc = 0
    seen = set()

    while True:
        instruction = instructions[pc]
        opcode = instruction.opcode
        value = instruction.value

        if pc in seen:
            break

        seen.add(pc)
        if opcode == "acc":
            accumulator += value
            pc += 1
        elif opcode == "jmp":
            pc += value
        elif opcode == "nop":
            pc += 1

    print(f"I've been here before.... {accumulator}")


def parse(raw):
    instructions = []

    for line in raw:
        opcode, value = line.split(" ")
        instructions.append(Instruction(opcode, int(value)))

    return instructions


if __name__ == "__main__":
    main()
