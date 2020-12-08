#!/usr/bin/env python3

from opcode import Instruction, parse_instructions, run_program


def main():
    # with open("sample.pi") as f:
    with open("opcodes.pi") as f:
        instructions = parse_instructions(f.readlines())

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

        acc, pc = run_program(copy, True)

        if pc >= len(instructions):
            print(f"program successfully terminated, accumulator: {acc}")
            break


if __name__ == "__main__":
    main()
