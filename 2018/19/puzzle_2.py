#!/usr/bin/python

opcodes = dict(
    addr=lambda a, b, r: r[a] + r[b],
    addi=lambda a, b, r: r[a] + b,
    mulr=lambda a, b, r: r[a] * r[b],
    muli=lambda a, b, r: r[a] * b,
    banr=lambda a, b, r: r[a] & r[b],
    bani=lambda a, b, r: r[a] & b,
    borr=lambda a, b, r: r[a] | r[b],
    bori=lambda a, b, r: r[a] | b,
    setr=lambda a, b, r: r[a],
    seti=lambda a, b, r: a,
    gtir=lambda a, b, r: 1 if a > r[b] else 0,
    gtri=lambda a, b, r: 1 if r[a] > b else 0,
    gtrr=lambda a, b, r: 1 if r[a] > r[b] else 0,
    eqir=lambda a, b, r: 1 if a == r[b] else 0,
    eqri=lambda a, b, r: 1 if r[a] == b else 0,
    eqrr=lambda a, b, r: 1 if r[a] == r[b] else 0,
)

def main():
    with open("instructions.pi") as f:
        raw = f.read().split("\n")

    ip_register = int(raw[0].split(" ")[1])
    instructions = parse(raw[1:])

    registers = execute_program(ip_register, instructions)
    print("the value of register 0 is {}".format(registers[0]))

def execute_program(ip_register, instructions):
    r = [0] * 6
    r[0] = 1
    # part 2 - seed registers and IP
    r = [0, 0, 10551386, 10551384, 3, 1]
    r = [5275696, 0, 10551386, 10551385, 3, 10551386]
    ip = r[ip_register]


    count = 0
    while ip < len(instructions):
        r[ip_register] = ip
        current_instruction = instructions[ip]
        opcode = current_instruction.keys()[0]
        values = current_instruction[opcode]
        print("{:4d} IP:[{:2d}] INSTRUCTION: {} {} - R: {}".format(count, ip, opcode, values, r))
        r[values[-1]] = opcodes[opcode](values[0], values[1], r)

        ip = r[ip_register]
        ip += 1
        count += 1

        if count > 100:
            break

    print("{} instructions were executed".format(count))

    return r

def parse(raw):
    instructions = []
    for row in raw:
        parts = row.split(" ")
        inst = dict()
        inst[parts[0]] = [int(i) for i in parts[1:]]
        instructions.append(inst)

    return instructions

if __name__ == "__main__":
    main()
