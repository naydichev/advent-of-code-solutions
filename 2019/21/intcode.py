from collections import defaultdict, namedtuple
from threading import Thread

InstructionOutput = namedtuple("InstructionOutput", ["ip", "output", "halt", "rb"], defaults=[None, None, False, None])
DEBUG = True


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


def execute_program(instructions, in_data, out_data, debug=False):
    thread = Thread(
        target=run_program,
        args=(instructions, in_data, out_data, debug),
        name="intcode-thread",
        daemon=True
    )

    thread.start()
    return thread


def run_program(instructions, in_data, output_data, debug=False):
    global DEBUG
    DEBUG = debug

    # save cursor position
    ip = 0
    relative_base = 0

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
            data=in_data
        )

        if output.halt:
            return

        if output.output is not None:
            output_data(output.output)

        if output.rb is not None:
            relative_base = output.rb

        if output.ip is not None:
            ip = output.ip
        else:
            ip += n


def decode_opcode(data):
    padded = str(data).zfill(5)
    return [int(i) for i in padded[:-2]], int(padded[-2:])
