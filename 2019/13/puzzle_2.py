#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from functools import partial
import time

InstructionOutput = namedtuple("InstructionOutput", ["ip", "output", "halt", "rb"], defaults=[None, None, False, None])

DEBUG = False


def dprint(data):
    if DEBUG:
        print(data)


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


def add(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    write_value(a + b, c, inst)
    return InstructionOutput()


def mult(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    write_value(a * b, c, inst)
    return InstructionOutput()


def read_input(modes, ip, inst, data, rb):
    value = data()
    a = ip_for_writing(modes[-1], ip + 1, inst, rb)
    dprint(f"<<< {value}")
    write_value(value, a, inst)

    return InstructionOutput()


def output(modes, ip, inst, rb, **kwargs):
    value = value_for_mode(modes[-1], ip + 1, inst, rb)
    dprint(f">>> {value}")

    return InstructionOutput(output=value)


def jump_if_true(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)

    ip = None
    if a is not 0:
        ip = b
    return InstructionOutput(ip=ip)


def jump_if_false(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)

    ip = None
    if a is 0:
        ip = b
    return InstructionOutput(ip=ip)


def less_than(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    value = 1 if a < b else 0
    write_value(value, c, inst)
    return InstructionOutput()


def equals(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)
    b = value_for_mode(modes[-2], ip + 2, inst, rb)
    c = ip_for_writing(modes[-3], ip + 3, inst, rb)

    value = 1 if a == b else 0
    write_value(value, c, inst)
    return InstructionOutput()


def adjust_relative_base(modes, ip, inst, rb, **kwargs):
    a = value_for_mode(modes[-1], ip + 1, inst, rb)

    new_base = rb + a
    return InstructionOutput(rb=new_base)


def halt(**kwargs):
    return InstructionOutput(halt=True)


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

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

BG_WHITE = "\33[47m"
BG_BLACK = "\33[40m"
FG_PINK = "\33[95m"
FG_BLUE = "\33[34m"
FG_RED = "\33[31m"
RESET = "\33[0m"

D = {
    EMPTY: f"{BG_WHITE} {RESET}",
    WALL: f"{BG_BLACK} {RESET}",
    BLOCK: f"{BG_WHITE}{FG_PINK}\u25b0{RESET}",
    PADDLE: f"{BG_WHITE}{FG_BLUE}\u25ac{RESET}",
    BALL: f"{BG_WHITE}{FG_RED}\u25c9{RESET}"
}


def main(instructions):
    # add our quarters
    instructions[0] = 2

    run_program(instructions)


def compute_move(panel):
    ball_x = find_position(panel, BALL)
    paddle_x = find_position(panel, PADDLE)

    move = 0
    if ball_x < paddle_x:
        move = -1
    elif ball_x > paddle_x:
        move = 1

    return move


def find_position(panel, symbol):
    for y in panel.keys():
        for x in panel[y].keys():
            if panel[y][x] == symbol:
                return x

    return None


def draw_board(panel, score):
    max_y = max(panel.keys())
    max_x = max([max(x) for x in panel.values()])
    print("\033[2J", flush=False)
    for y in range(max_y):
        line = []
        for x in range(max_x):
            line.append(D[panel[y][x]])

        if line[-1] != WALL:
            line.append(D[WALL])
        print("".join(line), flush=False)

    score_pad = " " * ((max_x - 5) // 2)
    print(f"{D[WALL]}" * (max_x + 1) + RESET, flush=False)
    print(f"{D[WALL]}{BG_WHITE}{score_pad}{FG_RED}{score:05}{RESET}{BG_WHITE}{score_pad}{D[WALL]}{RESET}", flush=False)
    print(f"{D[WALL]}" * (max_x + 1) + RESET, flush=True)
    time.sleep(.009)


def run_program(instructions):
    # save cursor position
    ip = 0
    relative_base = 0
    panel = defaultdict(lambda: defaultdict(lambda: EMPTY))
    score = 0
    in_data = []

    while ip < len(instructions):
        modes, opcode = decode_opcode(instructions[ip])

        n = IP_COUNT[opcode]

        dprint(
            f"{ip:04} - executing opcode {opcode:02}, with modes [RB: {relative_base:04}] {modes} - {instructions[ip:ip + n]}")

        output = OP[opcode](
            modes=modes,
            ip=ip,
            inst=instructions,
            rb=relative_base,
            data=partial(compute_move, panel)
        )

        if output.halt:
            print(f"final score: {score}")
            return

        if output.output is not None:
            in_data.append(output.output)
            if len(in_data) == 3:
                x, y, tile = in_data
                in_data = []
                if x == -1 and y == 0:
                    score = tile
                else:
                    panel[y][x] = tile

                    if tile == BALL or tile == PADDLE:
                        draw_board(panel, score)

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
    with open("arcade.pi") as f:
        main([int(i) for i in f.read().rstrip().split(",")])
