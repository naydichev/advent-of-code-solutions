#!/usr/bin/env python3

import re
from collections import defaultdict, namedtuple

Gate = namedtuple("Gate", ["op", "inputs", "destination", "opname"])

binary_pattern = re.compile("^(\w+) ([A-Z]+) (\w+) -> (\w+)$")
not_pattern = re.compile("^NOT (\w+) -> (\w+)$")

AND = "AND"
OR = "OR"
NOT = "NOT"
RSHIFT = "RSHIFT"
LSHIFT = "LSHIFT"
ASSIGNED = "->"

COMMANDS = [
    AND,
    OR,
    NOT,
    LSHIFT,
    RSHIFT,
    ASSIGNED
]

TOP = 2 ** 16
def not_fix(x):
    v = ~x
    if v < 0:
        v = v + TOP
    return v

def literal_or_value(x):
    try:
        return int(x)
    except:
        return WIRES[x]

def assign(x):
    try:
        return int(x)
    except:
        return WIRES[x]

OPERATIONS = {
    AND: lambda x, y: literal_or_value(x) & literal_or_value(y),
    OR: lambda x, y: literal_or_value(x) | literal_or_value(y),
    NOT: lambda x: not_fix(literal_or_value(x)),
    LSHIFT: lambda x, n: literal_or_value(x) << int(n),
    RSHIFT: lambda x, n: literal_or_value(x) >> int(n),
    ASSIGNED: lambda x: literal_or_value(x)
}

WIRES = {}

def main(raw_gates):
    gates = parse(raw_gates)

    wire_to_gate = { gate.destination: gate for gate in gates }
    deps = create_dependencies(gates)
    process_gates(deps, gates, wire_to_gate)

    # for w, val in sorted(WIRES.items(), key=lambda x: x[0]):
    #     print(f"{w}: {val}")
    print(f"wire a is: {WIRES['a']}")


def create_dependencies(gates):
    dependencies = defaultdict(lambda: [])

    for gate in gates:
        inputs = []
        dest = gate.destination
        for i in gate.inputs:
            try:
                int(i)
            except:
                inputs.append(i)

        dependencies[dest].extend(inputs)

    return dependencies

def process_gates(dependencies, gates, wire_to_gate):
    while len(dependencies):
        dcopy = dependencies.copy()
        for w, _ in filter(lambda x: len(x[1]) == 0, dcopy.items()):
            wire = wire_to_gate[w]
            WIRES[wire.destination] = wire.op(*wire.inputs)

            del dependencies[w]

            for key in filter(lambda x: w in dependencies[x], dependencies.keys()):
                dependencies[key].remove(w)


def parse(raw):
    gates = []

    for gate in raw:
        binmatch = binary_pattern.match(gate)

        if binmatch:
            gates.append(Gate(OPERATIONS[binmatch.group(2)], (binmatch.group(1), binmatch.group(3)), binmatch.group(4), binmatch.group(2)))
        else:
            notmatch = not_pattern.match(gate)
            if notmatch:
                gates.append(Gate(OPERATIONS[NOT], (notmatch.group(1),), notmatch.group(2), NOT))
            else:
                parts = [x.rstrip().lstrip() for x in gate.split(" -> ")]
                gates.append(Gate(OPERATIONS[ASSIGNED], (parts[0],), parts[1], ASSIGNED))

    return gates


if __name__ == "__main__":
    with open("gates.pi") as f:
        main(f.read().rstrip().split("\n"))
