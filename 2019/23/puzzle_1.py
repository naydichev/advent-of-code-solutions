#!/usr/bin/env python3

from collections import defaultdict
from functools import partial


def producer(data):
    if len(data) == 0:
        return -1

    d = data[0]
    v = d[0]
    d.pop(0)

    if len(d) == 0:
        data.pop(0)

    return v


def consumer(data, temp, value):
    temp.append(value)

    if len(temp) == 3:
        dest, x, y = temp
        if dest == 255:
            print(f"sending to 255! {x}, {y}")
            print("quit me")
        data[dest].append([x, y])
        temp.clear()


def main(instructions):
    data = defaultdict(list)
    temp = defaultdict(list)

    threads = []
    for i in range(50):
        data[i] = [[i]]

        thread = execute_program(instructions.copy(), partial(producer, data[i]), partial(consumer, data, temp[i]), False)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "aoc.23"
    from intcode import execute_program

    with open("nic.pi") as f:
        main(list(map(int, f.read().strip().split(","))))
