#!/usr/bin/python

def main():
    with open("plants.pi") as f:
    # with open("sample_input.pi") as f:
        raw_plants = f.read().split("\n")

    state, plant_rules = parse(raw_plants)
    pot_zero = 0

    # print(0, state, pot_zero)
    for i in xrange(50000000000):
        if i % 10000 == 0:
            print(i)
        state, pot_zero = one_generation(state, plant_rules, pot_zero)
        # print(i + 1, state, pot_zero)

    print(calculate_value(state, pot_zero))

def parse(raw_plants):
    initial_state = raw_plants.pop(0).split(": ")[1]

    # remove empty line
    raw_plants.pop(0)

    rules = {}
    for plant_rule in raw_plants:
        k, v = plant_rule.split(" => ")

        if v == ".":
            continue

        rules[k] = v

    return initial_state, rules

def one_generation(state, rules, pot_zero):
    prefix = "." * (3 - state.count(".", 0, state.find("#")))
    suffix = "." * 3
    temp_state = prefix + state + ".." + suffix

    pot_zero += len(prefix)
    next_state = ["."] * (len(temp_state))

    for rule, result in rules.iteritems():
        idx = -1
        while True:
            idx = temp_state.find(rule, idx + 1)
            if idx != - 1:
                next_state[idx + 2] = result
            else:
                break

    while next_state[0] == ".":
        pot_zero -= 1
        next_state.pop(0)

    while next_state[-1] == ".":
        next_state.pop()

    return "".join(next_state), pot_zero

def calculate_value(state, pot_zero):
    value = 0
    state_list = list(state)
    for i in range(len(state_list)):
        if state_list[i] == "#":
            value += i - pot_zero 

    return value

if __name__ == "__main__":
    main()
