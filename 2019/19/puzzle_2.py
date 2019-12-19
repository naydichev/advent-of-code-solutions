#!/usr/bin/env python3

from functools import partial


def main(instructions):

    check_value = partial(get_output_at, instructions)
    # first 1 after the initial 0, 0
    x, y = 3, 4
    while True:
        if check_value(x, y) == 1:
            print(x, y)
            if check_value(x + 99, y - 99) == 1:
                print("answer", x * 10000 + (y - 99))
                return
            else:
                y += 1
        else:
            x += 1


def consumer(conf, value):
    conf["produce"] = value


def producer(conf):
    return conf["consume"].pop(0)


def get_output_at(instructions, x, y):
    conf = dict(consume=[x, y])
    execute_program(instructions.copy(), partial(producer, conf), partial(consumer, conf), False).join()

    return conf["produce"]


if __name__ == "__main__":
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "aoc.19"
    from intcode import execute_program

    with open("emitter.pi") as f:
        main(list(map(int, f.read().strip().split(","))))
