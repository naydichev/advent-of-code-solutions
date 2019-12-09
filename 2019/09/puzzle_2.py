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
    9: 2,
    99: 1
}


def value_for_mode(mode, ip, inst, rb):
    try:
        if mode == 1:
            return inst[ip]
        elif mode == 2:
            return inst[inst[ip] + rb]
        return inst[inst[ip]]
    except:
        return 0

def ip_for_writing(mode, ip, inst, rb):
    try:
        if mode == 1:
            return ip
        elif mode == 2:
            return inst[ip] + rb

        return inst[ip]
    except:
        return 0

def write_value(value, ip, inst):
    if ip >= len(inst):
        inst.extend([0] * (ip - len(inst) + 1))

    inst[ip] = value


def add(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    write_value(a + b, c, inst)


def mult(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    write_value(a * b, c, inst)


def read_input(modes, ip, inst, data, rb):
    value = data.pop(0)
    a = ip_for_writing(modes[-1], ip + 1, inst, rb)

    write_value(value, a, inst)


def output(modes, ip, inst, _, rb):
    value = value_for_mode(modes[-1], ip + 1, inst, rb)
    print(f">>> {value}")


def jump_if_true(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)

    if a is not 0:
        return b, None


def jump_if_false(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)

    if a is 0:
        return b, None


def less_than(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    value = 1 if a < b else 0
    write_value(value, c, inst)


def equals(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    value = 1 if a == b else 0
    write_value(value, c, inst)


def adjust_relative_base(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)

    new_base = rb + a
    return None, new_base

def halt(_, __, inst, ___, ____):
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
    9: adjust_relative_base,
    99: halt
}


def main(instructions, inputs=[1]):
    ip = 0
    relative_base = 0

    while ip < len(instructions):
        modes, opcode = decode_opcode(instructions[ip])

        n = IP_COUNT[opcode]

        print(f"{ip:04} - executing opcode {opcode:02}, with modes [RB: {relative_base:04}] {modes} - {instructions[ip:ip + n]}")

        value = OP[opcode](modes, ip, instructions, inputs, relative_base)

        if value is not None:
            if value[0] is not None:
                ip = value[0]
            else:
                ip += n

            if value[1] is not None:
                relative_base = value[1]
        else:
            ip += n


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])


if __name__ == "__main__":
    with open("boost.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")], [2])
