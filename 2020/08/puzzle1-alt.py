#!/usr/bin/env python3

from opcode import parse_instructions, run_program
from collections import namedtuple

Instruction = namedtuple("Instruction", ["opcode", "value"])


def main():
    # with open("sample.pi") as f:
    with open("opcodes.pi") as f:
        instructions = parse_instructions(f.readlines())


    acc, pc = run_program(instructions, True)

    print(f"I've been here before.... {acc}")


if __name__ == "__main__":
    main()
