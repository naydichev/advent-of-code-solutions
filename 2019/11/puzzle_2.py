#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from queue import Queue
from threading import Thread

InstructionOutput = namedtuple("InstructionOutput", ["ip", "output", "halt", "rb"], defaults=[None, None, False, None])

BLACK  = '\33[40m'
WHITE  = '\33[47m'
END    = '\33[0m'

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
    return InstructionOutput()


def mult(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    write_value(a * b, c, inst)
    return InstructionOutput()


def read_input(modes, ip, inst, data, rb):
    value = data.get()
    a = ip_for_writing(modes[-1], ip + 1, inst, rb)
    print(f"<<< {value}")
    write_value(value, a, inst)
    data.task_done()

    return InstructionOutput()


def output(modes, ip, inst, _, rb):
    value = value_for_mode(modes[-1], ip + 1, inst, rb)
    print(f">>> {value}")

    return InstructionOutput(output=value)


def jump_if_true(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)

    ip = None
    if a is not 0:
        ip = b
    return InstructionOutput(ip=ip)


def jump_if_false(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)

    ip = None
    if a is 0:
        ip = b
    return InstructionOutput(ip=ip)


def less_than(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    value = 1 if a < b else 0
    write_value(value, c, inst)
    return InstructionOutput()


def equals(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    value = 1 if a == b else 0
    write_value(value, c, inst)
    return InstructionOutput()


def adjust_relative_base(modes, ip, inst, _, rb):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)

    new_base = rb + a
    return InstructionOutput(rb=new_base)


def halt(_, __, inst, ___, ____):
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
    9: adjust_relative_base,
    99: halt
}


DIRECTION = [ "^", ">", "v", "<"]
MOVE = {
    "^": lambda x,y: (x, y + 1),
    ">": lambda x,y: (x  +1, y),
    "v": lambda x,y: (x, y - 1),
    "<": lambda x,y: (x - 1, y)
}


def main(instructions, inputs=[1]):
    input_queue = Queue()
    output_queue = Queue()

    thread = Thread(target=run_program, args=(instructions, input_queue, output_queue))
    thread.start()

    panel = defaultdict(lambda: defaultdict(lambda: 0))
    panel[0][0] = 1
    x, y = 0, 0
    direction = "^"

    while thread.is_alive():
        # put our current color on the output
        input_queue.put(panel[x][y])

        # get our next paint and move task
        color = output_queue.get(1)
        output_queue.task_done()
        move_dir = output_queue.get()
        output_queue.task_done()

        panel[x][y] = color
        dir_index = DIRECTION.index(direction)
        if move_dir == 1:
            direction = DIRECTION[(dir_index + 1) % len(DIRECTION)]
        else:
            direction = DIRECTION[dir_index - 1]

        x, y = MOVE[direction](x, y)

    min_x = min(panel.keys())
    max_x = max(panel.keys())
    min_y = min([min(p.keys()) for p in panel.values()])
    max_y = max([max(p.keys()) for p in panel.values()])

    for i in range(max_y, min_y - 1, -1):
        line = []
        for j in range(min_x, max_x + 1):
            c = BLACK
            if panel[j][i] == 1:
                c = WHITE
            line.extend([c, " "])

        line.append(END)
        print("".join(line))


def run_program(instructions, input_queue, output_queue):
    ip = 0
    relative_base = 0

    while ip < len(instructions):
        modes, opcode = decode_opcode(instructions[ip])

        n = IP_COUNT[opcode]

        print(f"{ip:04} - executing opcode {opcode:02}, with modes [RB: {relative_base:04}] {modes} - {instructions[ip:ip + n]}")

        output = OP[opcode](modes, ip, instructions, input_queue, relative_base)

        if output.halt:
            return

        if output.output is not None:
            output_queue.put(output.output)

        if output.rb is not None:
            relative_base = output.rb

        if output.ip is not None:
            ip = output.ip
        else:
            ip += n


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])


if __name__ == "__main__":
    with open("paint.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")])
