#!/usr/bin/env python3

def main():
    with open("bus.pi") as f:
        now, busses = parse(f.readlines())

    busses = list(filter(lambda x: x != "x", busses))

    quickest_bus = None
    wait_time = None

    for bus in busses:
        n = now // bus
        next_arrival = bus * (n + 1)

        waits = next_arrival - now
        if quickest_bus is None or waits < wait_time:
            quickest_bus = bus
            wait_time = next_arrival - now

    print(f"bus {quickest_bus} arrives in {wait_time} minutes ({quickest_bus * wait_time})")



def parse(raw):
    now = int(raw[0].strip())
    busses = [int(b) if b != "x" else b for b in raw[1].split(",")]

    return now, busses


if __name__ == "__main__":
    main()
