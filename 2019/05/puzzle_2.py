#!/usr/bin/env python3

import sys
from collections import defaultdict


IP_COUNT = {
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4,
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
    c = inst[ip + 3]

    inst[c] = a + b


def mult(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    c = inst[ip + 3]

    inst[c] = a * b


def read_input(modes, ip, inst, data):
    value = data.pop(0)
    inst[inst[ip + 1]] = value


def output(modes, ip, inst, _):
    value = MODES[modes[-1]](inst[ip + 1], inst)
    print(f">>> {value}")


def jump_if_true(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)

    if a is not 0:
        return b


def jump_if_false(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)

    if a is 0:
        return b


def less_than(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    c = inst[ip + 3]

    value = 1 if a < b else 0
    inst[c] = value


def equals(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    c = inst[ip + 3]

    value = 1 if a == b else 0
    inst[c] = value


def halt(_, __, inst, ___):
    sys.exit(0)


OP = {
    1: add,
    2: mult,
    3: read_input,
    4: output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: halt
}


def main(instructions, inputs=[1]):
    ip = 0

    while ip < len(instructions):
        modes, opcode = decode_opcode(instructions[ip])

        n = IP_COUNT[opcode]

        print(f"{ip:04} - executing opcode {opcode:02}, with modes {modes} - {instructions[ip:ip + n]}")

        value = OP[opcode](modes, ip, instructions, inputs)

        if value is None:
            ip += n
        else:
            ip = value


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])


if __name__ == "__main__":
    with open("instructions.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")], [5])
