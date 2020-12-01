#!/usr/bin/env python3

from collections import defaultdict
from functools import partial
from threading import Thread

NAT = 255
LAST_NAT = "last_nat"
IDLE = "idle"


def monitor_thread(data):
    old_nat = None
    while len(data[NAT]) > 1:
        old_nat = data[NAT].pop(0)

    data[LAST_NAT] = old_nat
    if old_nat is not None and old_nat[1] == data[NAT][1]:
        print(f"the answer is {old_nat[1]}")

    data[0].append(data[NAT])

def producer(data, my_id):
    my_data = data[my_id]
    if len(my_data) == 0:
        data[IDLE] += 1
        return -1

    data[IDLE] = 0
    d = my_data[0]
    v = d[0]
    d.pop(0)

    if len(d) == 0:
        my_data.pop(0)

    return v


def consumer(data, temp, value):
    temp.append(value)

    if len(temp) == 3:
        dest, x, y = temp

        data[dest].append([x, y])
        temp.clear()


def main(instructions):
    data = defaultdict(list)
    temp = defaultdict(list)
    data[IDLE] = 0

    threads = [
        Thread(target=monitor_thread, args=(data,))
    ]

    for i in range(50):
        data[i] = [[i]]

        thread = execute_program(instructions.copy(), partial(producer, data, i), partial(consumer, data, temp[i]), False)
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
