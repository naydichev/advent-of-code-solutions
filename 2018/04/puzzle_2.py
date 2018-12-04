#!/usr/bin/python

from datetime import datetime
import re
import pprint

PATTERN = re.compile("\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.*)")
GUARD_PATTERN = re.compile("Guard #(\d+) begins shift")
FALL_ASLEEP = "falls asleep"
WAKES_UP = "wakes up"

SLEEP = "sleep"
AWAKE = "awake"
SHIFT_START = "shift_start"


def main():
    with open("schedule.pi") as f:
        raw_schedules = [x.strip("\n") for x  in f.readlines()]

    schedules = sorted([parse_schedule(x) for x in raw_schedules], key=lambda x: x["time"])
    for s in schedules:
        print(s)

    guard_sleeps = compute_guard_sleeps(schedules)

    most_asleep = minute_most_asleep(guard_sleeps)

    print("Guard {} was asleep the most, and most often on minute {}; answer: {}".format(
        most_asleep["id"],
        most_asleep["minute"],
        most_asleep["id"] * most_asleep["minute"]
    ))


def parse_schedule(raw_schedule):
    match = PATTERN.match(raw_schedule)

    date = match.group(1)
    dtime = datetime.strptime(date, "%Y-%m-%d %H:%M")

    schedule = dict(time=dtime)

    rest = match.group(2)

    guard_match = GUARD_PATTERN.match(rest)

    if guard_match:
        schedule["id"] = int(guard_match.group(1))
        schedule["action"] = SHIFT_START
    elif rest == FALL_ASLEEP:
        schedule["action"] = SLEEP
    elif rest == WAKES_UP:
        schedule["action"] = AWAKE

    return schedule

def compute_guard_sleeps(schedules):
    guards = {}
    current_guard = None
    went_to_sleep = None
    for schedule in schedules:
        print(schedule)
        if "id" in schedule:
            current_guard = schedule["id"]
        elif schedule["action"] == SLEEP:
            went_to_sleep = schedule["time"]
        elif schedule["action"] == AWAKE:
            woke_up = schedule["time"]
            minutes_asleep = (woke_up - went_to_sleep).seconds / 60

            guards.setdefault(current_guard, {})["id"] = current_guard
            guards[current_guard] \
                .setdefault("minutes_asleep", []) \
                .append(minutes_asleep)

            for i in range(went_to_sleep.minute, woke_up.minute):
                n = guards[current_guard].setdefault("minutes", {}).setdefault(i, 0)
                guards[current_guard]["minutes"][i] = n + 1

    return guards

def minute_most_asleep(guard_sleeps):
    minutes = {}

    for guard in guard_sleeps.values():
        for m, n in guard["minutes"].items():
            minutes.setdefault(m, []).extend([guard["id"]] * n)

    most_asleep_guard = None
    most_asleep_minute = None
    number_of_times_asleep = 0
    for m, guards  in minutes.items():
        for gid in set(guards):
            if guards.count(gid) > number_of_times_asleep:
                number_of_times_asleep = guards.count(gid)
                most_asleep_minute = m
                most_asleep_guard = gid

    print(guard_sleeps[most_asleep_guard])
    return dict(id=most_asleep_guard, minute=most_asleep_minute)



if __name__ == "__main__":
    main()
