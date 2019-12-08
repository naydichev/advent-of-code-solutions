#!/usr/bin/env python3

from collections import namedtuple

Reindeer = namedtuple("Reindeer", ["name", "speed", "flytime", "resttime"])

def main(raw, duration=2503):
    data = parse(raw)

    d = {r.name: distance(r, duration) for r in data}
    m = max(d.keys(), key=lambda x: d[x])

    print(f"{m} can travel the fastest {d[m]} km")


def distance(reindeer, duration):
    i = 0
    distance = 0
    while i < duration:
        amt = reindeer.flytime
        if i + amt >= duration:
            amt = duration - i
        distance += reindeer.speed * amt
        i += amt + reindeer.resttime

    return distance


def parse(raw):
    data = []

    for r in raw:
        parts = r.split()

        data.append(Reindeer(parts[0], int(parts[3]), int(parts[6]), int(parts[-2])))

    return data


if __name__ == "__main__":
    with open("reindeer.pi") as f:
        main(f.read().rstrip().split("\n"))
