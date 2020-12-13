#!/usr/bin/env python3

def main():
    with open("bus.pi") as f:
        _, busses = parse(f.readlines())

    busses = [b if b != "x" else 1 for b in busses]

    time = 0
    lcm = 1
    for idx, bus in enumerate(busses):
        # while the (time + index) is not an even multiple of time
        while (time + idx) % bus:
            # increase the time by the current least common multiple
            time += lcm

        # update the least common multiple to include the current bus
        lcm *= bus

    print(f"the earliest time that these busses could depart in sequence is {time}")


def parse(raw):
    now = int(raw[0].strip())
    busses = [int(b) if b != "x" else b for b in raw[1].split(",")]

    return now, busses


if __name__ == "__main__":
    main()
