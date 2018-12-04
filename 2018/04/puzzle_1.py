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

    longest_sleeper = find_longest_sleeper(guard_sleeps)

    most_asleep = minute_most_asleep(longest_sleeper)

    print("Guard {} was asleep the most, and most often on minute {}; answer: {}".format(
        longest_sleeper["id"],
        most_asleep,
        int(longest_sleeper["id"])  * most_asleep
    ))


def parse_schedule(raw_schedule):
    match = PATTERN.match(raw_schedule)

    date = match.group(1)
    dtime = datetime.strptime(date, "%Y-%m-%d %H:%M")

    schedule = dict(time=dtime)

    rest = match.group(2)

    guard_match = GUARD_PATTERN.match(rest)

    if guard_match:
        schedule["id"] = guard_match.group(1)
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

            print(guards[current_guard])

    return guards

def find_longest_sleeper(guard_sleeps):
    most_asleep_minutes = 0
    longest_sleeper_guard_id = -1

    for guard_id, guard in guard_sleeps.items():
        longest = sum(guard["minutes_asleep"])
        if longest > most_asleep_minutes:
            most_asleep_minutes = longest
            longest_sleeper_guard_id = guard_id

    print(guard_sleeps[longest_sleeper_guard_id])
    return guard_sleeps[longest_sleeper_guard_id]

def minute_most_asleep(longest_sleeper):
    longest_minute = -1
    max_sleeps = 0

    for minute, number_asleep in longest_sleeper["minutes"].items():
        if number_asleep > max_sleeps:
            max_sleeps = number_asleep
            longest_minute = minute

    return longest_minute

if __name__ == "__main__":
    main()
