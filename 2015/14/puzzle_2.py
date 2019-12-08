#!/usr/bin/env python3

from collections import namedtuple

Reindeer = namedtuple("Reindeer", ["name", "speed", "flytime", "resttime"])

FLYING = "flying"
RESTING = "resting"


def main(raw, duration=2503):
    data = parse(raw)

    d = calculate_points(data, duration)

    print(f"the winner has {d} points")


def calculate_points(data, duration):
    i = 0
    names = {r.name for r in data}
    points = {r.name: 0 for r in data}
    status = {r.name: FLYING for r in data}
    status_time = {r.name: 0 for r in data}
    distance = {r.name: 0 for r in data}

    while i < duration:
        for r in data:
            if status[r.name] == FLYING and status_time[r.name] == r.flytime:
                status[r.name] = RESTING
                status_time[r.name] = 0

            if status[r.name] == RESTING and status_time[r.name] == r.resttime:
                status[r.name] = FLYING
                status_time[r.name] = 0

            status_time[r.name] += 1

            if status[r.name] == FLYING:
                distance[r.name] += r.speed

        furthest = max(distance.values())
        for r in [r for r in names if distance[r] == furthest]:
            points[r] += 1

        i += 1

    return max(points.values())


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
