#!/usr/bin/env python3

from functools import partial

PROG = "program"
PROC = "processing"
OUTP = "output"


def producer(data):
    if not len(data[PROC]):
        data[PROC].extend(list(data[PROG].pop(0)))
        data[PROC].append("\n")

    return ord(data[PROC].pop(0))


def consumer(data, value):
    if value != 10:
        data[OUTP].append(value)
    else:
        line = [chr(x) for x in data[OUTP]]
        print("".join(line))
        data[OUTP].clear()


def main(instructions):
    data = {OUTP: [], PROG: [], PROC: []}
    data[PROG] = generate_program()
    execute_program(instructions.copy(), partial(producer, data), partial(consumer, data), False).join()
    print(data[OUTP])


def generate_program():
    return [
        "OR A J",
        "AND B J",
        "AND C J",
        "NOT J J",
        "AND D J",
        "WALK"
    ]

if __name__ == "__main__":
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "aoc.19"
    from intcode import execute_program

    with open("springdroid.pi") as f:
        main(list(map(int, f.read().strip().split(","))))
