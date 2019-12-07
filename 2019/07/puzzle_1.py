#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import permutations


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
    return None, value


def jump_if_true(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)

    if a is not 0:
        return b, None


def jump_if_false(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)

    if a is 0:
        return b, None


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


def main(instructions):
    max_thruster = 0

    for option in permutations(range(5)):
        output = 0
        for signal in option:
            output = run_program(instructions[:], [signal, output])

        if output > max_thruster:
            max_thruster = output

    print(f"max thruster value: {max_thruster}")

def run_program(instructions, inputs):
    ip = 0

    while ip < len(instructions):
        modes, opcode = decode_opcode(instructions[ip])

        n = IP_COUNT[opcode]

        print(f"{ip:04} - executing opcode {opcode:02}, with modes {modes} - {instructions[ip:ip + n]}")

        value = OP[opcode](modes, ip, instructions, inputs)

        if value is None:
            ip += n
        elif value[1] is not None:
            return value[1]
        else:
            ip = value[0]


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])


if __name__ == "__main__":
    with open("amps.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")])
