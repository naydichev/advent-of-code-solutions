#!/usr/bin/python

def main():
    with open("plants.pi") as f:
    # with open("sample_input.pi") as f:
        raw_plants = f.read().split("\n")

    state_set, plant_rules = parse(raw_plants)

    print_plants(state_set)
    last_sum = sum(state_set)
    last_delta = sum(state_set)
    same_last_sum = 0

    n = 50000000000
    for i in xrange(n):
        state_set = one_generation(state_set, plant_rules)
        s = sum(state_set)
        if s - last_sum == last_delta:
            same_last_sum += 1
        else:
            last_delta = s - last_sum
            same_last_sum = 0

        last_sum = s

        if same_last_sum == 6:
            print("should be", last_sum + ((n - i - 1) * last_delta))
            break

    print_plants(state_set, [i, sum(state_set), min(state_set), max(state_set)])


def print_plants(state_set, extra=None):
    if extra is None:
        extra = ""
    print(make_plant_str(state_set), extra)

def make_plant_str(vals):
    return "".join(["#" if x in vals else "." for x in range(min(vals), max(vals) + 1)])

def parse(raw_plants):
    initial_state = raw_plants.pop(0).split(": ")[1]

    state_set = set()
    for i, c in enumerate(initial_state):
        if c == "#":
            state_set.add(i)

    rules = set([x[0] for x in (line.split(" => ") for line in raw_plants[1:]) if x[1] == "#"])

    return state_set, rules

def one_generation(state_set, rules):
    new_set = set()
    start = min(state_set) - 4
    end = max(state_set) + 4

    for i in range(start, end):
        if "".join("#" if x in state_set else "." for x in range(i - 2, i + 3)) in rules:
            new_set.add(i)

    return new_set

if __name__ == "__main__":
    main()
