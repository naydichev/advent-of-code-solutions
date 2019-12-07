#!/usr/bin/env python3

import sys
from collections import defaultdict, namedtuple
from itertools import permutations
from threading import Thread
from queue import Queue

InstructionOutput = namedtuple('InstructionOutput', [ "ip", "output", "halt" ], defaults=[None, None, False])

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
    return InstructionOutput()


def mult(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    c = inst[ip + 3]

    inst[c] = a * b
    return InstructionOutput()


def read_input(modes, ip, inst, data):
    value = data.get()
    print(f"<<< {value}")
    inst[inst[ip + 1]] = value
    data.task_done()

    return InstructionOutput()


def output(modes, ip, inst, _):
    value = MODES[modes[-1]](inst[ip + 1], inst)
    print(f">>> {value}")

    return InstructionOutput(output=value)


def jump_if_true(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)

    ip = None
    if a is not 0:
        ip =b
    return InstructionOutput(ip=ip)


def jump_if_false(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)

    ip = None
    if a is 0:
        ip = b
    return InstructionOutput(ip=ip)


def less_than(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    c = inst[ip + 3]

    value = 1 if a < b else 0
    inst[c] = value

    return InstructionOutput()


def equals(modes, ip, inst, _):
    a = value_for_mode(modes[-1], ip + 1, inst)
    b = value_for_mode(modes[-2], ip + 2, inst)
    c = inst[ip + 3]

    value = 1 if a == b else 0
    inst[c] = value

    return InstructionOutput()


def halt(_, __, inst, ___):
    return InstructionOutput(halt=True)


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

    for option in permutations(range(5, 10)):
        queues = []
        for o in option:
            q = Queue()
            q.put(o)
            queues.append(q)

        threads = []

        for i, o in enumerate(option):
            input_queue = queues[i]
            if i == 0:
                input_queue.put(0)

            output_queue = queues[(i + 1) % len(queues)]

            t = Thread(target=run_program, name=f"thread-{o}", args=(i, instructions.copy(), input_queue, output_queue))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        output = queues[0].get()
        queues[0].task_done()

        if output > max_thruster:
            max_thruster = output

    print(f"max thruster value: {max_thruster}")

def run_program(t, instructions, input_queue, output_queue):
    ip = 0

    while ip < len(instructions):
        modes, opcode = decode_opcode(instructions[ip])

        n = IP_COUNT[opcode]

        print(f"[Thread {t}] {ip:04} - executing opcode {opcode:02}, with modes {modes} - {instructions[ip:ip + n]}")

        output = OP[opcode](modes, ip, instructions, input_queue)

        if output.halt:
            return

        if output.output is not None:
            output_queue.put(output.output)

        if output.ip is not None:
            ip = output.ip
        else:
            ip += n


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])


if __name__ == "__main__":
    with open("amps.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")])
