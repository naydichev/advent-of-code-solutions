#!/usr/bin/env python3

from collections import namedtuple

Instruction = namedtuple("Instruction", ["opcode", "value"])

OPCODES = {
    "acc": lambda pc, acc, value: (pc + 1, acc + value),
    "jmp": lambda pc, acc, value: (pc + value, acc),
    "nop": lambda pc, acc, value: (pc + 1, acc)
}

def parse_instructions(raw):
    instructions = []

    for line in raw:
        opcode, value = line.split(" ")
        instructions.append(Instruction(opcode, int(value)))

    return instructions


def run_program(instructions, halt_on_loop=False):
    pc = 0
    acc = 0
    seen = set()

    while pc < len(instructions):
        instruction = instructions[pc]

        opcode = instruction.opcode
        value = instruction.value

        if pc in seen and halt_on_loop:
            break

        seen.add(pc)

        pc, acc = OPCODES[opcode](pc, acc, value)

    return acc, pc
