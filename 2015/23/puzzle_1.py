#!/usr/bin/env python3


def main(program):
    i = 0
    registers = dict(a=0, b=0)
    while i < len(program):
        instruction, arguments = program[i]
        ip_changed = False

        print(f"{i:03} - [A: {registers['a']:05}; B: {registers['b']:05}] - {instruction} {arguments}")
        if instruction == "hlf":
            registers[arguments] //= 2
        elif instruction == "tpl":
            registers[arguments] *= 3
        elif instruction == "inc":
            registers[arguments] += 1
        elif instruction == "jmp":
            i += int(arguments)
            ip_changed = True
        elif instruction == "jie":
            r, offset = arguments.split(", ")
            if registers[r] % 2 == 0:
                i += int(offset)
                ip_changed = True
        elif instruction == "jio":
            r, offset = arguments.split(", ")
            if registers[r] == 1:
                i += int(offset)
                ip_changed = True

        if not ip_changed:
            i += 1

    print(registers)


if __name__ == "__main__":
    with open("program.pi") as f:
        main([(i[:3], i[4:]) for i in f.read().strip().split("\n")])
