#!/usr/bin/env python3

import sys
from collections import defaultdict


IP_COUNT = {
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    99: 1
}

MODES = [
    lambda addr, instr: instr[addr],
    lambda addr, instr: addr
]
def value_for_mode(mode, ip, inst):
    if mode == 1:
        return inst[ip]
    return inst[inst[ip]]


def add(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    inst[inst[ip + 3]] = a + b


def mult(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    inst[inst[ip + 3]] = a * b


def read_input(modes, ip, inst, data):
    value = data.pop(0)
    inst[inst[ip + 1]] = value


def output(modes, ip, inst, _):
    value = MODES[modes[-1]](inst[ip + 1], inst)
    print(f">>> {value}")


def halt(_, __, inst, ___):
    sys.exit(0)


OP = {
    1: add,
    2: mult,
    3: read_input,
    4: output,
    99: halt
}


def main(instructions, inputs=[1]):
    i = 0

    while i < len(instructions):
        mode_and_opcode = instructions[i]
        modes, opcode = decode_opcode(mode_and_opcode)
        n = IP_COUNT[opcode]
        print(f"executing opcode {opcode:02}, with modes {modes} - {instructions[i:i + n]}")
        out = instructions[i + n - 1]
        OP[opcode](modes, i, instructions, inputs)
        i += n

    print(instructions[0])


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])


if __name__ == "__main__":
    with open("instructions.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")])
